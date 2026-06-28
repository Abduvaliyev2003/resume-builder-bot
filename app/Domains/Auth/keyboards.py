from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.Shared.callbacks import AuthCallback
from app.Shared.enums import AuthAction


def auth_keyboard() -> InlineKeyboardMarkup:
    """
    Authentication menu.
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔐 Login",
        callback_data=AuthCallback(
            action=AuthAction.LOGIN,
        ),
    )

    builder.button(
        text="📝 Register",
        callback_data=AuthCallback(
            action=AuthAction.REGISTER,
        ),
    )

    builder.adjust(1)

    return builder.as_markup()