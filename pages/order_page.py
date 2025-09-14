from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .base_page import BasePage
from locators import OrderPageLocators
from selenium.webdriver.common.keys import Keys
import time

class OrderPage(BasePage):
    """Класс для работы со страницей оформления заказа"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()  # Добавляем атрибут locators
    
    def fill_order_form_first_part(self, name, lastname, address, phone, metro_station="sokolniki"):
        """Заполнение первой части формы заказа"""
        # Ждем появления полей формы
        self.wait_for_element_visible(self.locators.NAME_INPUT)
        
        self.fill_field(self.locators.NAME_INPUT, name)
        self.fill_field(self.locators.LASTNAME_INPUT, lastname)
        self.fill_field(self.locators.ADDRESS_INPUT, address)
        
        # Выбор станции метро
        self.click_element(self.locators.METRO_INPUT)
        if metro_station == "sokolniki":
            self.click_element(self.locators.METRO_STATION_SOKOLNIKI)
        elif metro_station == "lubyanka":
            self.click_element(self.locators.METRO_STATION_LUBYANKA)
        else:
            self.click_element(self.locators.METRO_STATION_KREMLIN)
        
        self.fill_field(self.locators.PHONE_INPUT, phone)
        self.click_element(self.locators.NEXT_BUTTON)
    
    def fill_order_form_second_part(self, date, comment, rental_period="1_day", color="black"):
        """Заполнение второй части формы заказа"""
        # Ждем появления полей второй части формы
        self.wait_for_element_visible(self.locators.DATE_INPUT)
        
        # Сначала заполняем дату
        self.fill_field(self.locators.DATE_INPUT, date)
        
        # Используем клавишу TAB для перехода к следующему полю вместо клика
        date_field = self.find_element(self.locators.DATE_INPUT)
        date_field.send_keys(Keys.TAB)
        time.sleep(1)  # Небольшая пауза
        
        # Выбор срока аренды
        self.safe_click(self.locators.RENTAL_PERIOD_DROPDOWN)
        if rental_period == "1_day":
            self.safe_click(self.locators.RENTAL_OPTION_1_DAY)
        elif rental_period == "2_days":
            self.safe_click(self.locators.RENTAL_OPTION_2_DAYS)
        else:
            self.safe_click(self.locators.RENTAL_OPTION_7_DAYS)
        
         # Выбор цвета
        if color:
            color_locator = (By.ID, f"{color}")
            self.click_element(color_locator)
        
        # Ввод комментария
        self.input_text(self.locators.COMMENT_INPUT, comment)
        
        # Кликаем по кнопке заказа
        self.click_element(self.locators.ORDER_BUTTON)
    
def safe_click(self, locator, timeout=None):
    """Безопасный клик с обработкой перекрывающих элементов"""
    try:
        self.click_element(locator, timeout)
    except ElementClickInterceptedException:
        # Если элемент перекрыт, скроллим к нему и пробуем снова
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
        self.click_element(locator, timeout)
    
    def confirm_order(self):
        """Подтверждение заказа"""
        self.safe_click(self.locators.CONFIRM_BUTTON)
    
    def is_success_message_displayed(self):
        """Проверка отображения сообщения об успешном заказе"""
        try:
            return self.is_element_visible(self.locators.SUCCESS_MESSAGE)
        except:
            return False
    
    def get_order_number(self):
        """Получение номера заказа (если доступно)"""
        try:
            return self.get_element_text(self.locators.ORDER_NUMBER)
        except:
            return None