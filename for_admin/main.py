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



@router.message(F.text == "/add_admin")
async def add_admin(message: types.Message, state:FSMContext):

    """ функция добавляет нового админа """

    admins = db.select_admins()

    for i in admins:
        if i[0] == message.chat.id and i[1] == 'admin':
            break
    else:
        return await message.answer('У вас недостаточно прав для добавления нового админа')

    

    await message.answer('Выберете то что вам подходит больше всего:')






@router.message(F.text == "/chat")
async def add_admin(message: types.Message, state:FSMContext):

    """Отпрвляет пользователю id чата с ботом"""

    await message.answer(str(message.chat.id))
















