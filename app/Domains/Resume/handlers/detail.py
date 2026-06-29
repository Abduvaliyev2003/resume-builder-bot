from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.Domains.Resume.service import resume_service
from app.Domains.Resume.formatter import resume_formatter
from app.Domains.Resume.keyboards import resume_detail_keyboard
from app.Shared.api import APIError
from app.Shared.callbacks import ResumeCallback
from app.Shared.enums import ResumeAction
from app.Shared.storage import token_storage

router = Router(name="resume.detail")


@router.callback_query(
    ResumeCallback.filter(
        F.action == ResumeAction.VIEW,
    )
)
async def resume_detail(
    callback: CallbackQuery,
    callback_data: ResumeCallback,
):

    resume_id = callback_data.resume_id

    if not resume_id:
        await callback.answer("Resume id topilmadi.", show_alert=True)
        return

    resume = await resume_service.get_resume(
        telegram_id=callback.from_user.id,
        resume_id=resume_id,
    )

    text = resume_formatter.format_resume(resume)

    await callback.message.edit_text(
        text=text,
        reply_markup=resume_detail_keyboard(resume_id),
    )

    await callback.answer()


@router.callback_query(
    ResumeCallback.filter(
        F.action == ResumeAction.DUPLICATE,
    )
)
async def duplicate_resume(
    callback: CallbackQuery,
    callback_data: ResumeCallback,
):
    resume_id = callback_data.resume_id

    if not resume_id:
        await callback.answer("Resume id topilmadi.", show_alert=True)
        return

    token = token_storage.get_token(callback.from_user.id)

    if not token:
        await callback.answer("Please login first.", show_alert=True)
        return

    try:
        await resume_service.duplicate(
            token=token,
            resume_id=resume_id,
        )
    except APIError as exc:
        await callback.answer(str(exc), show_alert=True)
        return

    await callback.message.answer(
        "✅ Resume nusxalandi.",
    )

    await callback.answer()
