from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
import database
import admin
from config import ADMIN_ID, QUESTION_ID, IDEA_ID

router = Router()

class choosing_state(StatesGroup):
    expected_answer = State()
    expected_idea = State()
    expected_faq = State()
    expected_image = State()
    expected_rewrite_faq = State()

@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.chat.id == ADMIN_ID:
        create_post_button = admin.admin_keyboard()
        await msg.answer("Перед вами панель админа (возможности будут дополняться). Выберите действие",
             reply_markup=create_post_button.as_markup())

        @router.callback_query(F.data =="answer_questions")
        async def answer_questions (callback: types.CallbackQuery, state:FSMContext):
            await callback.message.answer("Укажите ID чата и в новой строке ответ (также как приходят вопросы):")
            await state.set_state(choosing_state.expected_answer)

        @router.callback_query(F.data =="create_post")
        async def create_post (callback: types.CallbackQuery, state: FSMContext):
            await callback.message.answer("Выберете фото для отправки и в описании напишите текст поста:")
            await state.set_state(choosing_state.expected_image)

        @router.callback_query(F.data == "rewrite_faq")
        async def create_post(callback: types.CallbackQuery, state: FSMContext):
            await callback.message.answer("Сейчас раздел выглдяит следующим образом:")
            with open('faq.txt', 'r', encoding='cp1251') as f:
                text = f.read()
            await msg.answer(text)
            await msg.answer(
                "Старый не сохранится, если нужно его дополнить - то в сообщении пропишите и его. Отправьте "
                "новый текст:")
            await state.set_state(choosing_state.expected_rewrite_faq)
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

@router.message(Command("faq"))
async def message_handler(msg: Message):
    def create_keyboard():
        buttons = [
            [
                types.InlineKeyboardButton(text="Да", callback_data="bool_yes"),
                types.InlineKeyboardButton(text="Нет", callback_data="bool_no")
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
    with open('faq.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    await msg.answer(text, parse_mode=ParseMode.HTML)
    await msg.answer("Вы нашли ответ на свой вопрос?", reply_markup=create_keyboard())
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

@router.message(choosing_state.expected_answer)
async def read_id(msg: Message):
    query_answer = msg.text.split(f"\n")
    chat_id = query_answer[0]
    answer = query_answer[1]
    admin_answer = "Ответ на Ваш вопрос: " + answer
    await admin.get_answer(chat_id, admin_answer)

@router.message(choosing_state.expected_image)
async def user_question(msg: Message, bot: Bot):
    users_list = database.get_users()
    for user_id in users_list:
        try:
            await bot.send_photo(user_id, msg.photo[-1].file_id, caption=msg.caption)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

@router.message(choosing_state.expected_rewrite_faq)
async def rewrite_faq(msg: Message):
    with open('faq.txt', 'w', encoding='cp1251') as f:
        f.write(msg.text)
    await msg.answer("Текст обновлен")
