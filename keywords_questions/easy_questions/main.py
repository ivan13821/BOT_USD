from questions.main_questions import questions











class EasyQuestions:

    @staticmethod
    def generate_easy_answer():

        """ Генерирует ответ на основе введеных ключевых слов """

        keys = []

        

        





    @staticmethod
    def find_path(text) -> list:

        """ Ищет путь по массиву для генерации ответа на основе содержащихся в нем данных на все уровни """

        keys = []

        while True:

            if len(keys) > 0:
                for i in keys:
                    if type(i) == dict:
                        break
                else:
                    return keys
            

            
    @staticmethod
    def get_end_dict(mass, key:str):

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
    def find_best_path(last_path: str, user_text) -> str:

        """ ищет лучший путь/пути в массиве на 1 уровень """

        end_dict = EasyQuestions.get_end_dict(questions, last_path)

        summ = {}

        #Создаем массив заполненый значениями максимально похожих элементов группы поиска  
        for key in end_dict.keys():
            text, comment = key[0], key[2]
            comment = comment.split(', ')

            if EasyQuestions.complete_coincidence(text, user_text): 
                last_path += f"/{key[1]}"
                return last_path

            maxi = 0
            
            summ_text = EasyQuestions.partial_match(text, user_text)
            if maxi < summ_text:
                maxi = summ_text
            
            for i in comment:
                let = EasyQuestions.partial_match(i, user_text)
                if let > maxi:
                    maxi = let
            
            summ[key] = maxi
        
        #Создаем ответ на основе похожести элементов 
        answer = []
        maxi = 0

        for i in summ.items():
            if i[1] > maxi:
                maxi = i[1]
                answer = []
                answer.append(i[0][1])

            elif i[1] == maxi:
                answer.append(i[0][1])
        

        
        if maxi == 0:
            return None

        return answer
            





            







    @staticmethod
    def complete_coincidence(text1: str, text2: str) -> bool:

        """ Проверяет строки на полное совпадение их слов """

        text1, text2 = list(map(lambda x: x.strip(), text1.lower().split(' '))), list(map(lambda x: x.strip(), text2.lower().split(' ')))

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
                if i == j:
                    maxi += 1
                    break
        
        return maxi


print(EasyQuestions.find_best_path("references", "справка"))





