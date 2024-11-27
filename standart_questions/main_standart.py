from codecs import replace_errors

from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router, Bot, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import get_tg_api_token, get_feedback_chat_id
from questions.class_question import Questions

#импорт модулей проекта
from questions.questions_keyboards import KeyboardQuestions
from questions.main_questions import questions

router = Router()

bot = Bot(token=get_tg_api_token())







@router.message(F.text == "/start")
async def start(message: types.Message, state: FSMContext):

    """ начинает опрос пользователя """

    reply_markup = KeyboardQuestions.generate_keyboard(key='')

    await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=reply_markup)






@router.callback_query(StateFilter(None))
async def generate_keyboard(call: types.CallbackQuery, state: FSMContext):

    """ пользователь ходит по списку вопросов """

    key = call.data

    func = KeyboardQuestions.is_it_func(key)



    reply_markup = KeyboardQuestions.generate_keyboard(key=key)

    if not func:
        await bot.send_message(call.message.chat.id ,'Выберите действие:', reply_markup=reply_markup)
    else:
        answer = func()
        await bot.send_message(call.message.chat.id, answer, reply_markup=reply_markup)

    await bot.delete_message(call.message.chat.id, call.message.message_id)























