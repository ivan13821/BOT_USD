from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router, Bot, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from config import get_tg_api_token, get_feedback_chat_id



#импорт клавиатуры
from other.other_keyboard import OtherKeyboardFactory

router = Router()

bot = Bot(token=get_tg_api_token())



@router.message(F.text == '/help')
async def help(message: types.Message, state: FSMContext):

    """ Помощь пользователю """

    await message.answer('Помоги себе сам')

