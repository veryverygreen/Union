from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
import database, admin, keyboards, config

router = Router()

class choosing_state(StatesGroup):
    expected_idea = State()
    expected_faq = State()
    expected_medical_aid = State()
    expected_legal_aid = State()
    expected_psychological_aid = State()
    expected_financial_aid = State()
    expected_difficult_situation_aid = State()
    expected_other_questions = State()

create_return_button = keyboards.return_keyboard()

@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.chat.id == config.ADMIN_ID:
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
    document_terms = FSInputFile(path='C:\\Users\\Алексей\\PycharmProjects\\Union\\docs\\Порядок выплаты мат.помощи'
                                      '.pdf')
    await msg.answer("Тут Вы можете посмотреть порядок выплат от профсоюз ")
    await msg.answer_document(document_terms)
    await msg.answer("Вам будет необходимо заполнить заявление, подписать его и скан направить на почту: "
                     "Profsojuz_SV_Otd_7003_urb@omega.sbrf.ru (в сети omega)")
    await msg.answer_document(document_payment)

@router.message(Command("idea"))
async def message_handler(msg: Message, state: FSMContext):
    await msg.answer("Напишите свою идею, чтобы мы могли ее рассмотреть", reply_markup=create_return_button.as_markup())
    await state.set_state(choosing_state.expected_idea)

@router.message(Command("help"))
async def message_handler(msg: Message, state: FSMContext):
    create_help_button = keyboards.help_keyboard()
    await msg.answer("Если у вас есть какие-то вопросы, проблемы выберите тему проблемы",
                     reply_markup=create_help_button.as_markup())
    @router.callback_query(F.data == "medical_aid")
    async def medical_aid(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(database.get_content(f'{callback.data.split("_")[0]}'))
        await callback.message.answer("Если ваша проблема не решена напишите нам ваш табельный номер, свою проблему"
                                      "и контакты для связи, чтобы мы могли её решить", reply_markup =
                                      create_return_button.as_markup())
        await state.set_state(choosing_state.expected_medical_aid)

    @router.callback_query(F.data == "legal_aid")
    async def legal_aid(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(database.get_content(f'{callback.data.split("_")[0]}'))
        await callback.message.answer("Если ваша проблема не решена напишите нам ваш табельный номер, свою проблему"
                                      "и контакты для связи, чтобы мы могли её решить", reply_markup =
                                      create_return_button.as_markup())
        await state.set_state(choosing_state.expected_legal_aid)

    @router.callback_query(F.data == "psychological_aid")
    async def psychological_aid(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(database.get_content(f'{callback.data.split("_")[0]}'))
        await callback.message.answer("Если ваша проблема не решена напишите нам ваш табельный номер, свою проблему"
                                      "и контакты для связи, чтобы мы могли её решить", reply_markup =
                                      create_return_button.as_markup())

    @router.callback_query(F.data == "financial_aid")
    async def financial_aid(callback: types.CallbackQuery):
        create_financial_button = keyboards.financial_keyboard()
        await callback.message.answer(database.get_content(f'{callback.data.split("_")[0]}'), reply_markup =
                                                           create_financial_button.as_markup())

        @router.callback_query(F.data == "Yes")
        async def answer_questions(callback: types.CallbackQuery):
            await callback.message.answer("Обратитесь за денежной компенсацией в профсоюз: "
                                          "https://sberfriend.sbrf.ru/sberfriend/#/application/563DB41AB53E49C9BB9C37"
                                          "B880E1A1E6 ")
        @router.callback_query(F.data == "Don't know")
        async def answer_questions(callback: types.CallbackQuery):
            await callback.message.answer("Ознакомиться с перечнем компенсации вы можете, прописав здесь команду"
                                          " /payment")

        @router.callback_query(F.data == "No")
        async def answer_questions(callback: types.CallbackQuery, state: FSMContext):
            await callback.message.answer(
                "Напишите нам ваш табельный номер, свою проблему и контакты для связи, чтобы мы "
                "могли её решить.")
            await state.set_state(choosing_state.expected_financial_aid)

    @router.callback_query(F.data == "difficult_situation_aid")
    async def difficult_situation_aid(callback: types.CallbackQuery):
        await callback.message.answer("Напишите нам ваш табельный номер, свою проблему и контакты для связи, чтобы"
                                      " мы могли её решить.", reply_markup = create_return_button.as_markup())
        await state.set_state(choosing_state.expected_difficult_situation_aid)

    @router.callback_query(F.data == "other_questions")
    async def other_questions(callback: types.CallbackQuery):
        await callback.message.answer("Напишите нам ваш табельный номер, свою проблему и контакты для связи, чтобы"
                                      " мы могли её решить.", reply_markup = create_return_button.as_markup())
        await state.set_state(choosing_state.expected_other_questions)

    @router.callback_query(F.data == "Back")
    async def answer_questions(callback: types.CallbackQuery):
        await msg.answer("Если у вас есть какие-то вопросы, проблемы выберите тему проблемы",
                         reply_markup=create_help_button.as_markup())

@router.message(Command("faq"))
async def faq(msg: Message):
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
    await admin.get_question(config.IDEA_ID, idea)
    await msg.answer("Идея отправлена")

@router.message(choosing_state.expected_faq)
async def user_question(msg: Message):
    question = f"ID чата: " + str(msg.chat.id) + "\n" + msg.text
    await admin.get_question(config.QUESTION_ID, question)
    await msg.answer("Вопрос отправлен")

@router.message(choosing_state.expected_medical_aid)
async def help(msg: Message):
    recipient = config.MEDICAL_MAIL
    await admin.send_email(msg.chat.id, msg, recipient)

@router.message(choosing_state.expected_legal_aid)
async def help(msg: Message):
    recipient = config.LEGAL_MAIL
    await admin.send_email(msg.chat.id, msg, recipient)

@router.message(choosing_state.expected_psychological_aid)
async def help(msg: Message):
    recipient = config.PSYCHOLOGICAL_MAIL
    await admin.send_email(msg.chat.id, msg, recipient)

@router.message(choosing_state.expected_financial_aid)
async def help(msg: Message):
    recipient = config.FINANCIAL_MAIL
    await admin.send_email(msg.chat.id, msg, recipient)

@router.message(choosing_state.expected_difficult_situation_aid)
async def help(msg: Message):
    recipient = config.DIFFICULT_SITUATION_MAIL
    await admin.send_email(msg.chat.id, msg, recipient)

@router.message(choosing_state.expected_other_questions)
async def help(msg: Message):
    recipient = config.OTHER_QUESTIONS_MAIL
    await admin.send_email(msg.chat.id, msg, recipient)
