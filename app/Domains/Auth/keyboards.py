from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def auth_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔐 Login",
                    callback_data="login",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Register",
                    callback_data="register",
                )
            ]
        ]
    )