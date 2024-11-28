from questions.main_questions import questions, end_func
from keyboard_factory.keyboard_factory_main import KeyBoardFactory

from Levenshtein import ratio








class EasyQuestions:

    @staticmethod
    def generate_easy_answer(text: str):

        """
        Генерирует ответ на основе введеных ключевых слов 
        Ответ отправляем в формате keyboard
        """

        text = EasyQuestions.clear_answer(text)

        answers = {}


        #ищем кореляцию между вопросом юзера и вопросом с коментарием в системе
        for i in end_func.items():
            key, value = i
            func, question = value

            #если между вопросом пользователя и вопросом в системе полное совпадение, то отправляем ответ сразу
            if EasyQuestions.complete_coincidence(text, question): 
                #return [KeyBoardFactory.create_inline_keyboard([[f"{question}:-){key}"]])]
                return [[f"{question}:-){key}"]]
            

            #Если совпадение слов в пердложении больше 0 то добавлем это в ответ
            let = EasyQuestions.partial_match(question, text)
            if let >= 1:
                answers[f"{question}:-){key}"] = let
            
        

        #Ищем элементы с максимальной кореляцией
        result = []
        maxi = 0
        for i in answers.keys():
            if answers[i] > maxi:
                result = []
                maxi = answers[i]
                result.append([i])
            
            elif answers[i] == maxi:
                result.append([i])
        

        return result





    @staticmethod
    def clear_answer(text: str) -> str:

        """Очищает вопрос от ненужных символов """
        text = text.lower()

        answer = ''

        for i in text:
            if i in '1234567 890йцукенгшщзхъфывапролджэячсмитьбю':
                answer += i
        
        return answer


        

        





    # @staticmethod
    # def find_path(text) -> list:

    #     """ Ищет путь по массиву для генерации ответа на основе содержащихся в нем данных на все уровни """

    #     keys = []

    #     while True:

    #         if len(keys) > 0:
    #             for i in keys:
    #                 if type(i) == dict:
    #                     break
    #             else:
    #                 return keys
            

            
    # @staticmethod
    # def get_end_dict(mass, key:str):

    #     """ возвращает конечный список по ключу """

    #     keys = key.split('/')
    #     level = 0

    #     if not key:
    #         return mass

    #     while True:
    #         for i in mass.keys():
    #             if keys[level] in i[1]:
    #                 mass = mass[i]
    #                 level += 1
    #                 break
    #         if level == len(keys):
    #             break

    #     return mass




    



    # @staticmethod
    # def find_best_path(last_path: str, user_text) -> str:

    #     """ ищет лучший путь/пути в массиве на 1 уровень """

    #     end_dict = EasyQuestions.get_end_dict(questions, last_path)

    #     summ = {}

    #     #Создаем массив заполненый значениями максимально похожих элементов группы поиска  
    #     for key in end_dict.keys():
    #         text, comment = key[0], key[2]
    #         comment = comment.split(', ')

    #         if EasyQuestions.complete_coincidence(text, user_text): 
    #             last_path += f"/{key[1]}"
    #             return last_path

    #         maxi = 0
            
    #         summ_text = EasyQuestions.partial_match(text, user_text)
    #         if maxi < summ_text:
    #             maxi = summ_text
            
    #         for i in comment:
    #             let = EasyQuestions.partial_match(i, user_text)
    #             if let > maxi:
    #                 maxi = let
            
    #         summ[key] = maxi
        
    #     #Создаем ответ на основе похожести элементов 
    #     answer = []
    #     maxi = 0

    #     for i in summ.items():
    #         if i[1] > maxi:
    #             maxi = i[1]
    #             answer = []
    #             answer.append(i[0][1])

    #         elif i[1] == maxi:
    #             answer.append(i[0][1])
        

        
    #     if maxi == 0:
    #         return None

    #     return answer
            





            







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








