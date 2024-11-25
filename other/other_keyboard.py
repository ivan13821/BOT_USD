from keyboard_factory.keyboard_factory_main import KeyBoardFactory



class OtherKeyboardFactory:

    """ Клавиатура для разных вещей не входящи в основной функционал """

    pass
    











    #Помощь ---------------------------------------------------------------------------------------------------

    @staticmethod
    def help():

        """ Помощь пользователям """

        return KeyBoardFactory.create_inline_keyboard([
            ["Продажа, обмен или покупка ресурсов:-)help_bye_cold_swep"],
            ["Кредит:-)help_with_credit"],
            ["Уровень производства:-)help_with_level"]
        ])
    







    #Правила игры --------------------------------------------------------------------------------------------------

    @staticmethod
    def rules():

        """ Дополнительное объяснение правил игры """

        return KeyBoardFactory.create_inline_keyboard([
            ["Торговля:-)rules_bye_cold_swep"],
            ["Кредит:-)rules_with_credit"],
            ["Уровень производства:-)rules_with_level"],
            ["Объединения:-)rules_group"]
        ])