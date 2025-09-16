from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from .base_page import BasePage
from locators import OrderPageLocators
import time
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

        self.fill_field(self.locators.NAME_INPUT, name)
        self.fill_field(self.locators.LASTNAME_INPUT, lastname)
        self.fill_field(self.locators.ADDRESS_INPUT, address)

        self.click_element(self.locators.METRO_INPUT)
        if metro_station == "sokolniki":
            self.click_element(self.locators.METRO_STATION_SOKOLNIKI)
        elif metro_station == "lubyanka":
            self.click_element(self.locators.METRO_STATION_LUBYANKA)
        else:
            self.click_element(self.locators.METRO_STATION_KREMLIN)

        self.fill_field(self.locators.PHONE_INPUT, phone)
        self.click_element(self.locators.NEXT_BUTTON)

    @allure.step("Заполнение второй части формы заказа")  
    def fill_order_form_second_part(self, date, comment, rental_period="1_day", color="black"):
        """Заполнение второй части формы заказа"""
        self.wait_for_element_visible(self.locators.DATE_INPUT)

        date_field = self.find_element(self.locators.DATE_INPUT)
        date_field.clear()
        date_field.send_keys(date)
        
        self._close_datepicker()
        
        # Работаем с периодом аренды
        self._select_rental_period(rental_period)
        
        # Выбираем цвет
        if color:
            self._select_color(color)

        # Заполняем комментарий
        self.fill_field(self.locators.COMMENT_INPUT, comment)

        # Нажимаем кнопку заказа
        self._click_order_button()

    def _close_datepicker(self):
        """Закрытие календаря даты"""
        try:
            # Способ 1: ESC клавиша
            date_field = self.find_element(self.locators.DATE_INPUT)
            date_field.send_keys(Keys.ESCAPE)
        except:
            try:
                # Способ 2: Клик в другое место
                header = self.find_element((By.XPATH, "//div[contains(@class, 'Order_Header')]"))
                header.click()
            except:
                # Способ 3: JavaScript клик по body
                self.execute_script("document.activeElement.blur();")
                self.execute_script("document.body.click();")

    def _select_rental_period(self, rental_period):
        """Выбор периода аренды"""
        # Ждем пока dropdown станет кликабельным
        self.wait_for_element_clickable(self.locators.RENTAL_PERIOD_DROPDOWN)
        
        # Открываем dropdown через JavaScript (обходит возможное перекрытие)
        dropdown = self.find_element(self.locators.RENTAL_PERIOD_DROPDOWN)
        self.execute_script("arguments[0].click();", dropdown)
        
        # Ждем появления опций
        time.sleep(3)
        
        # Выбираем опцию
        if rental_period == "1_day":
            option = self.find_element(self.locators.RENTAL_OPTION_1_DAY)
        elif rental_period == "2_days":
            option = self.find_element(self.locators.RENTAL_OPTION_2_DAYS)
        else:
            option = self.find_element(self.locators.RENTAL_OPTION_7_DAYS)
        
        # Кликаем через JavaScript
        self.execute_script("arguments[0].click();", option)

    def _select_color(self, color):
        """Выбор цвета самоката"""
        color_locator = (By.ID, color)  
        try:
            color_element = self.find_element(color_locator)
            self.execute_script("arguments[0].click();", color_element)
        except:
            # Альтернативный способ если ID не работает
            if color == "black":
                color_locator = (By.XPATH, "//input[@id='black']")
            elif color == "grey":
                color_locator = (By.XPATH, "//input[@id='grey']")
            color_element = self.find_element(color_locator)
            self.execute_script("arguments[0].click();", color_element)

    def _click_order_button(self):
        """Клик по кнопке заказа с проверкой видимости"""
        order_button = self.find_element(self.locators.ORDER_BUTTON)
        
        # Прокручиваем к кнопке
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", order_button)
        
        # Ждем пока кнопка станет кликабельной
        self.wait_for_element_clickable(self.locators.ORDER_BUTTON)
        
        # Пробуем обычный клик, если не получается - JS клик
        try:
            order_button.click()
        except ElementClickInterceptedException:
            self.execute_script("arguments[0].click();", order_button)

    @allure.step("Безопасный клик")  
    def safe_click(self, locator, timeout=None):
        """Безопасный клик с обработкой перекрывающих элементов"""
        try:
            self.click_element(locator, timeout)
        except ElementClickInterceptedException:
            element = self.find_element(locator, timeout)
            self.scroll_to_element(locator)
            time.sleep(1)
            self.click_element(locator, timeout)

    @allure.step("Подтверждение заказа") 
    def confirm_order(self):
        """Подтверждение заказа"""
        self.safe_click(self.locators.CONFIRM_BUTTON)

    @allure.step("Проверка сообщения об успешном заказе")  
    def is_success_message_displayed(self):
        """Проверка отображения сообщения об успешном заказе"""
        try:
            return self.is_element_visible(self.locators.SUCCESS_MESSAGE)
        except:
            return False

    @allure.step("Получение номера заказа")  
    def get_order_number(self):
        """Получение номера заказа (если доступно)"""
        try:
            return self.get_element_text(self.locators.ORDER_NUMBER)
        except:
            return None