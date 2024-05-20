import config, keyboards, database, smtplib
from aiogram.types import Message
from email.mime.text import MIMEText
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

bot = Bot(token=config.BOT_TOKEN)

class choosing_admin_state(StatesGroup):
    expected_answer = State()
    expected_image = State()
    expected_rewrite_faq = State()

def get_username (msg: types.Message):
    username = str(msg.from_user.username)
    if username != None:
        user_id=username
    else:
        name = str(msg.from_user.id)
        first_name = str(msg.from_user.first_name)
        last_name = str(msg.from_user.last_name)
        if name.isdigit() == True:
            if last_name == None:
                user_id = first_name
            else:
                user_id = first_name + last_name
        else:
            user_id = name
    return user_id

async def get_question (chat_id: int, question: str):
    await bot.send_message(chat_id=chat_id, text=question)

async def get_answer(chat_id: str, answer: str):
     await bot.send_message(chat_id=chat_id, text=answer)

async def send_email(chat_id: int, msg: Message, recipient: str):
    message = f"Пришел новый запрос:\n" + msg.text
    subject = get_username(msg)
    sender = config.EMAIL_SENDER
    password = config.EMAIL_PASSWORD
    server = smtplib.SMTP("smtp.yandex.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        mess = MIMEText(message, 'html')
        mess['From'] = sender
        mess['To'] = recipient
        mess['Subject'] = f"{subject}"
        server.sendmail(sender, recipient, mess.as_string())
        await bot.send_message(chat_id=chat_id, text="Ваша проблема принята. Мы обязательно поможем решить вашу "
                                                     "проблему в течении 5 рабочих дней")
    except Exception as _ex:
        return f"{_ex}_"

async def admin_panel(msg:Message, router: Router):
    create_admin_button = keyboards.admin_keyboard()
    await msg.answer("Перед вами панель админа (возможности будут дополняться). Выберите действие",
                     reply_markup=create_admin_button.as_markup())

    @router.callback_query(F.data == "answer_questions")
    async def answer_questions(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Укажите ID чата и в новой строке ответ (также как приходят вопросы):")
        await state.set_state(choosing_admin_state.expected_answer)

    @router.callback_query(F.data == "create_post")
    async def create_post(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Выберете фото для отправки и в описании напишите текст поста:")
        await state.set_state(choosing_admin_state.expected_image)

    @router.callback_query(F.data == "rewrite_faq")
    async def create_post(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Сейчас раздел выглдяит следующим образом:")
        with open('faq.txt', 'r', encoding='cp1251') as f:
            text = f.read()
        await msg.answer(text)
        await msg.answer(
            "Старый не сохранится, если нужно его дополнить - то в сообщении пропишите и его. Отправьте "
            "новый текст:")
        await state.set_state(choosing_admin_state.expected_rewrite_faq)

    @router.message(choosing_admin_state.expected_answer)
    async def read_id(msg: Message):
        query_answer = msg.text.split(f"\n")
        chat_id = query_answer[0]
        answer = query_answer[1]
        admin_answer = "Ответ на Ваш вопрос: " + answer
        await get_answer(chat_id, admin_answer)

    @router.message(choosing_admin_state.expected_image)
    async def user_question(msg: Message, bot: Bot):
        users_list = database.get_users()
        for user_id in users_list:
            try:
                await bot.send_photo(user_id, msg.photo[-1].file_id, caption=msg.caption)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

    @router.message(choosing_admin_state.expected_rewrite_faq)
    async def rewrite_faq(msg: Message):
        with open('faq.txt', 'w', encoding='cp1251') as f:
            f.write(msg.text)
        await msg.answer("Текст обновлен")