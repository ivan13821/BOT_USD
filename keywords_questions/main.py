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

#импорт клавиатуры
from other.other_keyboard import OtherKeyboardFactory
from keyboard_factory.keyboard_factory_main import KeyBoardFactory

router = Router()

bot = Bot(token=get_tg_api_token())

db = Database('keywords questions')


@router.message()
async def search_keywords(message: types.Message, state:FSMContext):

    """ поиск по введенным ключевым словам """

    text = message.text

    db.answers_insert_question(question=text)

    id = db.answers_select_id_for_the_question(question=text)

    answer = EasyQuestions.generate_easy_answer(text, id_question=id)

    if answer == []:
        return await message.answer('Попробуйте перефразировать свой вопрос')
    
    #если ответ один, то отправляем просто сообщение с ответом
    if len(answer) == 1:
        answer = db.select_question_where_id(answer[0][0].split(':-)')[1].split('_')[0])[0][1]

        db.answers_update_answer_status_button_text(answer=answer, status='not rated', id=id)

        keyboard = KeyBoardFactory.create_inline_keyboard([[f'Хороший ответ:-)GoodAnswer_{id}', f'Плохой ответ:-)BadAnswer_{id}']])
        return await message.answer(answer, reply_markup=keyboard)
    
    #если возможных ответов несколько
    else:
        answer = KeyBoardFactory.create_inline_keyboard(answer)
        await message.answer('Выберете то что вам подходит больше всего:', reply_markup=answer)










@router.callback_query(StateFilter(None))
async def generate_keyboard(call: types.CallbackQuery, state: FSMContext):

    """ пользователь ходит по списку вопросов или отвечает на полезность ответа """

    key, id_question = call.data.split('_')


    #Пользователь отвечает был ли полезен ему ответ
    if "GoodAnswer" in key: #Хороший ответ

        db.answers_delete(id_question)

        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        return await call.answer("Рад был помочь, обращайтесь еще")
        
    elif "BadAnswer" in key: #Плохой ответ
        db.answers_update_status(status='bad answer', id=id_question)

        await bot.send_message(chat_id=call.message.chat.id, text="Ваш вопрос был направлен на рассмотрение, скоро вы получите на него ответ. Спасибо за ожидание")

        result = db.answer_select_all(id_question)

        bad_message = f"id вопроса: {result[0]}\n\nВопрос: {result[1]}\n\nНажатая кнопка из списка: {result[3]}\n\nОтвет: {result[2]}"
        
        await bot.send_message(get_feedback_chat_id(), bad_message)
        return await bot.delete_message(call.message.chat.id, call.message.message_id)





    #если пользователь нажал на вопрос из списка 
    func = db.select_question_where_id(key)

    answer = func[0][1]

    button_text = func[0][2]

    db.answers_update_answer_status_button_text(answer=answer, status='not rated', id=id_question, button_text=button_text)


    keyboard = KeyBoardFactory.create_inline_keyboard([[f'Хороший ответ:-)GoodAnswer_{id_question}', f'Плохой ответ:-)BadAnswer_{id_question}']])
    await bot.send_message(call.message.chat.id, answer, reply_markup=keyboard)
    await bot.delete_message(call.message.chat.id, call.message.message_id)










