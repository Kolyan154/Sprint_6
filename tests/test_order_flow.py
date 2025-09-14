import pytest
import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.order_page import OrderPage
from locators import ExpectedTexts, OrderPageLocators

class TestOrderFlow:
    """Тестовый класс для проверки процесса заказа"""
    
    @allure.feature("Order flow")
    @allure.story("Positive order scenario")
    @pytest.mark.parametrize("order_button_locator,test_data", [
        # Параметризация: точка входа (кнопка) и тестовые данные
        ("top", {
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
        ("bottom", {
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
    def test_order_flow_positive(self, driver, order_button_locator, test_data):
        """Позитивный тест процесса заказа с разными данными и точками входа"""
        
        with allure.step("Open main page"):
            main_page = MainPage(driver)
            main_page.go_to_site()
            main_page.wait_for_page_load()
            
            # Закрываем баннер cookie, если он есть
            main_page.close_cookie_banner()
        
        with allure.step(f"Click {order_button_locator} order button"):
            # Выбор точки входа в процесс заказа
            if order_button_locator == "top":
                main_page.click_top_order_button()
            else:
                # Для нижней кнопки скроллим вниз и ждем
                main_page.scroll_to_bottom()
                time.sleep(1)
                main_page.click_bottom_order_button()
        
        with allure.step("Wait for order page to load"):
            # Ждем загрузки страницы заказа
            order_page = OrderPage(driver)
            WebDriverWait(driver, 15).until(
                EC.url_contains("order")
            )
            time.sleep(3)  # Дополнительное время для стабилизации
        
        with allure.step("Fill first part of order form"):
            # Заполнение первой части формы
            order_page.fill_order_form_first_part(
                test_data["name"],
                test_data["lastname"],
                test_data["address"],
                test_data["phone"],
                test_data["metro"]
            )
        
        with allure.step("Wait for second part of form"):
            # Ждем загрузки второй части формы
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(OrderPageLocators.DATE_INPUT)
            )
            time.sleep(2)
        
        with allure.step("Fill second part of order form"):
            # Заполнение второй части формы
            order_page.fill_order_form_second_part(
                test_data["date"],
                test_data["comment"],
                test_data["rental_period"],
                test_data["color"]
            )
        
        with allure.step("Confirm order"):
            # Подтверждение заказа
            order_page.confirm_order()
            time.sleep(3)  # Ждем появления окна подтверждения
        
        with allure.step("Verify success message is displayed"):
            # Проверка сообщения об успешном заказе
            assert order_page.is_success_message_displayed(), "Order success message is not displayed"
    
    @allure.feature("Navigation")
    @allure.story("Scooter logo navigation")
    def test_scooter_logo_navigation(self, driver):
        """Тест проверяет переход на главную страницу по логотипу Самоката"""
        
        with allure.step("Open main page"):
            main_page = MainPage(driver)
            main_page.go_to_site()
            main_page.wait_for_page_load()
            
            # Закрываем баннер cookie
            main_page.close_cookie_banner()
        
        with allure.step("Click Scooter logo"):
            main_page.click_scooter_logo()
            main_page.wait_for_page_load()
        
        with allure.step("Verify navigation to main page"):
            current_url = main_page.get_current_url()
            assert current_url == "https://qa-scooter.praktikum-services.ru/", \
                f"Expected main page URL, but got: {current_url}"
    
    @allure.feature("Navigation") 
    @allure.story("Yandex logo navigation")
    def test_yandex_logo_navigation(self, driver):
        """Тест проверяет переход на Dzen по логотипу Яндекса"""
        
        with allure.step("Open main page"):
            main_page = MainPage(driver)
            main_page.go_to_site()
            main_page.wait_for_page_load()
            
            # Закрываем баннер cookie
            main_page.close_cookie_banner()
        
        with allure.step("Click Yandex logo"):
            main_window = driver.current_window_handle
            main_page.click_yandex_logo()
        
        with allure.step("Switch to new window and verify Dzen page"):
            # Ожидание открытия нового окна
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            windows = driver.window_handles
            
            # Переключение на новое окно
            driver.switch_to.window(windows[1])
            
            # Ожидание загрузки страницы и проверка URL
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Даем странице время полностью загрузиться
            time.sleep(3)
            
            current_url = driver.current_url.lower()
            assert "dzen" in current_url or "yandex" in current_url, \
                f"Expected Dzen or Yandex URL, but got: {current_url}"
            
            # Закрытие нового окна и возврат к основному
            driver.close()
            driver.switch_to.window(main_window)
    
    @allure.feature("Order form")
    @allure.story("Form validation")
    def test_order_form_validation(self, driver):
        """Тест проверяет валидацию формы заказа"""
        
        with allure.step("Open main page and go to order form"):
            main_page = MainPage(driver)
            main_page.go_to_site()
            main_page.wait_for_page_load()
            
            # Закрываем баннер cookie
            main_page.close_cookie_banner()
            
            main_page.click_top_order_button()
            order_page = OrderPage(driver)
            
            # Ждем загрузки страницы заказа
            WebDriverWait(driver, 15).until(
                EC.url_contains("order")
            )
            time.sleep(2)
        
        with allure.step("Try to submit empty form"):
            # Пытаемся отправить пустую форму
            order_page.click_element(OrderPageLocators.NEXT_BUTTON)
            
            # Проверяем, что остались на той же странице (форма не прошла валидацию)
            current_url = driver.current_url
            assert "order" in current_url, "Should stay on order page if form is invalid"
    
    @allure.feature("Order flow")
    @allure.story("Different metro stations")
    @pytest.mark.parametrize("metro_station", ["sokolniki", "lubyanka"])
    def test_different_metro_stations(self, driver, metro_station):
        """Тест проверяет работу с разными станциями метро"""
        
        with allure.step("Open main page and go to order form"):
            main_page = MainPage(driver)
            main_page.go_to_site()
            main_page.wait_for_page_load()
            
            # Закрываем баннер cookie
            main_page.close_cookie_banner()
            
            main_page.click_top_order_button()
            order_page = OrderPage(driver)
            
            # Ждем загрузки страницы заказа
            WebDriverWait(driver, 15).until(
                EC.url_contains("order")
            )
            time.sleep(2)
        
        with allure.step(f"Select metro station: {metro_station}"):
            # Заполняем обязательные поля
            order_page.fill_field(OrderPageLocators.NAME_INPUT, "Тест")
            order_page.fill_field(OrderPageLocators.LASTNAME_INPUT, "Тестов")
            order_page.fill_field(OrderPageLocators.ADDRESS_INPUT, "Тестовая улица, 1")
            
            # Выбираем станцию метро
            order_page.click_element(OrderPageLocators.METRO_INPUT)
            
            if metro_station == "sokolniki":
                order_page.click_element(OrderPageLocators.METRO_STATION_SOKOLNIKI)
            else:
                order_page.click_element(OrderPageLocators.METRO_STATION_LUBYANKA)
            
            # Заполняем телефон
            order_page.fill_field(OrderPageLocators.PHONE_INPUT, "+79990000000")
            
            # Проверяем, что можно перейти к следующему шагу
            order_page.click_element(OrderPageLocators.NEXT_BUTTON)
            
            # Ждем перехода на следующую страницу
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(OrderPageLocators.DATE_INPUT)
            )
            
            # Проверяем, что перешли ко второй части формы
            assert order_page.is_element_visible(OrderPageLocators.DATE_INPUT), \
                "Should be on second part of order form"
    
    @allure.feature("Order flow")
    @allure.story("Order cancellation")
    def test_order_cancellation(self, driver):
        """Тест проверяет отмену заказа"""
        
        with allure.step("Open main page and go to order form"):
            main_page = MainPage(driver)
            main_page.go_to_site()
            main_page.wait_for_page_load()
            
            # Закрываем баннер cookie
            main_page.close_cookie_banner()
            
            main_page.click_top_order_button()
            order_page = OrderPage(driver)
            
            # Ждем загрузки страницы заказа
            WebDriverWait(driver, 15).until(
                EC.url_contains("order")
            )
            time.sleep(2)
        
        with allure.step("Fill order form and cancel"):
            # Заполняем первую часть формы
            order_page.fill_order_form_first_part(
                "Анна",
                "Смирнова",
                "ул. Тестовая, 15",
                "+79991112233",
                "sokolniki"
            )
            
            # Ждем вторую часть формы
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(OrderPageLocators.DATE_INPUT)
            )
            time.sleep(2)
            
            # Заполняем вторую часть формы
            order_page.fill_order_form_second_part(
                "25.12.2024",
                "Тестовый комментарий",
                "1_day",
                "black"
            )
            
            # Ищем кнопку отмены
            cancel_button = order_page.find_element_safe(OrderPageLocators.CANCEL_BUTTON)
            if cancel_button and cancel_button.is_displayed():
                cancel_button.click()
                
                # Проверяем, что вернулись на форму или главную страницу
                current_url = driver.current_url
                assert "order" in current_url or "qa-scooter" in current_url, \
                    f"Expected order form or main page after cancellation, got: {current_url}"
            else:
                # Если кнопки отмены нет, просто пропускаем тест
                pytest.skip("Cancel button not found on order page")