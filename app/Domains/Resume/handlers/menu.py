from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.Domains.Resume.keyboards import resume_menu_keyboard

router = Router(name="resume_menu")


@router.message(Command("resume"))
async def resume_menu(message: Message) -> None:
    """
    Open resume menu.
    """

    await message.answer(
        text=(
            "📄 <b>Resume Builder</b>\n\n"
            "Choose one of the actions below."
        ),
        reply_markup=resume_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == "resume:menu")
async def resume_menu_callback(
    callback: CallbackQuery,
) -> None:
    """
    Open resume menu from callback.
    """

    await callback.message.edit_text(
        text=(
            "📄 <b>Resume Builder</b>\n\n"
            "Choose one of the actions below."
        ),
        reply_markup=resume_menu_keyboard(),
        parse_mode="HTML",
    )

    await callback.answer()