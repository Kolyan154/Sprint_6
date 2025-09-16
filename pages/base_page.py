from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import allure

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

    @allure.step("Переход на сайт")
    def go_to_site(self, url=None):
        """
        Переход на указанный URL или базовый URL сайта.
        
        :param url: Опциональный URL для перехода
        """
        target_url = url or self.base_url
        self.driver.get(target_url)
        self.wait_for_page_load()

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        """Получение текущего URL страницы."""
        return self.driver.current_url

    @allure.step("Получение заголовка страницы")
    def get_page_title(self):
        """Получение заголовка текущей страницы."""
        return self.driver.title

    @allure.step("Обновление страницы")
    def refresh_page(self):
        """Обновление текущей страницы."""
        self.driver.refresh()
        self.wait_for_page_load()

    @allure.step("Навигация назад")
    def go_back(self):
        """Навигация назад в истории браузера."""
        self.driver.back()
        self.wait_for_page_load()

    @allure.step("Навигация вперед")
    def go_forward(self):
        """Навигация вперед в истории браузера."""
        self.driver.forward()
        self.wait_for_page_load()

    # --- Методы ожидания ---

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self, timeout=None):
        """
        Ожидание полной загрузки страницы.
        
        :param timeout: Максимальное время ожидания в секундах
        :return: True если страница загрузилась, иначе False
        """
        timeout = timeout or self.timeout
        try:
            self.wait_for_condition(
                lambda driver: driver.execute_script("return document.readyState") == "complete",
                timeout
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Безопасный клик на элемент")
    def safe_click(self, locator, timeout=None):
        """Безопасный клик с обработкой перекрывающих элементов"""
        try:
            self.click_element(locator, timeout)
        except ElementClickInterceptedException:
            # Если элемент перекрыт, скроллим к нему и пробуем снова
            element = self.find_element(locator, timeout)
            self.scroll_to_element(locator)
            time.sleep(1)
            self.click_element(locator, timeout)

    @allure.step("Ожидание появления элемента")
    def wait_for_element(self, locator, timeout=None):
        """
        Ожидание появления элемента на странице.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: True если элемент появился, иначе False
        """
        timeout = timeout or self.timeout
        try:
            self.wait_for_condition(
                EC.presence_of_element_located(locator),
                timeout
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание видимости элемента")
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Ожидание видимости элемента на странице.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: True если элемент видим, иначе False
        """
        timeout = timeout or self.timeout
        try:
            self.wait_for_condition(
                EC.visibility_of_element_located(locator),
                timeout
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание кликабельности элемента")
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Ожидание, пока элемент станет кликабельным.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: True если элемент кликабелен, иначе False
        """
        timeout = timeout or self.timeout
        try:
            self.wait_for_condition(
                EC.element_to_be_clickable(locator),
                timeout
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание условия")
    def wait_for_condition(self, condition, timeout=None):
        """
        Универсальный метод ожидания условия.
        
        :param condition: Условие для ожидания
        :param timeout: Максимальное время ожидания в секундах
        :return: Результат условия
        """
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout, self.poll_frequency).until(condition)

    @allure.step("Ожидание URL")
    def wait_for_url_contains(self, text, timeout=None):
        """
        Ожидание, пока URL содержит указанный текст.
        
        :param text: Текст для поиска в URL
        :param timeout: Максимальное время ожидания в секундах
        :return: True если URL содержит текст, иначе False
        """
        timeout = timeout or self.timeout
        try:
            self.wait_for_condition(EC.url_contains(text), timeout)
            return True
        except TimeoutException:
            return False

    # --- Методы поиска элементов ---

    @allure.step("Поиск элемента")
    def find_element(self, locator, timeout=None):
        """
        Поиск элемента с явным ожиданием.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: Найденный WebElement
        """
        timeout = timeout or self.timeout
        return self.wait_for_condition(
            EC.presence_of_element_located(locator),
            timeout
        )

    @allure.step("Поиск нескольких элементов")
    def find_elements(self, locator, timeout=None):
        """
        Поиск нескольких элементов с явным ожиданием.
        
        :param locator: Кортеж (By, selector) для поиска элементов
        :param timeout: Максимальное время ожидания в секундах
        :return: Список найденных WebElements
        """
        timeout = timeout or self.timeout
        return self.wait_for_condition(
            EC.presence_of_all_elements_located(locator),
            timeout
        )

    @allure.step("Безопасный поиск элемента")
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

    @allure.step("Клик по элементу")
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

    @allure.step("Заполнение поля")
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

    @allure.step("Получение текста элемента")
    def get_element_text(self, locator, timeout=None):
        """
        Получение текста элемента.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: Текст элемента
        """
        element = self.find_element(locator, timeout)
        return element.text.strip()

    @allure.step("Получение атрибута элемента")
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

    @allure.step("Проверка видимости элемента")
    def is_element_visible(self, locator, timeout=10):
        """Проверяет, виден ли элемент"""
        try:
            element = self.wait_for_condition(
                EC.visibility_of_element_located(locator),
                timeout
            )
            return element.is_displayed()
        except TimeoutException:
            return False

    @allure.step("Проверка наличия элемента")
    def is_element_present(self, locator, timeout=None):
        """
        Проверка наличия элемента на странице.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        :return: True если элемент присутствует, иначе False
        """
        return self.wait_for_element(locator, timeout)


    @allure.step("Выполнение JavaScript")
    def execute_script(self, script, *args):
        """
        Выполнение JavaScript кода.
        
        :param script: JavaScript код для выполнения
        :param args: Аргументы для скрипта
        :return: Результат выполнения скрипта
        """
        return self.driver.execute_script(script, *args)

    @allure.step("Скролл к элементу")
    def scroll_to_element(self, locator, timeout=None):
        """
        Скролл к элементу.
        
        :param locator: Кортеж (By, selector) для поиска элемента
        :param timeout: Максимальное время ожидания в секундах
        """
        element = self.find_element(locator, timeout)
        self.execute_script("arguments[0].scrollIntoView(true);", element)

    @allure.step("Скролл к верху страницы")
    def scroll_to_top(self):
        """Скролл к верху страницы."""
        self.execute_script("window.scrollTo(0, 0);")

    @allure.step("Скролл к низу страницы")
    def scroll_to_bottom(self):
        """Скролл к низу страницы."""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # --- Методы работы с окнами ---

    @allure.step("Переключение на новое окно")
    def switch_to_new_window(self, timeout=None):
        """
        Переключение на новое окно/вкладку.
        
        :param timeout: Максимальное время ожидания в секундах
        """
        timeout = timeout or self.timeout
        original_window = self.driver.current_window_handle

        self.wait_for_condition(
            lambda driver: len(driver.window_handles) > 1,
            timeout
        )

        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

        self.wait_for_page_load()

    @allure.step("Закрытие текущего окна")
    def close_current_window(self):
        """Закрытие текущего окна/вкладки."""
        main_window = self.driver.window_handles[0]
        self.driver.close()
        self.driver.switch_to.window(main_window)

    # --- Утилитные методы ---

    @allure.step("Создание скриншота")
    def take_screenshot(self, filename=None):
        """
        Создание скриншота текуной страницы.
        
        :param filename: Имя файла для сохранения
        :return: Путь к сохраненному скриншоту
        """
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"

        self.driver.save_screenshot(filename)
        return filename

    @allure.step("Ожидание")
    def wait(self, seconds):
        """
        Явное ожидание.
        
        :param seconds: Количество секунд для ожидания
        """
        time.sleep(seconds)

    @allure.step("Получение исходного кода страницы")
    def get_page_source(self):
        """Получение исходного кода страницы."""
        return self.driver.page_source