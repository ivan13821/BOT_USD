from keyboard_factory.keyboard_factory_main import KeyBoardFactory






class ForAdminKeyboard:

    """ клавиатура для админов """


    @staticmethod
    def back():
        return KeyBoardFactory.create_reply_keyboard([
            ["Назад"]
        ])