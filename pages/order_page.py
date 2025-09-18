from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base_page import BasePage
from locators import OrderPageLocators
import allure

class OrderPage(BasePage):
    """Класс для работы со страницей оформления заказа"""

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()

    @allure.step("Заполнение первой части формы заказа")
    def fill_order_form_first_part(self, name, lastname, address, phone, metro_station="sokolniki"):
        """Заполнение первой части формы заказа"""
        self.wait_for_element_visible(self.locators.NAME_INPUT)

        # Заполняем основные поля
        self.fill_field(self.locators.NAME_INPUT, name)
        self.fill_field(self.locators.LASTNAME_INPUT, lastname)
        self.fill_field(self.locators.ADDRESS_INPUT, address)
        self.fill_field(self.locators.PHONE_INPUT, phone)

        # Выбор станции метро
        self._select_metro_station(metro_station)

        # Переходим к следующей части формы
        self.click_element(self.locators.NEXT_BUTTON)
        
        # Ждем загрузки второй части формы
        self.wait_for_element_visible(self.locators.DATE_INPUT)

    @allure.step("Выбор станции метро")
    def _select_metro_station(self, metro_station):
        """Внутренний метод для выбора станции метро"""
        # Кликаем на поле ввода метро
        self.click_element(self.locators.METRO_INPUT)
        
        # Ждем появления списка станций
        self.wait_for_element_visible((By.CLASS_NAME, "select-search__options"))
        
        # Выбираем станцию в зависимости от параметра
        if metro_station == "sokolniki":
            station_locator = self.locators.METRO_STATION_SOKOLNIKI
        elif metro_station == "lubyanka":
            station_locator = self.locators.METRO_STATION_LUBYANKA
        else:
            station_locator = self.locators.METRO_STATION_KREMLIN
        
        # Скроллим к станции и кликаем
        self.scroll_to_element(station_locator)
        self.click_element(station_locator)

    @allure.step("Заполнение второй части формы заказа")
    def fill_order_form_second_part(self, date, comment, rental_period="1_day", color="black"):
        """Заполнение второй части формы заказа"""
        self.wait_for_element_visible(self.locators.DATE_INPUT)

        # Заполняем дату (правильный формат)
        self._fill_date_field(date)
        
        # Выбор срока аренды
        self._select_rental_period(rental_period)

        # Выбор цвета
        self._select_color(color)

        # Заполняем комментарий
        if comment:
            self.fill_field(self.locators.COMMENT_INPUT, comment)
        
        # Кликаем по кнопке заказа
        self.safe_click(self.locators.ORDER_BUTTON)
        
        # Ждем появления модального окна подтверждения
        self.wait_for_element_visible(self.locators.CONFIRM_BUTTON, timeout=10)

    @allure.step("Заполнение поля даты")
    def _fill_date_field(self, date):
        """Внутренний метод для заполнения поля даты"""
        date_field = self.find_element(self.locators.DATE_INPUT)
        date_field.clear()
        
        # Используем правильный формат даты (например, 15.12.2024)
        date_field.send_keys(date)
        
        # Закрываем календарь нажатием Enter
        date_field.send_keys(Keys.ENTER)

    @allure.step("Выбор срока аренды")
    def _select_rental_period(self, rental_period):
        """Внутренний метод для выбора срока аренды"""
        self.safe_click(self.locators.RENTAL_PERIOD_DROPDOWN)
        
        # Ждем появления options
        self.wait_for_element_visible((By.CLASS_NAME, "Dropdown-option"), timeout=5)
        
        if rental_period == "1_day":
            self.safe_click(self.locators.RENTAL_OPTION_1_DAY)
        elif rental_period == "2_days":
            self.safe_click(self.locators.RENTAL_OPTION_2_DAYS)
        else:
            self.safe_click(self.locators.RENTAL_OPTION_7_DAYS)

    @allure.step("Выбор цвета самоката")
    def _select_color(self, color):
        """Внутренний метод для выбора цвета"""
        if color == "black":
            self.safe_click(self.locators.COLOR_BLACK)
        elif color == "grey":
            self.safe_click(self.locators.COLOR_GREY)

    @allure.step("Безопасный клик")
    def safe_click(self, locator, timeout=None):
        """Безопасный клик с обработкой перекрывающих элементов"""
        try:
            self.wait_for_element_clickable(locator, timeout)
            self.click_element(locator, timeout)
        except ElementClickInterceptedException:
            # Если элемент перекрыт, скроллим к нему и пробуем снова
            self.scroll_to_element(locator)
            self.wait_for_element_clickable(locator, timeout)
            self.click_element(locator, timeout)

    @allure.step("Подтверждение заказа")
    def confirm_order(self):
        """Подтверждение заказа"""
        self.wait_for_element_clickable(self.locators.CONFIRM_BUTTON, timeout=10)
        self.safe_click(self.locators.CONFIRM_BUTTON)
        
        # Ждем появления сообщения об успехе с увеличенным timeout
        self.wait_for_element_visible(self.locators.SUCCESS_MESSAGE, timeout=15)

    @allure.step("Проверка сообщения об успешном заказе")
    def is_success_message_displayed(self):
        """Проверка отображения сообщения об успешном заказе"""
        try:
            # Увеличиваем timeout для поиска элемента
            return self.is_element_visible(self.locators.SUCCESS_MESSAGE, timeout=5)
        except:
            return False

    @allure.step("Получение номера заказа")
    def get_order_number(self):
        """Получение номера заказа (если доступно)"""
        try:
            return self.get_element_text(self.locators.ORDER_NUMBER)
        except:
            return None