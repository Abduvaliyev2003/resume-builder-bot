from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Domains.Resume.handlers.create import _parse_sections
from app.Domains.Resume.service import resume_service
from app.Domains.Resume.states import ResumeState
from app.Shared.api import APIError
from app.Shared.callbacks import ResumeCallback
from app.Shared.enums import ResumeAction
from app.Shared.storage import token_storage

router = Router(name="resume.edit")


@router.callback_query(
    ResumeCallback.filter(
        F.action == ResumeAction.EDIT,
    )
)
async def edit_resume(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ResumeCallback,
) -> None:
    """Start resume edit flow."""

    if not callback_data.resume_id:
        await callback.answer("Resume id topilmadi.", show_alert=True)
        return

    token = token_storage.get_token(callback.from_user.id)

    if not token:
        await callback.answer("Please login first.", show_alert=True)
        return

    try:
        resume = await resume_service.show(
            token=token,
            resume_id=callback_data.resume_id,
        )
    except APIError as exc:
        await callback.answer(str(exc), show_alert=True)
        return

    await state.update_data(
        edit_resume_id=callback_data.resume_id,
        edit_template_id=_template_id(resume),
    )

    await state.set_state(ResumeState.edit_title)

    await callback.message.edit_text(
        (
            "✏️ Yangi resume title kiriting.\n\n"
            f"Hozirgi title: {resume.get('title', '-')}"
        )
    )

    await callback.answer()


@router.message(
    ResumeState.edit_title,
    F.text,
)
async def edit_title(
    message: Message,
    state: FSMContext,
) -> None:
    """Save edited title and ask for sections JSON."""

    data = await state.get_data()

    if "edit_resume_id" not in data:
        return

    await state.update_data(
        edit_title=message.text.strip(),
    )

    await state.set_state(ResumeState.edit_sections)

    await message.answer(
        (
            "Yangi sections JSON array yuboring.\n\n"
            "Har section: section_type string, content array, order_index integer optional."
        )
    )


@router.message(
    ResumeState.edit_sections,
    F.text,
)
async def edit_sections(
    message: Message,
    state: FSMContext,
) -> None:
    """Update a resume using PUT /api/resumes/{id}."""

    data = await state.get_data()

    if "edit_resume_id" not in data:
        return

    try:
        sections = _parse_sections(message.text or "")
    except ValueError as exc:
        await message.answer(f"❌ Sections xato: {exc}")
        return

    token = token_storage.get_token(message.from_user.id)

    if not token:
        await message.answer("❌ Please login first.")
        return

    try:
        await resume_service.update(
            token=token,
            resume_id=data["edit_resume_id"],
            title=data["edit_title"],
            template_id=data.get("edit_template_id"),
            sections=sections,
        )
    except APIError as exc:
        await message.answer(f"❌ Resume yangilanmadi: {exc}")
        return

    await state.clear()

    await message.answer(
        "✅ Resume yangilandi."
    )


def _template_id(resume: dict) -> str | None:
    """Extract template_id from common Laravel response shapes."""

    if isinstance(resume.get("template_id"), str):
        return resume["template_id"]

    template = resume.get("template")

    if isinstance(template, dict) and isinstance(template.get("id"), str):
        return template["id"]

    return None
