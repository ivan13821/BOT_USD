from aiogram.types import ReplyKeyboardRemove

from keyboard_factory.keyboard_factory_main import KeyBoardFactory
from questions.class_question import Questions
from questions.main_questions import questions

class KeyboardQuestions:

    """ Клавиатуры для взаимодействия с вопросами"""

    @staticmethod
    def get_end_dict(mass, key):

        """ возвращает конечный список по ключу """

        keys = key.split('/')
        level = 0

        if not key:
            return mass

        while True:
            for i in mass.keys():
                if keys[level] in i[1]:
                    mass = mass[i]
                    level += 1
                    break
            if level == len(keys):
                break

        return mass




    @staticmethod
    def generate_keyboard(key):

        """ Генерирует список на основе массива по ключу """

        mass = KeyboardQuestions.get_end_dict(questions, key)

        keyboard = []

        if type(mass) != dict:
            return ReplyKeyboardRemove()

        for i in mass.keys():
            keyboard.append([f"{i[0]}:-){i[1]}"])

        if not keyboard:
            return None

        return KeyBoardFactory.create_inline_keyboard(keyboard)




    @staticmethod
    def is_it_func(key):

        """ Проверяет является ли конечное значение функцией или нет """

        mass = KeyboardQuestions.get_end_dict(questions, key)

        if type(mass) == dict:
            return False
        else:
            return mass

