import psycopg2

from database.config import get_db_params




def clean_message(message: str) -> str:
    """Очищает сообщзение от ненужных символов """

    return ''.join(list(filter(lambda x: True if x in list('1234567890 qwertyuiopasdfghjklzxcvbnm йцукенгшщзхъфывапролджэячсмитьбю@') else False, message)))

class Database:



    # подключение и создание бд ------------------------------------------------------------------------------------------
    def __init__(self, modyl_name):
        self.conn = None
        self.cur = None
        self.connect_to_db(modyl_name)

    def connect_to_db(self, modyl_name):
        params = get_db_params()
        print('Подключаюсь к PostgreSQL...')
        try:
            self.conn = psycopg2.connect(**params)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            print(f'Успешно подключен для работы с {modyl_name}')
            self.create_tables_if_they_do_not_exists()
            self.create_table_admins_if_not_exists()
            self.create_table_answers_if_not_exists()
        except Exception as error:
            print(error)




    def execute_query(self, query, params=None):
        try:
            if params is not None:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
        except psycopg2.InterfaceError as e:
            print(e)
            print("Не удалось выполнить запрос из-за ошибки подключения. Пытаюсь подключиться к базе заново")
            self.connect_to_db()
            self.cur.execute(query, params)


    def create_tables_if_they_do_not_exists(self):
        self.execute_query("""CREATE TABLE IF NOT EXISTS questions (
                                id_question serial primary key,
                                button_text text,
                                key_words text,
                                answer text
                                );""")
    

    def create_table_admins_if_not_exists(self):
        self.execute_query("""CREATE TABLE IF NOT EXISTS admins (
                                admin_chat_id bigint unique,
                                admin_status varchar(10)
                            );
                            """)
    
    def create_table_answers_if_not_exists(self):
        self.execute_query("""CREATE TABLE IF NOT EXISTS answers (
                                id_question serial primary key,
                                question text,
                                answer text,
                                button_text text,
                                status varchar(20)
                                );
                                """)
    


    #работа с бд -----------------------------------------------------------------------------------------------------------------




    def select_max_id_question(self):

        """ Возвращает максимальный по id элемент базы данных """

        self.execute_query(f"""SELECT MAX(id_question) FROM questions""")

        return self.cur.fetchall()
    





    def select_admins(self):

        """ Возвращает всех админов """

        self.execute_query(f"""SELECT * FROM admins""")

        return self.cur.fetchall()
    





    def select_admin_status(self, chat_id):

        """Возвращает статус админа по chat id"""

        self.execute_query(f"""SELECT admin_status FROM admins where admin_chat_id={chat_id}""")
        return self.cur.fetchall()







    def insert_into_admins(self, chat_id: int, status: str) -> str:

        """ Добавляет нового администратора или пользователя который может писать вопросы """

        if status not in ['editor', 'admin']:
            return "Пользователь может быть либо editor либо admin"
        
        if type(chat_id) != int:
            return "id чата должан быть int"
        
        if self.select_admin_status(chat_id) != []:
            return 'Админ с таким чатом уже существует'
        
        self.execute_query(f"""INSERT INTO admins (admin_chat_id, admin_status) values ({chat_id}, '{status}')""")

        return "Успешно"


    
    #таблица с вопросами




    def select_questions(self, start_id: int = 0, end_id: int = 100):

        self.execute_query(f"""SELECT id_question, button_text, key_words, answer FROM questions 
                           WHERE id_question BETWEEN {start_id} AND {end_id}
                           LIMIT 100""")

        return self.cur.fetchall()
    




    def select_question_where_key_words(self, key_words):

        self.execute_query(f"""SELECT key_words, answer FROM questions 
                           WHERE key_words='{key_words}'""")

        return self.cur.fetchall()
    

    def select_question_where_id(self, quest_id):

        self.execute_query(f"""SELECT key_words, answer, button_text FROM questions 
                           WHERE id_question='{quest_id}'""")

        return self.cur.fetchall()
    



    def delete_question(self, id_question):

        self.execute_query(f"""DELETE FROM questions WHERE id_question='{id_question}'""")





    
    def insert_question(self, key_words: str, answer: str) -> None:

        """ Записывает ключевые слова вопроса и ответ на него """
        
        #Проверяем тип данных, если данные не того типа то выводим ошибку, в противном случае приводим данные к нужному типу
        if type(key_words) == list:
            new_list = []
            for i in key_words:
                if type(i) == str:
                    new_list.append(i)
                else:
                    return "Вы не можете записать в ключевые слова не строку"
            key_words = ' '.join(new_list)
        
        elif type(key_words) != str:
            return "Вы не можете записать в ключевые слова не строку"

        #удаляем все ненужные символы из ключевых слов 
        clear_key_words = clean_message(key_words)

        #удаляем все ненужные символы из ответа
        clear_answer = clean_message(answer)

        self.execute_query(f"""INSERT INTO questions (key_words, answer) values ('{clear_key_words}', '{clear_answer}')""")
        return "Успешно"



    # --------  Таблица с ответами и вопросами для сбора информации ---------------------------------------------------------


    # def answers_insert_question_answer_status(self, question: str, answer: str, status: str) -> None:
    #     """Добавляет новый вопрос в таблицу вопросы + ответы """

    #     clear_answer, clear_question = clean_message(answer), clean_message(question)

    #     self.execute_query(f"""INSERT INTO answers (question, answer, status) 
    #                        values
    #                        ('{clear_question}', '{clear_answer}', '{status}')""")
    

    def answers_insert_question(self, question: str) -> None:

        """Добавляет вопрос в базу данных """

        self.execute_query(f"""INSERT INTO answers (question)
                           values
                           ('{question}')""")
    


    def answers_update_answer_status_button_text(self, answer: str, status: str, id: int, button_text: str = None) -> None:

        """ Обновляет вопрос добавляя в него ответ и статус """

        if button_text is not None:
            self.execute_query(f"""UPDATE answers
                                        SET answer='{answer}',
                                        status='{status}',
                                        button_text='{button_text}'
                                        WHERE id_question={id}""")
        else:
            self.execute_query(f"""UPDATE answers
                                        SET answer='{answer}',
                                        status='{status}'
                                        WHERE id_question={id}""")
    



    def answers_select_id_for_the_question(self, question: str) -> int:

        """ Дает id по вопросу """

        self.execute_query(f"""SELECT id_question FROM answers
                           WHERE question='{question}' 
                           LIMIT 1""")

        return self.cur.fetchall()[0][0]
    


    def answer_select_answer(self, id: int) -> str:

        """Возваращает ответ на вопрос по id """

        self.execute_query(f"""SELECT answer FROM answers
                           WHERE id_question='{id}' 
                           """)
        
        return self.cur.fetchall()[0][0]




    def answer_select_all(self, id: int) -> list:

        """Возвращает все данные по id """

        self.execute_query(f"""SELECT * FROM answers
                           WHERE id_question='{id}' 
                           """)
        
        return self.cur.fetchall()[0]

    

    def answers_update_status(self, status: str, id: int) -> None:

        """ Обновляет статус по вопросу """

        self.execute_query(f"""UPDATE answers
                                    SET status='{status}'
                                    WHERE id_question={id}""")
    


    def answers_delete(self, id: int) -> None:

        """Удаляет вопрос и ответ по заданому id"""

        self.execute_query(f"""DELETE FROM answers
                           WHERE id_question={id}""")