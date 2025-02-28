from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router, Bot, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Filter

from config import get_tg_api_token, get_feedback_chat_id
from database.main import Database


#импорт клавиатуры
from other.other_keyboard import OtherKeyboardFactory

router = Router()

bot = Bot(token=get_tg_api_token())

db = Database()






#================================================= Получение и запись номера телефона пользователя =====================================================================


#Создание фильтра для остановки незарегистрированных пользователей
class MyFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        return db.has_number(message.chat.id)





@router.message(F.contact)
async def contacts(message: types.Message, state: FSMContext):

    """Получаем номер пользователя и записываем его в бд """

    db.insert_phone(message.contact.phone_number, message.chat.id)

    await message.answer(f"Теперь ты можешь пользоваться ботом!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()



@router.message(MyFilter())
async def help(message: types.Message, state: FSMContext):

    """Проверяем зарегистрирован ли пользователь"""

    await message.answer("Сначала вам нужно зарегистрироваться!\nДля авторизации мне нужен ваш номер телефона", reply_markup=OtherKeyboardFactory.get_phone())





#======================================== commands ============================================================================





