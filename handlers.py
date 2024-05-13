from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
import database, admin, keyboards
from config import ADMIN_ID, QUESTION_ID, IDEA_ID

router = Router()

class choosing_state(StatesGroup):
    expected_idea = State()
    expected_faq = State()

@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.chat.id == ADMIN_ID:
        await admin.admin_panel(msg, router)
    else:
        chat_id = int(msg.chat.id)
        database.reg(chat_id)
        await msg.answer("Привет! Я - бот помощи для членам профсоюза. Можешь посмотреть список команд в МЕНЮ слева "
                         "внизу")

@router.message(Command("promo"))
async def message_handler(msg: Message):
    document = FSInputFile(path='C:\\Users\\Алексей\\PycharmProjects\\Union\\docs\\Акции и скидки.pdf')
    await msg.answer_document(document)

@router.message(Command("payment"))
async def message_handler(msg: Message):
    document_payment = FSInputFile(path='C:\\Users\\Алексей\\PycharmProjects\\Union\\docs\\Заявление на мат.помощь.doc')
    document_terms = FSInputFile(path='C:\\Users\\Алексей\\PycharmProjects\\Union\\docs\\Порядок выплаты мат.помощи.pdf')
    await msg.answer("Тут Вы можете посмотреть порядок выплат от профсоюз ")
    await msg.answer_document(document_terms)
    await msg.answer("Вам будет необходимо заполнить заявление, подписать его и скан направить на почту: "
                     "Profsojuz_SV_Otd_7003_urb@omega.sbrf.ru (в сети omega)")
    await msg.answer_document(document_payment)

@router.message(Command("idea"))
async def message_handler(msg: Message, state: FSMContext):
    await msg.answer("Напишите свою идею, чтобы мы могли ее рассмотреть")
    await state.set_state(choosing_state.expected_idea)

@router.message(Command("help"))
async def message_handler(msg: Message):
    create_help_button = keyboards.help_keyboard()
    await msg.answer("Если у вас есть какие-то вопросы, проблемы выберите тему проблемы",
                     reply_markup=create_help_button.as_markup())
    @router.callback_query(F.data == "medical_aid")
    async def medical_aid(callback: types.CallbackQuery):
        await callback.message.answer("Напишите проблему и контакты, чтобы мы могли помочь ее решить:")
        await msg.answer("medical_aid. Сообщение отправлено")

    @router.callback_query(F.data == "legal_aid")
    async def medical_aid(callback: types.CallbackQuery):
        await callback.message.answer("Напишите проблему и контакты, чтобы мы могли помочь ее решить:")
        await msg.answer("legal_aid. Сообщение отправлено")

    @router.callback_query(F.data == "psychological_aid")
    async def medical_aid(callback: types.CallbackQuery):
        await callback.message.answer("Напишите проблему и контакты, чтобы мы могли помочь ее решить:")
        await msg.answer("psychological_aid. Сообщение отправлено")

    @router.callback_query(F.data == "financial_aid")
    async def medical_aid(callback: types.CallbackQuery):
        await callback.message.answer("Напишите проблему и контакты, чтобы мы могли помочь ее решить:")
        await msg.answer("financial_aid. Сообщение отправлено")

    @router.callback_query(F.data == "difficult_situation_aid")
    async def medical_aid(callback: types.CallbackQuery):
        await callback.message.answer("Напишите проблему и контакты, чтобы мы могли помочь ее решить:")
        await msg.answer("difficult_situation_aid. Сообщение отправлено")

    @router.callback_query(F.data == "other_questions")
    async def medical_aid(callback: types.CallbackQuery):
        await callback.message.answer("Напишите проблему и контакты, чтобы мы могли помочь ее решить:")
        await msg.answer("other_questions. Сообщение отправлено")

@router.message(Command("faq"))
async def message_handler(msg: Message):
    create_faq_button = keyboards.faq_keyboard()
    with open('faq.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    await msg.answer(text, parse_mode=ParseMode.HTML)
    await msg.answer("Вы нашли ответ на свой вопрос?", reply_markup=create_faq_button.as_markup())

@router.callback_query(F.data.startswith("bool_"))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    if action == "yes":
        await callback.message.answer("Отлично!")
    elif action == "no":
        await callback.message.answer("Очень жаль. Задайте пожалуйста свой вопрос, а я через время вернусь к Вам с "
                                      "обратной связью")
        await state.set_state(choosing_state.expected_faq)

@router.message(choosing_state.expected_idea)
async def user_idea(msg: Message):
    idea = f"Новая идея: " + msg.text
    await admin.get_question(IDEA_ID, idea)
    await msg.answer("Идея отправлена")

@router.message(choosing_state.expected_faq)
async def user_question(msg: Message):
    question = f"ID чата: " + str(msg.chat.id) + "\n" + msg.text
    await admin.get_question(QUESTION_ID, question)
    await msg.answer("Вопрос отправлен")