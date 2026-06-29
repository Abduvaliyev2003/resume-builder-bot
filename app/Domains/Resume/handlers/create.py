import json
from typing import Any

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram.fsm.context import FSMContext

from app.Domains.Resume.states import ResumeState
from app.Domains.Resume.service import resume_service
from app.Domains.Template.service import template_service
from app.Domains.Resume.keyboards import (
    template_keyboard,
)
from app.Shared.api import APIError
from app.Shared.callbacks import ResumeCallback
from app.Shared.enums import ResumeAction

router = Router(
    name="resume.create",
)

@router.callback_query(
    ResumeCallback.filter(
        F.action == ResumeAction.CREATE,
    )
)
async def create_resume(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ResumeCallback,
):

    await state.clear()

    await state.set_state(
        ResumeState.title,
    )

    await callback.message.answer(
        "📝 Resume title kiriting:"
    )

    await callback.answer()

@router.message(
    ResumeState.title,
)
async def title(
    message: Message,
    state: FSMContext,
):

    await state.update_data(
        title=message.text,
    )

    templates = await template_service.get_templates(
        telegram_id=message.from_user.id,
    )

    await state.set_state(
        ResumeState.template,
    )

    await message.answer(
        "🎨 Template tanlang:",
        reply_markup=template_keyboard(
            templates,
        ),
    )

@router.callback_query(
    ResumeState.template,
    ResumeCallback.filter(
        F.action == ResumeAction.TEMPLATE,
    ),
)
async def choose_template(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ResumeCallback,
):

    template_id = callback_data.template_id

    await state.update_data(
        template_id=template_id,
    )

    await state.set_state(
        ResumeState.sections,
    )

    await callback.message.answer(
        (
            "🤖 Endi resume sections JSON array yuboring.\n\n"
            "Masalan:\n"
            "[{\"section_type\":\"summary\",\"content\":[{\"text\":\"...\"}],\"order_index\":1}]"
        )
    )

    await callback.answer()


@router.message(
    ResumeState.sections,
)
async def sections(
    message: Message,
    state: FSMContext,
):
    """Create a resume from the collected title, template and sections."""

    try:
        parsed_sections = _parse_sections(message.text or "")
    except ValueError as exc:
        await message.answer(f"❌ Sections xato: {exc}")
        return

    data = await state.get_data()

    try:
        await resume_service.create_resume(
            telegram_id=message.from_user.id,
            title=data["title"],
            template_id=data.get("template_id"),
            sections=parsed_sections,
        )
    except APIError as exc:
        await message.answer(f"❌ Resume yaratilmadi: {exc}")
        return

    await state.clear()

    await message.answer(
        "✅ Resume yaratildi."
    )


def _parse_sections(raw_text: str) -> list[dict[str, Any]]:
    """Parse and validate API sections payload from Telegram text."""

    try:
        sections = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError("JSON array yuboring.") from exc

    if not isinstance(sections, list):
        raise ValueError("sections array bo'lishi kerak.")

    for index, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            raise ValueError(f"{index}-section object bo'lishi kerak.")

        if not isinstance(section.get("section_type"), str) or not section["section_type"].strip():
            raise ValueError(f"{index}-section uchun section_type majburiy.")

        if "content" not in section or not isinstance(section["content"], list):
            raise ValueError(f"{index}-section uchun content array majburiy.")

        order_index = section.get("order_index")

        if order_index is not None and not isinstance(order_index, int):
            raise ValueError(f"{index}-section uchun order_index integer bo'lishi kerak.")

    return sections
