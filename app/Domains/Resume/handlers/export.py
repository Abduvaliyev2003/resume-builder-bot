from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.Domains.Resume.service import resume_service
from app.Domains.Resume.keyboards import export_keyboard

router = Router(name="resume.export")

@router.callback_query(
    F.data.startswith("resume:export:")
)
async def export_menu(
    callback: CallbackQuery,
):

    resume_id = callback.data.split(":")[2]

    await callback.message.edit_text(

        "📤 Choose export format:",

        reply_markup=export_keyboard(
            resume_id,
        ),
    )

    await callback.answer()

@router.callback_query(
    F.data.startswith("resume:export_pdf:")
)
async def export_pdf(
    callback: CallbackQuery,
):

    resume_id = callback.data.split(":")[2]

    response = await resume_service.export_resume(

        telegram_id=callback.from_user.id,

        resume_id=resume_id,

        export_format="pdf",

    )

    await callback.message.answer(
        "✅ PDF export created."
    )

    await callback.answer()

@router.callback_query(
    F.data.startswith("resume:export_docx:")
)
async def export_docx(
    callback: CallbackQuery,
):

    resume_id = callback.data.split(":")[2]

    response = await resume_service.export_resume(

        telegram_id=callback.from_user.id,

        resume_id=resume_id,

        export_format="docx",

    )

    await callback.message.answer(
        "✅ DOCX export created."
    )

    await callback.answer()