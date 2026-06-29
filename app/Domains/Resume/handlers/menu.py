from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.Domains.Resume.keyboards import resume_menu_keyboard
from app.Shared.callbacks import ResumeCallback
from app.Shared.enums import ResumeAction

router = Router(name="resume_menu")


@router.message(Command("menu", "resume"))
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


@router.callback_query(
    ResumeCallback.filter(
        F.action == ResumeAction.MENU,
    )
)
async def resume_menu_callback(
    callback: CallbackQuery,
    callback_data: ResumeCallback,
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
