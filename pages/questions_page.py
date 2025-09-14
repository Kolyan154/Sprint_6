from .base_page import BasePage
from locators import QuestionsPageLocators
import time


class QuestionsPage(BasePage):
    "Класс для работы с разделом вопросов на главной странице"
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = QuestionsPageLocators()
    
    def click_question(self, question_index):
        "Клик по вопросу с индексом question_index"
        question_locator = self.locators.QUESTION_LOCATORS[question_index]
    
        # Скроллим к вопросу
        element = self.find_element(question_locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
    
        # Кликаем на вопрос
        self.click_element(question_locator)
        time.sleep(1)  # Даем время для анимации
    
    def is_question_visible(self, question_index):
        "Проверяет, виден ли вопрос с индексом question_index"
        question_locator = self.locators.QUESTION_LOCATORS[question_index]
        return self.is_element_visible(question_locator)
    
    def get_answer_text(self, index):
        "Получение текста ответа по индексу"
        answer_locator = self.locators.ANSWER_LOCATORS[index]
        return self.get_element_text(answer_locator)
    
    def is_answer_visible(self, index):
        "Проверка видимости ответа по индексу"
        answer_locator = self.locators.ANSWER_LOCATORS[index]
        return self.is_element_visible(answer_locator)
    
    def get_all_questions_count(self):
        "Получение количества вопросов"
        return len(self.locators.QUESTION_LOCATORS)