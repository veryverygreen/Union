import config, database
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

async def get_question (chat_id: int, question:str):
    await bot.send_message(chat_id=chat_id, text=question)

async def get_answer(chat_id: str, answer:str):
     await bot.send_message(chat_id=chat_id, text=answer)

def admin_keyboard():
    create_post_button = InlineKeyboardBuilder()
    create_post_button.add(types.InlineKeyboardButton(text="Создать пост", callback_data="create_post"),
                           types.InlineKeyboardButton(text="Ответить на вопрос", callback_data="answer_questions"),
                           types.InlineKeyboardButton(text="Поменять раздел FAQ", callback_data="rewrite_faq"))
    return create_post_button
