from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.Shared.callbacks import ResumeCallback
from app.Shared.enums import ResumeAction


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

        builder.button(
            text=template["name"],
            callback_data=ResumeCallback(
                action=ResumeAction.TEMPLATE,
                template_id=template["id"],
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
        callback_data=f"resume:view:{resume_id}",
    )

    builder.adjust(2, 1)

    return builder.as_markup()