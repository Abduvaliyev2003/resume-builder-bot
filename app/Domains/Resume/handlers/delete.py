from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.Domains.Resume.keyboards import (
    delete_confirmation_keyboard,
)
from app.Domains.Resume.service import (
    resume_service,
)
from app.Shared.callbacks import ResumeCallback
from app.Shared.enums import ResumeAction

router = Router(name="resume.delete")


@router.callback_query(
    ResumeCallback.filter(
        F.action == ResumeAction.DELETE,
    )
)
async def delete_resume(
    callback: CallbackQuery,
    callback_data: ResumeCallback,
):
    """
    Ask confirmation before deleting resume.
    """

    resume_id = callback_data.resume_id

    if not resume_id:
        await callback.answer("Resume id topilmadi.", show_alert=True)
        return

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
    ResumeCallback.filter(
        F.action == ResumeAction.CONFIRM_DELETE,
    )
)
async def confirm_delete(
    callback: CallbackQuery,
    callback_data: ResumeCallback,
):
    """
    Delete selected resume.
    """

    resume_id = callback_data.resume_id

    if not resume_id:
        await callback.answer("Resume id topilmadi.", show_alert=True)
        return

    await resume_service.delete_resume(
        telegram_id=callback.from_user.id,
        resume_id=resume_id,
    )

    await callback.message.edit_text(
        "✅ Resume deleted successfully."
    )

    await callback.answer()
