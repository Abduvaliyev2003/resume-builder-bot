from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.Domains.Resume.keyboards import (
    delete_confirmation_keyboard,
)
from app.Domains.Resume.service import (
    resume_service,
)

router = Router(name="resume.delete")


@router.callback_query(
    F.data.startswith("resume:delete:")
)
async def delete_resume(
    callback: CallbackQuery,
):
    """
    Ask confirmation before deleting resume.
    """

    resume_id = callback.data.split(":")[2]

    await callback.message.edit_text(
        text=(
            "⚠️ <b>Delete Resume</b>\n\n"
            "Are you sure you want to delete this resume?"
        ),
        reply_markup=delete_confirmation_keyboard(
            resume_id,
        ),
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("resume:confirm_delete:")
)
async def confirm_delete(
    callback: CallbackQuery,
):
    """
    Delete selected resume.
    """

    resume_id = callback.data.split(":")[2]

    await resume_service.delete_resume(
        telegram_id=callback.from_user.id,
        resume_id=resume_id,
    )

    await callback.message.edit_text(
        "✅ Resume deleted successfully."
    )

    await callback.answer()