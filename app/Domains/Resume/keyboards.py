from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.Shared.callbacks import ResumeCallback, SectionCallback
from app.Shared.enums import ResumeAction, SectionAction, SectionType


def resume_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📄 My Resumes",
        callback_data=ResumeCallback(
            action=ResumeAction.LIST,
        ),
    )

    builder.button(
        text="➕ Create Resume",
        callback_data=ResumeCallback(
            action=ResumeAction.CREATE,
        ),
    )

    builder.adjust(1)

    return builder.as_markup()


def resume_detail_keyboard(
    resume_id: str,
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✏️ Edit",
        callback_data=ResumeCallback(
            action=ResumeAction.EDIT,
            resume_id=resume_id,
        ),
    )

    builder.button(
        text="📑 Duplicate",
        callback_data=ResumeCallback(
            action=ResumeAction.DUPLICATE,
            resume_id=resume_id,
        ),
    )

    builder.button(
        text="📤 Export",
        callback_data=ResumeCallback(
            action=ResumeAction.EXPORT,
            resume_id=resume_id,
        ),
    )

    builder.button(
        text="🗑 Delete",
        callback_data=ResumeCallback(
            action=ResumeAction.DELETE,
            resume_id=resume_id,
        ),
    )

    builder.button(
        text="⬅️ Back",
        callback_data=ResumeCallback(
            action=ResumeAction.LIST,
        ),
    )

    builder.adjust(2, 2, 1)

    return builder.as_markup()


def delete_confirmation_keyboard(
    resume_id: str,
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Yes",
        callback_data=ResumeCallback(
            action=ResumeAction.CONFIRM_DELETE,
            resume_id=resume_id,
        ),
    )

    builder.button(
        text="❌ Cancel",
        callback_data=ResumeCallback(
            action=ResumeAction.VIEW,
            resume_id=resume_id,
        ),
    )

    builder.adjust(2)

    return builder.as_markup()


def template_keyboard(
    templates: list[dict],
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    for template in templates:
        raw_id = template.get("id")

        # ba'zan id nested dict bo'lib kelishi mumkin — shuni handle qilamiz
        if isinstance(raw_id, dict):
            raw_id = raw_id.get("id")

        template_id = str(raw_id)

        builder.button(
            text=template.get("name", "Template"),
            callback_data=ResumeCallback(
                action=ResumeAction.TEMPLATE,
                template_id=template_id,
            ),
        )

    builder.adjust(1)

    return builder.as_markup()


def pagination_keyboard(
    page: int,
    has_prev: bool,
    has_next: bool,
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    if has_prev:
        builder.button(
            text="⬅️ Previous",
            callback_data=ResumeCallback(
                action=ResumeAction.PAGE,
                page=page - 1,
            ),
        )

    if has_next:
        builder.button(
            text="Next ➡️",
            callback_data=ResumeCallback(
                action=ResumeAction.PAGE,
                page=page + 1,
            ),
        )

    builder.adjust(2)

    return builder.as_markup()


def resume_list_keyboard(
    resumes: list[dict],
    page: int,
    has_prev: bool,
    has_next: bool,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for resume in resumes:
        resume_id = str(resume.get("id", ""))

        if not resume_id:
            continue

        builder.button(
            text=f"📄 {resume.get('title', 'Untitled')}",
            callback_data=ResumeCallback(
                action=ResumeAction.VIEW,
                resume_id=resume_id,
            ),
        )

    if has_prev:
        builder.button(
            text="⬅️ Previous",
            callback_data=ResumeCallback(
                action=ResumeAction.LIST,
                page=page - 1,
            ),
        )

    if has_next:
        builder.button(
            text="Next ➡️",
            callback_data=ResumeCallback(
                action=ResumeAction.LIST,
                page=page + 1,
            ),
        )

    builder.button(
        text="➕ Create Resume",
        callback_data=ResumeCallback(
            action=ResumeAction.CREATE,
        ),
    )

    builder.button(
        text="🏠 Menu",
        callback_data=ResumeCallback(
            action=ResumeAction.MENU,
        ),
    )

    builder.adjust(1)

    return builder.as_markup()


def preview_keyboard() -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Save Resume",
        callback_data=ResumeCallback(
            action=ResumeAction.SAVE,
        ),
    )

    builder.button(
        text="✏️ Edit",
        callback_data=ResumeCallback(
            action=ResumeAction.EDIT_PREVIEW,
        ),
    )

    builder.button(
        text="❌ Cancel",
        callback_data=ResumeCallback(
            action=ResumeAction.CANCEL,
        ),
    )

    builder.adjust(1)

    return builder.as_markup()

def export_keyboard(
    resume_id: str,
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📄 PDF",
        callback_data=f"resume:export_pdf:{resume_id}",
    )

    builder.button(
        text="📝 DOCX",
        callback_data=f"resume:export_docx:{resume_id}",
    )

    builder.button(
        text="⬅️ Back",
        callback_data=ResumeCallback(
            action=ResumeAction.VIEW,
            resume_id=resume_id,
        ),
    )

    builder.adjust(2, 1)

    return builder.as_markup()

def section_menu_keyboard() -> InlineKeyboardMarkup:
    """Section turini tanlash yoki tugatish menyusi."""

    builder = InlineKeyboardBuilder()

    labels = {
        SectionType.SUMMARY: "📄 Summary",
        SectionType.EXPERIENCE: "💼 Experience",
        SectionType.EDUCATION: "🎓 Education",
        SectionType.SKILLS: "🛠 Skills",
    }

    for section_type, label in labels.items():
        builder.button(
            text=label,
            callback_data=SectionCallback(
                action=SectionAction.CHOOSE,
                section_type=section_type,
            ),
        )

    builder.button(
        text="✅ Tugatish va saqlash",
        callback_data=SectionCallback(
            action=SectionAction.FINISH,
        ),
    )

    builder.adjust(2, 2, 1)

    return builder.as_markup()
