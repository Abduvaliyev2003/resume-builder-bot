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
    add_more_item_keyboard,
)
from app.Domains.Resume.sections_config import (
    SECTION_FIELDS,
    SECTION_TITLES,
    SINGLE_SECTIONS,
    SKILLS_PROMPT,
    build_sections_payload,
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
    await state.set_state(ResumeState.title)
    await callback.message.answer("📝 Resume title kiriting:")
    await callback.answer()


@router.message(
    ResumeState.title,
)
async def title(
    message: Message,
    state: FSMContext,
):
    await state.update_data(title=message.text)

    templates = await template_service.get_templates(
        telegram_id=message.from_user.id,
    )

    await state.set_state(ResumeState.template)

    await message.answer(
        "🎨 Template tanlang:",
        reply_markup=template_keyboard(templates),
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
    await state.update_data(
        template_id=callback_data.template_id,
        filled_sections={},  # {section_type_value: content_dict}
    )

    await state.set_state(ResumeState.section_menu)

    await callback.message.answer(
        "🧩 Resume bo'limlarini to'ldiramiz. Qaysi bo'limdan boshlaymiz?\n\n"
        "Istasangiz ba'zilarini bo'sh qoldirib, keyinroq saytda to'ldirishingiz mumkin.",
        reply_markup=section_menu_keyboard(set()),
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

    if section_type == SectionType.SKILLS:
        await state.update_data(current_section_type=section_type.value)
        await state.set_state(ResumeState.section_field)
        await callback.message.answer(SKILLS_PROMPT)
        await callback.answer()
        return

    await state.update_data(
        current_section_type=section_type.value,
        current_field_index=0,
        current_answers={},
    )

    await state.set_state(ResumeState.section_field)

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

    # --- SKILLS: alohida, oddiy vergul bilan ajratilgan ---
    if section_type == SectionType.SKILLS:
        skills = [s.strip() for s in message.text.split(",") if s.strip()]

        filled = data.get("filled_sections", {})
        filled[section_type.value] = {"list": skills}

        await state.update_data(filled_sections=filled)
        await state.set_state(ResumeState.section_menu)

        await message.answer(
            f"✅ {SECTION_TITLES[section_type]} qo'shildi.\n\nYana bo'lim tanlang:",
            reply_markup=section_menu_keyboard(
                {SectionType(k) for k in filled.keys()}
            ),
        )
        return

    # --- Oddiy field-by-field bo'limlar (contact, summary, experience, education, certifications, languages) ---
    field_index = data["current_field_index"]
    answers = data["current_answers"]

    fields = SECTION_FIELDS[section_type]
    field_name, _ = fields[field_index]
    answers[field_name] = message.text
    field_index += 1

    if field_index < len(fields):
        await state.update_data(
            current_field_index=field_index,
            current_answers=answers,
        )
        _, next_question = fields[field_index]
        await message.answer(next_question)
        return

    # Shu item/bo'lim uchun barcha fieldlar to'ldirildi
    filled = data.get("filled_sections", {})

    if section_type in SINGLE_SECTIONS:
        # contact, summary — bitta object
        filled[section_type.value] = answers

        await state.update_data(
            filled_sections=filled,
            current_section_type=None,
            current_field_index=0,
            current_answers={},
        )
        await state.set_state(ResumeState.section_menu)

        await message.answer(
            f"✅ {SECTION_TITLES[section_type]} qo'shildi.\n\nYana bo'lim tanlang:",
            reply_markup=section_menu_keyboard(
                {SectionType(k) for k in filled.keys()}
            ),
        )
        return

    # experience, education, certifications, languages — items ro'yxati
    existing = filled.get(section_type.value, {"items": []})
    existing["items"].append(answers)
    filled[section_type.value] = existing

    await state.update_data(
        filled_sections=filled,
        current_field_index=0,
        current_answers={},
    )
    await state.set_state(ResumeState.section_item_more)

    await message.answer(
        f"✅ {SECTION_TITLES[section_type]}ga element qo'shildi.\n\nYana qo'shasizmi?",
        reply_markup=add_more_item_keyboard(section_type),
    )


@router.callback_query(
    ResumeState.section_item_more,
    SectionCallback.filter(
        F.action == SectionAction.ADD_MORE,
    ),
)
async def add_more_item(
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
    await state.set_state(ResumeState.section_field)

    _, first_question = SECTION_FIELDS[section_type][0]

    await callback.message.answer(
        f"{SECTION_TITLES[section_type]} (yangi element)\n\n{first_question}"
    )

    await callback.answer()


@router.callback_query(
    ResumeState.section_item_more,
    SectionCallback.filter(
        F.action == SectionAction.STOP_ITEMS,
    ),
)
async def stop_items(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: SectionCallback,
):
    data = await state.get_data()
    filled = data.get("filled_sections", {})

    await state.update_data(
        current_section_type=None,
        current_field_index=0,
        current_answers={},
    )
    await state.set_state(ResumeState.section_menu)

    await callback.message.answer(
        "Yana bo'lim tanlang:",
        reply_markup=section_menu_keyboard(
            {SectionType(k) for k in filled.keys()}
        ),
    )

    await callback.answer()


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

    filled_raw = data.get("filled_sections", {})
    filled = {SectionType(k): v for k, v in filled_raw.items()}

    sections_payload = build_sections_payload(filled)

    try:
        await resume_service.create_resume(
            telegram_id=callback.from_user.id,
            title=data["title"],
            template_id=data.get("template_id"),
            sections=sections_payload,
        )
    except APIError as exc:
        await callback.message.answer(f"❌ Resume yaratilmadi: {exc}")
        await callback.answer()
        return

    await state.clear()

    await callback.message.answer("✅ Resume yaratildi.")
    await callback.answer()