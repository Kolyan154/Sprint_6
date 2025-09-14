"""
Локаторы для сайта QA Scooter.
Содержит все селекторы для элементов страниц.
"""

from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы главной страницы"""
    
    # Кнопки заказа
    ORDER_BUTTON_TOP = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and not(contains(@class, 'Button_Middle'))]")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and contains(@class, 'Button_Middle')]")
    
    # Логотипы
    SCOOTER_LOGO = (By.XPATH, "//img[@alt='Scooter']")
    YANDEX_LOGO = (By.XPATH, "//img[@alt='Yandex']")
    
    # Разделы страницы
    QUESTIONS_SECTION = (By.XPATH, "//div[text()='Вопросы о важном']")
    
    # Навигационное меню (если есть)
    HOME_LINK = (By.XPATH, "//a[text()='Главная']")
    ORDER_STATUS_LINK = (By.XPATH, "//a[text()='Статус заказа']")

    # Баннер cookie
    COOKIE_BANNER = (By.XPATH, "//div[contains(@class, 'App_CookieConsent')]")
    COOKIE_BUTTON = (By.XPATH, "//button[contains(text(), 'да все привыкли')]")


class QuestionsPageLocators:
    """Локаторы раздела вопросов-ответов"""
    
    # Вопросы (аккордеон)
    QUESTION_1 = (By.ID, "accordion__heading-0")  # Сутки — 400 рублей...
    QUESTION_2 = (By.ID, "accordion__heading-1")  # Несколько самокатов
    QUESTION_3 = (By.ID, "accordion__heading-2")  # Расчет времени
    QUESTION_4 = (By.ID, "accordion__heading-3")  # Заказ сегодня
    QUESTION_5 = (By.ID, "accordion__heading-4")  # Продление заказа
    QUESTION_6 = (By.ID, "accordion__heading-5")  # Зарядка
    QUESTION_7 = (By.ID, "accordion__heading-6")  # Отмена заказа
    QUESTION_8 = (By.ID, "accordion__heading-7")  # Доставка за МКАД
    
    # Ответы
    ANSWER_1 = (By.ID, "accordion__panel-0")
    ANSWER_2 = (By.ID, "accordion__panel-1")
    ANSWER_3 = (By.ID, "accordion__panel-2")
    ANSWER_4 = (By.ID, "accordion__panel-3")
    ANSWER_5 = (By.ID, "accordion__panel-4")
    ANSWER_6 = (By.ID, "accordion__panel-5")
    ANSWER_7 = (By.ID, "accordion__panel-6")
    ANSWER_8 = (By.ID, "accordion__panel-7")
    
    # Списки для параметризации
    QUESTION_LOCATORS = [
        QUESTION_1, QUESTION_2, QUESTION_3, QUESTION_4,
        QUESTION_5, QUESTION_6, QUESTION_7, QUESTION_8
    ]
    
    ANSWER_LOCATORS = [
        ANSWER_1, ANSWER_2, ANSWER_3, ANSWER_4,
        ANSWER_5, ANSWER_6, ANSWER_7, ANSWER_8
    ]


class OrderPageLocators:
    """Локаторы страницы оформления заказа"""
    
    # Первая часть формы
    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LASTNAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")
    
    # Станции метро (можно добавить больше)
    METRO_STATION_SOKOLNIKI = (By.XPATH, "//div[text()='Сокольники']")
    METRO_STATION_LUBYANKA = (By.XPATH, "//div[text()='Лубянка']")
    METRO_STATION_KREMLIN = (By.XPATH, "//div[text()='Охотный ряд']")
    
    # Вторая часть формы
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.XPATH, "//div[text()='* Срок аренды']")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[contains(@class, 'Button_Middle') and text()='Заказать']")
    
    # Опции срока аренды
    RENTAL_OPTION_1_DAY = (By.XPATH, "//div[text()='сутки']")
    RENTAL_OPTION_2_DAYS = (By.XPATH, "//div[text()='двое суток']")
    RENTAL_OPTION_7_DAYS = (By.XPATH, "//div[text()='семеро суток']")
    
    # Цвета самоката
    COLOR_BLACK = (By.ID, "black")
    COLOR_GREY = (By.ID, "grey")
    
    # Подтверждение заказа
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Да']")
    CANCEL_BUTTON = (By.XPATH, "//button[text()='Нет']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(), 'Заказ оформлен')]")
    ORDER_NUMBER = (By.XPATH, "//div[contains(text(), 'Номер заказа')]")


class OrderStatusLocators:
    """Локаторы для проверки статуса заказа"""
    
    ORDER_NUMBER_INPUT = (By.XPATH, "//input[@placeholder='Введите номер заказа']")
    GO_BUTTON = (By.XPATH, "//button[text()='Go!']")
    ORDER_STATUS = (By.XPATH, "//div[contains(@class, 'Order_Text')]")
    NOT_FOUND_MESSAGE = (By.XPATH, "//div[contains(text(), 'Заказ не найден')]")


class CommonLocators:
    """Общие локаторы для всех страниц"""
    
    # Заголовки
    PAGE_TITLE = (By.XPATH, "//title")
    MAIN_HEADING = (By.XPATH, "//h1")
    
    # Кнопки
    BUTTON_PRIMARY = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g')]")
    BUTTON_SECONDARY = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g Button_Middle')]")
    
    # Лоадеры
    LOADER = (By.XPATH, "//div[contains(@class, 'Loader')]")
    
    # Сообщения
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'ErrorMessage')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'SuccessMessage')]")


class ExpectedTexts:
    """Ожидаемые тексты для проверок"""
    
    # Ответы на вопросы
    ANSWER_TEXTS = [
        "Сутки — 400 рублей. Оплата курьеру — наличными или картой.",
        "Пока что у нас так: один заказ — один самокат.",
        "Допустим, вы оформляете заказ на 8 мая.",
        "Только начиная с завтрашнего дня.",
        "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010.",
        "Самокат приезжает к вам с полной зарядкой.",
        "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои.",
        "Да, обязательно. Всем самокатов! И Москве, и Московской области."
    ]
    
    # Заголовки страниц
    MAIN_PAGE_TITLE = "Яндекс Самокат"
    ORDER_PAGE_TITLE = "Яндекс Самокат — заказ"
    
    # Сообщения
    ORDER_SUCCESS = "Заказ оформлен"
    ORDER_NOT_FOUND = "Заказ не найден"