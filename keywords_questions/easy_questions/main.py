# from questions.main_questions import questions, end_func
from keyboard_factory.keyboard_factory_main import KeyBoardFactory
from database.main import Database

from Levenshtein import ratio



db = Database()




class EasyQuestions:

    @staticmethod
    def generate_easy_answer(text: str, id_question: str = None):

        """
        Генерирует ответ на основе введеных ключевых слов 
        Ответ отправляем в формате keyboard
        """

        text = EasyQuestions.clear_answer(text)

        #ограничения id
        start = 0
        end = 100
        need = db.select_max_id_question()[0][0]

        #для ответов 
        result = {}
        maxi = 1

        while True:

            questions = db.select_questions(start_id=start, end_id=end)

            if questions == []:
                break

            for id, button_text, key_words, answer in questions:
                if EasyQuestions.complete_coincidence(text, key_words): 
                    return [[f"{button_text}:-){id}"]]
                

                let = EasyQuestions.partial_match(key_words, text)


                if let > maxi:
                    result = {}
                    result[f"{button_text}:-){id}_{id_question}"] = let
                    maxi = let
                elif let >= maxi:
                    result[f"{button_text}:-){id}_{id_question}"] = let

            

            if end > need:
                break
            else:
                start += 100
                end += 100
        
        answer = list(map(lambda x: [x], list(result.keys())))
        return answer





    @staticmethod
    def clear_answer(text: str) -> str:

        """Очищает вопрос от ненужных символов """
        text = text.lower()

        answer = ''

        for i in text:
            if i in '1234567 890йцукенгшщзхъфывапролджэячсмитьбю':
                answer += i
        
        return answer
            





            







    @staticmethod
    def complete_coincidence(text1: str, text2: str) -> bool:

        """ Проверяет строки на полное совпадение их слов """

        text1, text2 = list(map(lambda x: x.strip(), text1.lower().split(' '))), list(map(lambda x: x.strip(), text2.lower().split(' ')))

        if len(text1) != len(text2): return False

        for i in text1:
            for j in text2:
                if i == j:
                    break
            else:
                return False
        
        return True











    @staticmethod
    def partial_match(text1: str, text2: str) -> int:
        
        """ Считает сумму совпавших слов """

        text1, text2 = list(map(lambda x: x.strip(), text1.lower().split(' '))), list(map(lambda x: x.strip(), text2.lower().split(' ')))
        maxi = 0

        for i in text1:
            for j in text2:
                if ratio(i, j) > 0.7:
                    maxi += 1
                    break
        
        return maxi








