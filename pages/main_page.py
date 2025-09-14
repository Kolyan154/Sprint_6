from .base_page import BasePage
from locators import MainPageLocators

class MainPage(BasePage):
    """Класс для работы с главной страницей сервиса"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_top_order_button(self):
        """Клик по верхней кнопке заказа"""
        self.click_element(MainPageLocators.ORDER_BUTTON_TOP)
    
    def click_bottom_order_button(self):
        """Клик по нижней кнопке заказа"""
        # Прокручиваем к кнопке и кликаем
        self.scroll_to_element(MainPageLocators.ORDER_BUTTON_BOTTOM)
        self.click_element(MainPageLocators.ORDER_BUTTON_BOTTOM)
    
    def click_scooter_logo(self):
        """Клик по логотипу Самоката"""
        self.click_element(MainPageLocators.SCOOTER_LOGO)
    
    def click_yandex_logo(self):
        """Клик по логотипу Яндекса"""
        self.click_element(MainPageLocators.YANDEX_LOGO)
    
    def scroll_to_questions_section(self):
        """Скролл к разделу с вопросами"""
        self.scroll_to_element(MainPageLocators.QUESTIONS_SECTION)
    
    def close_cookie_banner(self):
        """Закрытие баннера cookie, если он присутствует"""
        cookie_banner = self.find_element_safe(MainPageLocators.COOKIE_BANNER)
        if cookie_banner and cookie_banner.is_displayed():
            cookie_button = self.find_element_safe(MainPageLocators.COOKIE_BUTTON)
            if cookie_button:
                cookie_button.click()
                self.wait(1)  # Небольшая пауза после закрытия