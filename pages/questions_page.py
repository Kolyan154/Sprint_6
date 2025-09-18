from .base_page import BasePage
from locators import QuestionsPageLocators
import allure

class QuestionsPage(BasePage):
    """Класс для работы с разделом вопросов на главной странице"""

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = QuestionsPageLocators()

    @allure.step("Клик по вопросу")
    def click_question(self, question_index):
        """Клик по вопросу с индексом question_index"""
        question_locator = self.locators.QUESTION_LOCATORS[question_index]
        
        # Скроллим к вопросу и ждем кликабельности
        self.scroll_to_element(question_locator)
        self.wait_for_element_clickable(question_locator)
        
        # Кликаем на вопрос
        self.click_element(question_locator)
        
        # Ждем появления ответа вместо sleep
        answer_locator = self.locators.ANSWER_LOCATORS[question_index]
        self.wait_for_element_visible(answer_locator)

    @allure.step("Проверка видимости вопроса")
    def is_question_visible(self, question_index):
        """Проверяет, виден ли вопрос с индексом question_index"""
        question_locator = self.locators.QUESTION_LOCATORS[question_index]
        return self.is_element_visible(question_locator)

    @allure.step("Получение текста ответа")
    def get_answer_text(self, index):
        """Получение текста ответа по индексу"""
        answer_locator = self.locators.ANSWER_LOCATORS[index]
        return self.get_element_text(answer_locator)

    @allure.step("Проверка видимости ответа")
    def is_answer_visible(self, index):
        """Проверка видимости ответа по индексу"""
        answer_locator = self.locators.ANSWER_LOCATORS[index]
        return self.is_element_visible(answer_locator)

    @allure.step("Получение количества вопросов")
    def get_all_questions_count(self):
        """Получение количества вопросов"""
        return len(self.locators.QUESTION_LOCATORS)