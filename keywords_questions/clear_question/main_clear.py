



class Clear:

    """ Очищает вопрос от ненужных символов """

    @staticmethod
    def clear(string):

        """ Оставляет только буквы и цифры """

        clear_string = []

        for i in string:

            if i in list('qwertyuiopasdfghjklzxcvbnm 1234567890 йцукенгшщзхъфывапролджэячсмитьбю'):
                clear_string.append(i)

        return ''.join(string)