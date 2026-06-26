from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def templates_keyboard(templates):

    keyboard = []

    for template in templates:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=template["name"],
                    callback_data=f"template:{template['id']}",
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )