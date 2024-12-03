from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router, Bot, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove


from config import get_tg_api_token, get_feedback_chat_id


#импорт модулей проекта
from keywords_questions.easy_questions.main import EasyQuestions
from database.main import Database
from for_admin.keyboards import ForAdminKeyboard

#импорт клавиатуры
from other.other_keyboard import OtherKeyboardFactory
from keyboard_factory.keyboard_factory_main import KeyBoardFactory

router = Router()

bot = Bot(token=get_tg_api_token())


db = Database('admins')









class AdminsStates(StatesGroup):

    admin_input_message_chat_id =  State()
    admin_input_chat_id_drop_admin = State()
    add_question = State()
    drop_question = State()
    update_question = State()










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

    if status == []:
        return await message.answer("У вас недостаточно прав для совершения данной операции")
    
    if status[0][0] != 'admin':
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    await message.answer("Введите пожалуйста id чата и роль (editor или admin) через запятую\nУзнать это можно с помощью команды /chat", reply_markup=ForAdminKeyboard.back())

    await state.set_state(AdminsStates.admin_input_message_chat_id)











@router.message(AdminsStates.admin_input_message_chat_id)
async def add_admin(message: types.Message, state:FSMContext):

    """ Админ вводит чат id и роль"""

    if message.text == 'Назад': 
        await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())
        return await state.clear()

    text = message.text
    text = list(map(lambda x: x.strip(), text.split(',')))

    if len(text) != 2:
        return await message.answer("Введите пожалуйста id чата и роль (editor или admin) через запятую")
    
    if (role := text[1]) not in ['editor', 'admin']:
        return await message.answer(f"К сожалению роли {role} не существует")
    
    if not text[0].isdigit():
        return await message.answer(f"К сожалению id {text[0]} не может существовать")
    
    result = db.insert_into_admins(int(text[0]), text[1])


    await message.answer(result, reply_markup=ReplyKeyboardRemove())
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

    if status != []:
        return await message.answer("У вас недостаточно прав для совершения данной операции")
    
    if status[0][0] != 'admin':
        return await message.answer("У вас недостаточно прав для совершения данной операции")



    await message.answer("Введите пожалуйста id чата админа\nЧтобы узнать id админов введите /show_admins", reply_markup=ForAdminKeyboard.back())

    await state.set_state(AdminsStates.admin_input_chat_id_drop_admin)







@router.message(AdminsStates.admin_input_chat_id_drop_admin)
async def add_admin(message: types.Message, state:FSMContext):

    """ Получение id админа """

    if message.text == 'Назад': 
        await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())
        return await state.clear()

    admin_id = message.text

    if not admin_id.isdigit():
        return await message.answer("id должен состоять из цифр")
    
    status = db.select_admin_status(admin_id)

    try:
        if status[0][0] == 'admin':
            return await message.answer("Вы не можете удалить админа со статусом admin")
    except KeyError:
        return await message.answer("Такого админа не существует")
    
    await message.answer("админ удален", reply_markup=ReplyKeyboardRemove())
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

    if status == []:
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    await message.answer("Введите пожалуйста ключевые слова, а через знак ; введите ответ на эту комбинацию ключевых слов", reply_markup=ForAdminKeyboard.back())

    await state.set_state(AdminsStates.add_question)







@router.message(AdminsStates.add_question)
async def add_admin(message: types.Message, state:FSMContext):

    """ Получения ключевых слов и ответа на них """

    text = list(map(lambda x: x.lower().strip(), message.text.split(';')))

    if message.text == 'Назад': 
        await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())
        return await state.clear()
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

    if (x:=db.select_question_where_key_words(words)) != []:
        return await message.answer("Вопрос с такими ключевыми словами уже создан, попробуйте его уточнить")
        
    answer = db.insert_question(words, answers)

    await message.answer(answer, reply_markup=ReplyKeyboardRemove())
    await state.clear()

    
    


@router.message(F.text == "/show_questions")
async def add_admin(message: types.Message, state:FSMContext):

    """ Показывает все вопросы """

    status = db.select_admin_status(message.chat.id)

    if status == []:
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    result = db.select_questions()

    answer = ''

    if result == []:
        return await message.answer("К сожалению вопросов еще не добавленно")


    for quest_id, key_words, answers in result:
        answer += f"{quest_id}) {key_words}: {answers}\n"

    
    await message.answer(answer)



#
#
#обновление вопросов ------------------------------------------------------------------------------------------------------------------------------------------------------
#
#







@router.message(F.text == "/update_question")
async def add_admin(message: types.Message, state:FSMContext):

    """ Обновление вопроса """

    status = db.select_admin_status(message.chat.id)

    if status == []:
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    await message.answer("Введите пожалуйста id вопроса", reply_markup=ForAdminKeyboard.back())

    await state.set_state(AdminsStates.update_question)









@router.message(AdminsStates.update_question)
async def add_admin(message: types.Message, state:FSMContext):

    """ Удаление вопроса """

    if message.text == 'Назад': 
        await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())
        return await state.clear()

    if db.select_question_where_id(message.text) == []:
        return await message.answer("Вопроса с такими ключевыми словами не существует")
    
    db.delete_question(id_question=message.text)


    await message.answer("Введите пожалуйста ключевые слова, а через знак ; введите ответ на эту комбинацию ключевых слов")

    await state.set_state(AdminsStates.add_question)











#
#
#удаление вопросов -----------------------------------------------------------------------------------------------------------------------------------------------------------
#
#



@router.message(F.text == "/drop_question")
async def add_admin(message: types.Message, state:FSMContext):

    """ Удаление вопроса """

    status = db.select_admin_status(message.chat.id)

    if status == []:
        return await message.answer("У вас недостаточно прав для совершения данной операции")


    await message.answer("Введите пожалуйста id вопроса", reply_markup=ForAdminKeyboard.back())

    await state.set_state(AdminsStates.drop_question)




@router.message(AdminsStates.drop_question)
async def add_admin(message: types.Message, state:FSMContext):

    """ Удаление вопроса """

    if message.text == 'Назад': 
        await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())
        return await state.clear()

    if not message.text.isdigit():
        return await message.answer("id должен состоять из цифр")

    if db.select_question_where_id(message.text) == []:
        return await message.answer("Вопроса с такими ключевыми словами не существует")
    
    db.delete_question(id_question=message.text)


    await message.answer("Вопрос успешно удален", reply_markup=ReplyKeyboardRemove())
    await state.clear()














# other ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





@router.message(F.text == "/q")
async def add_admin(message: types.Message, state:FSMContext):

    """ Показать команды связанные с вопросами """

    status = db.select_admin_status(message.chat.id)

    if status == []:
        return await message.answer("У вас недостаточно прав для совершения данной операции")

    question_command = ["/show_questions - показать вопросы", "/add_question - добавить вопрос", "/update_question - обновить вопрос", "/drop_question - удалить вопрос"]

    answer = '\n\n'.join(question_command)

    await message.answer(answer)









@router.message(F.text == "/a")
async def add_admin(message: types.Message, state:FSMContext):

    """ Показать команды связанные с админами """

    status = db.select_admin_status(message.chat.id)

    if status == []:
        return await message.answer("У вас недостаточно прав для совершения данной операции")

    question_command = ["/chat - показать id", "/show_admins - показать админов", "/add_admin - добавить админа", "/drop_admin - удалить админа"]

    answer = '\n\n'.join(question_command)

    await message.answer(answer)