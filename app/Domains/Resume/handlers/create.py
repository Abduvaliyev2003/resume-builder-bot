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
    section_menu_keyboard,
)
from app.Domains.Resume.sections_config import (
    SECTION_FIELDS,
    SECTION_TITLES,
    build_section_content,
)
from app.Shared.api import APIError
from app.Shared.callbacks import ResumeCallback, SectionCallback
from app.Shared.enums import ResumeAction, SectionAction, SectionType

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
        sections=[],
    )

    await state.set_state(
        ResumeState.section_menu,
    )

    await callback.message.answer(
        "🧩 Resume'ga qaysi bo'limni qo'shmoqchisiz?",
        reply_markup=section_menu_keyboard(),
    )

    await callback.answer()


@router.callback_query(
    ResumeState.section_menu,
    SectionCallback.filter(
        F.action == SectionAction.CHOOSE,
    ),
)
async def choose_section_type(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: SectionCallback,
):

    section_type = callback_data.section_type

    await state.update_data(
        current_section_type=section_type.value,
        current_field_index=0,
        current_answers={},
    )

    await state.set_state(
        ResumeState.section_field,
    )

    first_field_name, first_question = SECTION_FIELDS[section_type][0]

    await callback.message.answer(
        f"{SECTION_TITLES[section_type]}\n\n{first_question}"
    )

    await callback.answer()


@router.message(
    ResumeState.section_field,
)
async def collect_section_field(
    message: Message,
    state: FSMContext,
):

    data = await state.get_data()

    section_type = SectionType(data["current_section_type"])
    field_index = data["current_field_index"]
    answers: dict[str, Any] = data["current_answers"]

    fields = SECTION_FIELDS[section_type]
    field_name, _ = fields[field_index]

    answers[field_name] = message.text
    field_index += 1

    if field_index < len(fields):
        # Keyingi savolni beramiz
        await state.update_data(
            current_field_index=field_index,
            current_answers=answers,
        )

        _, next_question = fields[field_index]

        await message.answer(next_question)
        return

    # Barcha fieldlar to'ldirildi — sectionni yakunlaymiz
    sections: list[dict] = data.get("sections", [])

    content = build_section_content(section_type, answers)

    sections.append(
        {
            "section_type": section_type.value,
            "content": content,
            "order_index": len(sections) + 1,
        }
    )

    await state.update_data(
        sections=sections,
        current_section_type=None,
        current_field_index=0,
        current_answers={},
    )

    await state.set_state(
        ResumeState.section_menu,
    )

    await message.answer(
        f"✅ {SECTION_TITLES[section_type]} qo'shildi.\n\n"
        "Yana bo'lim qo'shasizmi yoki tugatasizmi?",
        reply_markup=section_menu_keyboard(),
    )


@router.callback_query(
    ResumeState.section_menu,
    SectionCallback.filter(
        F.action == SectionAction.FINISH,
    ),
)
async def finish_sections(
    callback: CallbackQuery,
    state: FSMContext,
):

    data = await state.get_data()

    sections = data.get("sections", [])

    if not sections:
        await callback.answer(
            "⚠️ Kamida 1 ta bo'lim qo'shishingiz kerak.",
            show_alert=True,
        )
        return

    try:
        await resume_service.create_resume(
            telegram_id=callback.from_user.id,
            title=data["title"],
            template_id=data.get("template_id"),
            sections=sections,
        )
    except APIError as exc:
        await callback.message.answer(f"❌ Resume yaratilmadi: {exc}")
        await callback.answer()
        return

    await state.clear()

    await callback.message.answer(
        "✅ Resume yaratildi."
    )

    await callback.answer()