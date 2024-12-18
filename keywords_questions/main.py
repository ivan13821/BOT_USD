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

db = Database()


@router.message()
async def search_keywords(message: types.Message, state:FSMContext):

    """ поиск по введенным ключевым словам """

    text = message.text

    answer = EasyQuestions.generate_easy_answer(text)

    if answer == []:
        return await message.answer('Попробуйте перефразировать свой вопрос')

    answer = KeyBoardFactory.create_inline_keyboard(answer)

    await message.answer('Выберете то что вам подходит больше всего:', reply_markup=answer)










@router.callback_query(StateFilter(None))
async def generate_keyboard(call: types.CallbackQuery, state: FSMContext):

    """ пользователь ходит по списку вопросов """

    key = call.data

    func = db.select_question_where_id(key)



    answer = func[0][1]
    await bot.send_message(call.message.chat.id, answer)

    await bot.delete_message(call.message.chat.id, call.message.message_id)










