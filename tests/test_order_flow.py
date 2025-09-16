import pytest
import allure
import time
from pages.main_page import MainPage
from pages.order_page import OrderPage
from locators import ExpectedTexts, OrderPageLocators

class TestOrderFlow:
    """Тестовый класс для проверки процесса заказа"""

    # Разделяем параметризованные тесты на отдельные методы
    @allure.title("Позитивный сценарий заказа через верхнюю кнопку")
    @allure.feature("Order flow")
    @allure.story("Positive order scenario - top button")
    def test_order_flow_positive_top_button(self, driver):
        """Позитивный тест процесса заказа через верхнюю кнопку"""
        test_data = {
            "name": "Иван",
            "lastname": "Иванов",
            "address": "ул. Пушкина, д. 10",
            "phone": "+79991234567",
            "date": "15.12.2024",
            "comment": "Тестовый заказ 1",
            "metro": "sokolniki",
            "rental_period": "1_day",
            "color": "black"
        }
        self._execute_order_flow_test(driver, "top", test_data)

    @allure.title("Позитивный сценарий заказа через нижнюю кнопку")
    @allure.feature("Order flow")
    @allure.story("Positive order scenario - bottom button")
    def test_order_flow_positive_bottom_button(self, driver):
        """Позитивный тест процесса заказа через нижнюю кнопку"""
        test_data = {
            "name": "Мария",
            "lastname": "Петрова", 
            "address": "пр. Ленина, д. 25",
            "phone": "+79997654321",
            "date": "20.12.2024",
            "comment": "Тестовый заказ 2",
            "metro": "lubyanka",
            "rental_period": "2_days",
            "color": "grey"
        }
        self._execute_order_flow_test(driver, "bottom", test_data)

    def _execute_order_flow_test(self, driver, order_button_locator, test_data):
        """Общий метод для выполнения теста заказа"""
        with allure.step("Open main page"):
            main_page = MainPage(driver)
            main_page.go_to_site()
            main_page.wait_for_page_load()
            main_page.close_cookie_banner()

        with allure.step(f"Click {order_button_locator} order button"):
            if order_button_locator == "top":
                main_page.click_top_order_button()
            else:
                main_page.scroll_to_bottom()
                time.sleep(1)
                main_page.click_bottom_order_button()

        with allure.step("Wait for order page to load"):
            order_page = OrderPage(driver)
            order_page.wait_for_url_contains("order")
            time.sleep(2)

        with allure.step("Fill first part of order form"):
            order_page.fill_order_form_first_part(
                test_data["name"],
                test_data["lastname"],
                test_data["address"],
                test_data["phone"],
                test_data["metro"]
            )

        with allure.step("Wait for second part of form"):
            order_page.wait_for_element_visible(OrderPageLocators.DATE_INPUT)
            time.sleep(1)

        with allure.step("Fill second part of order form"):
            order_page.fill_order_form_second_part(
                test_data["date"],
                test_data["comment"],
                test_data["rental_period"],
                test_data["color"]
            )

        with allure.step("Confirm order"):
            order_page.confirm_order()
            time.sleep(2)

        with allure.step("Verify success message is displayed"):
            assert order_page.is_success_message_displayed(), "Order success message is not displayed"
