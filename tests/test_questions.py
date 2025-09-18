import pytest
import allure
from pages.main_page import MainPage
from locators import QuestionsPageLocators
from locators import ExpectedTexts
from pages.questions_page import QuestionsPage

class TestQuestions:
    """Тестовый класс для проверки раздела с вопросами"""
    
    @allure.feature("Questions section")
    @allure.story("FAQ functionality")
    @pytest.mark.parametrize("question_index,expected_answer", [
        # Параметризация с использованием данных из locators.py
        (0, ExpectedTexts.ANSWER_TEXTS[0]),
        (1, ExpectedTexts.ANSWER_TEXTS[1]),
        (2, ExpectedTexts.ANSWER_TEXTS[2]),
        (3, ExpectedTexts.ANSWER_TEXTS[3]),
        (4, ExpectedTexts.ANSWER_TEXTS[4]),
        (5, ExpectedTexts.ANSWER_TEXTS[5]),
        (6, ExpectedTexts.ANSWER_TEXTS[6]),
        (7, ExpectedTexts.ANSWER_TEXTS[7])
    ])
    def test_question_answer_displayed(self, driver, question_index, expected_answer):
        """Тест проверяет отображение правильного ответа при клике на вопрос"""
        
        with allure.step("Open main page"):
            # Открытие главной страницы
            main_page = MainPage(driver)
            main_page.go_to_site()
        
        with allure.step("Scroll to questions section"):
            # Скролл к разделу с вопросами
            main_page.scroll_to_questions_section()
        
        with allure.step(f"Click on question {question_index + 1}"):
            # Клик по вопросу
            questions_page = QuestionsPage(driver)
            questions_page.click_question(question_index)
        
        with allure.step("Verify answer is displayed and contains expected text"):
            # Проверка видимости и содержания ответа
            assert questions_page.is_answer_visible(question_index), f"Answer for question {question_index + 1} is not visible"
            answer_text = questions_page.get_answer_text(question_index)
            assert expected_answer in answer_text, f"Expected answer '{expected_answer}' not found. Got: '{answer_text}'"
    
    @allure.feature("Questions section")
    @allure.story("All questions should be available")
    @pytest.mark.parametrize("question_index", [0, 1, 2, 3, 4, 5, 6, 7])
    def test_all_questions_visible(self, driver, question_index):
        """Тест проверяет, что все вопросы отображаются на странице"""
        
        with allure.step("Open main page"):
            main_page = MainPage(driver)
            main_page.go_to_site()
        
        with allure.step("Scroll to questions section"):
            main_page.scroll_to_questions_section()
        
        with allure.step(f"Verify question {question_index + 1} is visible"):
            questions_page = QuestionsPage(driver)
            assert questions_page.is_question_visible(question_index), f"Question {question_index + 1} is not visible"
    
    @allure.feature("Questions section")
    @allure.story("Questions count verification")
    def test_questions_count(self, driver):
        """Тест проверяет, что всего 8 вопросов на странице"""
        
        with allure.step("Open main page"):
            main_page = MainPage(driver)
            main_page.go_to_site()
        
        with allure.step("Scroll to questions section"):
            main_page.scroll_to_questions_section()
        
        with allure.step("Verify questions count is 8"):
            questions_page = QuestionsPage(driver)
            questions_count = questions_page.get_all_questions_count()
            
            assert questions_count == 8, f"Expected 8 questions, but found {questions_count}"