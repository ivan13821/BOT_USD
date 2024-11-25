from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router, Bot, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import get_tg_api_token, get_feedback_chat_id

#импорт модулей проекта
from clear_question.main_clear import Clear

#импорт клавиатуры
from other.other_keyboard import OtherKeyboardFactory
from questions.main_questions import Questions

router = Router()

bot = Bot(token=get_tg_api_token())






@router.message()
async def search_keywords(message: types.Message, state:FSMContext):

    """ поиск по введенным ключевым словам """

    text = Clear.clear(message.text)

    answer = Questions.genereta_answer(text)

    await message.answer(answer)























