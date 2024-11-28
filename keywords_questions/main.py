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

#импорт клавиатуры
from other.other_keyboard import OtherKeyboardFactory
from keyboard_factory.keyboard_factory_main import KeyBoardFactory

router = Router()

bot = Bot(token=get_tg_api_token())






@router.message()
async def search_keywords(message: types.Message, state:FSMContext):

    """ поиск по введенным ключевым словам """

    text = message.text

    answer = EasyQuestions.generate_easy_answer(text)

    if answer == []:
        return await message.answer('Попробуйте перефразировать свой вопрос')

    answer = KeyBoardFactory.create_inline_keyboard(answer)

    await message.answer('Выберете то что вам подходит больше всего:', reply_markup=answer)























