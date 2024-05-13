from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def help_keyboard():
    create_help_button = InlineKeyboardBuilder()
    create_help_button.row(types.InlineKeyboardButton(text="Медицинская помощь", callback_data="medical_aid"))
    create_help_button.row(types.InlineKeyboardButton(text="Юридическая помощь", callback_data="legal_aid"))
    create_help_button.row(types.InlineKeyboardButton(text="Психологическая помощь", callback_data="psychological_aid"))
    create_help_button.row(types.InlineKeyboardButton(text="Финансовая помощь", callback_data="financial_aid"))
    create_help_button.row(types.InlineKeyboardButton(text="Помощь в сложной жизненной ситуации",
                                                      callback_data="difficult_situation_aid"))
    create_help_button.row(types.InlineKeyboardButton(text="Другой вопрос", callback_data="other_questions"))
    return create_help_button

def faq_keyboard():
    create_faq_button = InlineKeyboardBuilder()
    create_faq_button.add(types.InlineKeyboardButton(text="Да", callback_data="bool_yes"),
                           types.InlineKeyboardButton(text="Нет", callback_data="bool_no"))
    return create_faq_button

def admin_keyboard():
    create_post_button = InlineKeyboardBuilder()
    create_post_button.row(types.InlineKeyboardButton(text="Создать пост", callback_data="create_post"))
    create_post_button.row(types.InlineKeyboardButton(text="Ответить на вопрос", callback_data="answer_questions"))
    create_post_button.row(types.InlineKeyboardButton(text="Поменять раздел FAQ", callback_data="rewrite_faq"))
    return create_post_button