import pytest
import allure
from pages.main_page import MainPage
from pages.order_page import OrderPage
from locators import OrderPageLocators, MainPageLocators

class TestOrderFlow:
    """Тестовый класс для проверки процесса заказа"""

    @pytest.mark.parametrize("order_button_locator,test_data", [
        (MainPageLocators.ORDER_BUTTON_TOP, {
            "name": "Иван",
            "lastname": "Иванов",
            "address": "ул. Пушкина, д. 10",
            "phone": "+79991234567",
            "date": "15.12.2024",
            "comment": "Тестовый заказ 1",
            "metro": "sokolniki",
            "rental_period": "1_day",
            "color": "black"
        }),
        (MainPageLocators.ORDER_BUTTON_BOTTOM, {
            "name": "Мария",
            "lastname": "Петрова", 
            "address": "пр. Ленина, д. 25",
            "phone": "+79997654321",
            "date": "20.12.2024",
            "comment": "Тестовый заказ 2",
            "metro": "lubyanka",
            "rental_period": "2_days",
            "color": "grey"
        })
    ])
    @allure.title("Позитивный сценарий заказа через разные кнопки")
    @allure.feature("Order flow")
    @allure.story("Positive order scenario with different buttons")
    def test_order_flow_positive(self, driver, order_button_locator, test_data):
        """Позитивный тест процесса заказа через разные кнопки"""
        
        with allure.step("Open main page"):
            main_page = MainPage(driver)
            main_page.go_to_site()
            main_page.wait_for_page_load()
            main_page.close_cookie_banner()

        with allure.step("Click order button"):
            main_page.click_order_button_by_locator(order_button_locator)

        with allure.step("Wait for order page to load"):
            order_page = OrderPage(driver)
            order_page.wait_for_url_contains("order")

        with allure.step("Fill first part of order form"):
            order_page.fill_order_form_first_part(
                test_data["name"],
                test_data["lastname"],
                test_data["address"],
                test_data["phone"],
                test_data["metro"]
            )

        with allure.step("Fill second part of order form"):
            order_page.fill_order_form_second_part(
                test_data["date"],
                test_data["comment"],
                test_data["rental_period"],
                test_data["color"]
            )

        with allure.step("Confirm order"):
            order_page.confirm_order()

        with allure.step("Verify success message is displayed"):
            assert order_page.is_success_message_displayed(), "Order success message is not displayed"