from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router, Bot, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup


from config import get_tg_api_token, get_feedback_chat_id


#импорт модулей проекта
from keywords_questions.easy_questions.main import EasyQuestions
from database.main import Database


#импорт клавиатуры
from other.other_keyboard import OtherKeyboardFactory
from keyboard_factory.keyboard_factory_main import KeyBoardFactory

router = Router()

bot = Bot(token=get_tg_api_token())


db = Database()









class AdminsStates(StatesGroup):

    admin_input_message_chat_id =  State()
    admin_input_chat_id_drop_admin = State()
    add_question = State()
    drop_question = State()










#
#
#Добавление админов -----------------------------------------------------------------------------------------------------------------------------------------------------------
#
#

@router.message(F.text == "/chat")
async def get_chat_id(message: types.Message, state:FSMContext):

    """Отпрвляет пользователю id чата с ботом"""

    await message.answer(str(message.chat.id))








@router.message(F.text == "/add_admin")
async def add_admin(message: types.Message, state:FSMContext):

    """ Супер админ вводит команду на добавление админа в бота """

    status = db.select_admin_status(message.chat.id)

    try:
        if status[0][0] != 'admin':
            return await message.answer("У вас недостаточно прав для совершения данной операции")
    except KeyError:
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    await message.answer("Введите пожалуйста id чата и роль (editor или admin) через запятую\nУзнать это можно с помощью команды /chat")

    await state.set_state(AdminsStates.admin_input_message_chat_id)











@router.message(AdminsStates.admin_input_message_chat_id)
async def add_admin(message: types.Message, state:FSMContext):

    """ Админ вводит чат id и роль"""

    text = message.text
    text = list(map(lambda x: x.strip(), text.split(',')))

    if len(text) != 2:
        return await message.answer("Введите пожалуйста id чата и роль (editor или admin) через запятую")
    
    if (role := text[1]) not in ['editor', 'admin']:
        return await message.answer(f"К сожалению роли {role} не существует")
    
    if not text[0].isdigit():
        return await message.answer(f"К сожалению id {text[0]} не может существовать")
    
    result = db.insert_into_admins(text[0], text[1])

    await message.answer(result)
    await state.clear()






@router.message(F.text == "/show_admins")
async def add_admin(message: types.Message, state:FSMContext):

    """Показывает чаты всех админов и их статусы"""

    admins = db.select_admins()

    result = ''

    if admins is None:
        return await message.answer("К сожалению админов не добавлено")

    for chat, status in admins:

        result += f'{chat}: {status}\n'
    

    if result == '':
        return await message.answer("К сожалению админов не добавлено")
    else:
        await message.answer(result)




















#
#
#удаление админов -----------------------------------------------------------------------------------------------------------------------------------------------------------
#
#



@router.message(F.text == "/drop_admin")
async def add_admin(message: types.Message, state:FSMContext):

    """ Удаление админа """

    status = db.select_admin_status(message.chat.id)

    try:
        if status[0][0] != 'admin':
            return await message.answer("У вас недостаточно прав для совершения данной операции")
    except KeyError:
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    await message.answer("Введите пожалуйста id чата админа\nЧтобы узнать id админов введите /show_admins")

    await state.set_state(AdminsStates.admin_input_chat_id_drop_admin)







@router.message(AdminsStates.admin_input_chat_id_drop_admin)
async def add_admin(message: types.Message, state:FSMContext):

    """ Получение id админа """

    admin_id = message.text

    if not admin_id.isdigit():
        return await message.answer("id должен состоять из цифр")
    
    status = db.select_admin_status(admin_id)

    try:
        if status[0][0] == 'admin':
            return await message.answer("Вы не можете удалить админа со статусом admin")
    except KeyError:
        return await message.answer("Такого админа не существует")
    
    await message.answer("админ удален")
    await state.clear()
    

    




#
#
#добавление вопросов -----------------------------------------------------------------------------------------------------------------------------------------------------------
#
#





@router.message(F.text == "/add_question")
async def add_admin(message: types.Message, state:FSMContext):

    """ Добавление вопроса """

    status = db.select_admin_status(message.chat.id)

    try:
        if status[0][0] not in ['admin', 'editor']:
            return await message.answer("У вас недостаточно прав для совершения данной операции")
    except KeyError:
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    await message.answer("Введите пожалуйста ключевые слова, а через знак ; введите ответ на эту комбинацию ключевых слов")

    await state.set_state(AdminsStates.add_question)







@router.message(AdminsStates.add_question)
async def add_admin(message: types.Message, state:FSMContext):

    """ Получения ключевых слов и ответа на них """

    text = list(map(lambda x: x.lower().strip(), message.text.split(';')))

    if len(text) != 2:
        return await message.answer("Введите пожалуйста ключевые слова, а через знак ; введите ответ на эту комбинацию ключевых слов")
    
    words = []
    for i in text[0]:
        if i in "йцукенгшщзхъфывапролджэячсмитьбю 1234567890":
            words.append(i)
    words = ''.join(words)
    
    answers = []
    for i in text[1]:
        if i in "йцукенгшщзхъфывапролджэячсмитьбю 1234567890":
            answers.append(i)
    answers = ''.join(answers)

    if db.select_question_where_key_words(words) == []:
        return await message.answer("Вопрос с такими ключевыми словами уже создан, попробуйте его уточнить")
        
    answer = db.insert_question(words, answers)

    await message.answer(answer)
    await state.clear()

    
    


@router.message(F.text == "/show_questions")
async def add_admin(message: types.Message, state:FSMContext):

    """ Показывает все вопросы """

    status = db.select_admin_status(message.chat.id)

    try:
        if status[0][0] not in ['admin', 'editor']:
            return await message.answer("У вас недостаточно прав для совершения данной операции")
    except KeyError:
        return await message.answer("У вас недостаточно прав для совершения данной операции")

    result = db.select_questions()

    answer = ''

    if result == []:
        return await message.answer("К сожалению вопросов еще не добавленно")

    k = 1
    for key_words, answers in result:
        answer += f"{k}) {key_words}: {answers}\n"
        k += 1
    
    await message.answer(answer)






#
#
#удаление вопросов -----------------------------------------------------------------------------------------------------------------------------------------------------------
#
#



@router.message(F.text == "/drop_question")
async def add_admin(message: types.Message, state:FSMContext):

    """ Удаление вопроса """

    status = db.select_admin_status(message.chat.id)

    try:
        if status[0][0] not in ['admin', 'editor']:
            return await message.answer("У вас недостаточно прав для совершения данной операции")
    except KeyError:
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    await message.answer("Введите пожалуйста ключевые слова вопроса")

    await state.set_state(AdminsStates.drop_question)




@router.message(AdminsStates.drop_question)
async def add_admin(message: types.Message, state:FSMContext):

    """ Удаление вопроса """

    if db.select_question_where_key_words(message.text) == []:
        return await message.answer("Вопроса с такими ключевыми словами не существует")
    
    db.delete_question(key_words=message.text)


    await message.answer("Вопрос успешно удален")
    await state.clear()









#удалить
@router.message(F.text == "/test")
async def add_admin(message: types.Message, state:FSMContext):

    print(db.insert_into_admins(message.chat.id, "admin"))




