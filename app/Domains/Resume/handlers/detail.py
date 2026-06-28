from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.Domains.Resume.service import resume_service
from app.Domains.Resume.formatter import resume_formatter
from app.Domains.Resume.keyboards import resume_detail_keyboard

router = Router(name="resume.detail")


@router.callback_query(F.data.startswith("resume:view:"))
async def resume_detail(callback: CallbackQuery):

    resume_id = callback.data.split(":")[2]

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