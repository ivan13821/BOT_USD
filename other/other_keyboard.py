from keyboard_factory.keyboard_factory_main import KeyBoardFactory
from aiogram import types


class OtherKeyboardFactory:

    """ Клавиатура для разных вещей не входящи в основной функционал """

    


    @staticmethod
    def get_phone():

        keyboard =[[types.KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]]

        return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)