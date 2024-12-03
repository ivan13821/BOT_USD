import psycopg2

from database.config import get_db_params

class Database:



    # подключение и создание бд ------------------------------------------------------------------------------------------
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect_to_db()

    def connect_to_db(self):
        params = get_db_params()
        print('Подключаюсь к PostgreSQL...')
        try:
            self.conn = psycopg2.connect(**params)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            print('Успешно подключен к PostgreSQL!')
            self.create_tables_if_they_do_not_exists()
            self.create_table_admins_if_not_exists()
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
                                key_words VARCHAR(100),
                                answer VARCHAR(500)
                                );""")
    

    def create_table_admins_if_not_exists(self):
        self.execute_query("""CREATE TABLE IF NOT EXISTS admins (
                                admin_chat_id bigint unique,
                                admin_status varchar(10)
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

        self.execute_query(f"""SELECT id_question, key_words, answer FROM questions 
                           WHERE id_question BETWEEN {start_id} AND {end_id}
                           LIMIT 100""")

        return self.cur.fetchall()
    




    def select_question_where_key_words(self, key_words):

        self.execute_query(f"""SELECT key_words, answer FROM questions 
                           WHERE key_words='{key_words}'""")

        return self.cur.fetchall()
    

    def select_question_where_id(self, quest_id):

        self.execute_query(f"""SELECT key_words, answer FROM questions 
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
        clear_key_words = ''
        for i in key_words:
            if i in list('1234567890 йцукенгшщзщхъфывапролджэячсмитьбю'):
                clear_key_words += i

        #удаляем все ненужные символы из ответа
        clear_answer = ''
        for i in answer:
            if i in list('1234567890 йцукенгшщзщхъфывапролджэячсмитьбю'):
                clear_answer += i

        self.execute_query(f"""INSERT INTO questions (key_words, answer) values ('{clear_key_words}', '{clear_answer}')""")
        return "Успешно"



        