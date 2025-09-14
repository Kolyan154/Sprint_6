from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class BasePage:
    """
    Базовый класс Page Object для всех страниц.
    Содержит общие методы для работы с веб-элементами.
    """
    
    def __init__(self, driver):
        """
        Инициализация базовой страницы.
        
        :param driver: WebDriver instance для управления браузером
        """
        self.driver = driver
        self.base_url = "https://qa-scooter.praktikum-services.ru/"
        self.timeout = 10
        self.poll_frequency = 0.5
    
    # --- Основные методы навигации ---
    
    def go_to_site(self, url=None):
        """
        Переход на указанный URL или базовый URL сайта.
        
        :param url: Опциональный URL для перехода
        """
        target_url = url or self.base_url
        self.driver.get(target_url)
        self.wait_for_page_load()
    
    def get_current_url(self):
        """Получение текущего URL страницы."""
        return self.driver.current_url
    
    def get_page_title(self):
        """Получение заголовка текущей страницы."""
        return self.driver.title
    
    def refresh_page(self):
        """Обновление текущей страницы."""
        self.driver.refresh()
        self.wait_for_page_load()
    
    def go_back(self):
        """Навигация назад в истории браузера."""
        self.driver.back()
        self.wait_for_page_load()
    
    def go_forward(self):
        """Навигация вперед в истории браузера."""
        self.driver.forward()
        self.wait_for_page_load()
    
    # --- Методы ожидания ---
    
    def wait_for_page_load(self, timeout=None):
        """
        Ожидание полной загрузки страницы.
        
        :param timeout: Максимальное время ожидания в секундах
        :return: True если страница загрузилась, иначе False
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False
    
    def safe_click(self, locator, timeout=None):
        """Безопасный клик с обработкой перекрывающих элементов"""
        try:
            self.click_element(locator, timeout)
        except ElementClickInterceptedException:
            # Если элемент перекрыт, скроллим к нему и пробуем снова
            element = self.find_element(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)  # Даем время для скролла
            self.click_element(locator, timeout)
        
    def wait_for_element(self, locator, timeout=None):
        """
        Ожидание появления элемента на странице.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: True если элемент появился, иначе False
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Ожидание видимости элемента на странице.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: True если элемент видим, иначе False
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Ожидание, пока элемент станет кликабельным.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: True если элемент кликабелен, иначе False
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            return False
    
    # --- Методы поиска элементов ---
    
    def find_element(self, locator, timeout=None):
        """
        Поиск элемента с явным ожиданием.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: Найденный WebElement
        """
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout, self.poll_frequency).until(
            EC.presence_of_element_located(locator),
            message=f"Не удалось найти элемент по локатору: {locator}"
        )
    
    def find_elements(self, locator, timeout=None):
        """
        Поиск нескольких элементов с явным ожиданием.
        
        :param locator: Кортеж (By, selector) для поиска элементов
        :param timeout: Максимальное время ожидания в секундах
        :return: Список найденных WebElements
        """
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout, self.poll_frequency).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не удалось найти элементы по локатору: {locator}"
        )
    
    def find_element_safe(self, locator, timeout=None):
        """
        Безопасный поиск элемента (без исключений).
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: WebElement если найден, иначе None
        """
        try:
            return self.find_element(locator, timeout)
        except (TimeoutException, NoSuchElementException):
            return None
    
    # --- Методы взаимодействия с элементами ---
    
    def click_element(self, locator, timeout=None):
        """
        Клик по элементу с предварительным ожиданием.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        """
        element = self.find_element(locator, timeout)
        self.wait_for_element_clickable(locator, timeout)
        
        try:
            element.click()
        except StaleElementReferenceException:
            element = self.find_element(locator, timeout)
            element.click()
    
    def fill_field(self, locator, text, timeout=None):
        """
        Заполнение поля текстом.
        
        :param locator: Кортеж (By, selector) для поиска поля
        :param text: Текст для ввода
        :param timeout: Максимальное время ожидания в секундах
        """
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator, timeout=None):
        """
        Получение текста элемента.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: Текст элемента
        """
        element = self.find_element(locator, timeout)
        return element.text.strip()
    
    def get_element_attribute(self, locator, attribute, timeout=None):
        """
        Получение значения атрибута элемента.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param attribute: Название атрибута
        :param timeout: Максимальное время ожидания в секундах
        :return: Значение атрибута
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)
    
    def is_element_visible(self, locator, timeout=10):
        """Проверяет, виден ли элемент"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=None):
        """
        Проверка наличия элемента на странице.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: True если элемент присутствует, иначе False
        """
        return self.wait_for_element(locator, timeout)
    
    
    def execute_script(self, script, *args):
        """
        Выполнение JavaScript кода.
        
        :param script: JavaScript код для выполнения
        :param args: Аргументы для скрипта
        :return: Результат выполнения скрипта
        """
        return self.driver.execute_script(script, *args)
    
    def scroll_to_element(self, locator, timeout=None):
        """
        Скролл к элементу.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        """
        element = self.find_element(locator, timeout)
        self.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def scroll_to_top(self):
        """Скролл к верху страницы."""
        self.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_bottom(self):
        """Скролл к низу страницы."""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # --- Методы работы с окнами ---
    
    def switch_to_new_window(self, timeout=None):
        """
        Переключение на новое окно/вкладку.
        
        :param timeout: Максимальное время ожидания в секундах
        """
        timeout = timeout or self.timeout
        original_window = self.driver.current_window_handle
        
        WebDriverWait(self.driver, timeout).until(
            lambda driver: len(driver.window_handles) > 1
        )
        
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break
        
        self.wait_for_page_load()
    
    def close_current_window(self):
        """Закрытие текущего окна/вкладки."""
        main_window = self.driver.window_handles[0]
        self.driver.close()
        self.driver.switch_to.window(main_window)
    
    # --- Утилитные методы ---
    
    def take_screenshot(self, filename=None):
        """
        Создание скриншота текущей страницы.
        
        :param filename: Имя файла для сохранения
        :return: Путь к сохраненному скриншоту
        """
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        
        self.driver.save_screenshot(filename)
        return filename
    
    def wait(self, seconds):
        """
        Явное ожидание.
        
        :param seconds: Количество секунд для ожидания
        """
        time.sleep(seconds)
    
    def get_page_source(self):
        """Получение исходного кода страницы."""
        return self.driver.page_source