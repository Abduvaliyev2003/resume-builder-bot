from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.Domains.Resume.keyboards import (
    pagination_keyboard,
    resume_menu_keyboard,
)
from app.Domains.Resume.service import resume_service
from app.Shared.callbacks import ResumeCallback
from app.Shared.enums import ResumeAction
from app.Shared.storage import token_storage

router = Router(name="resume_list")


@router.callback_query(
    ResumeCallback.filter(
        F.action == ResumeAction.LIST
    )
)
async def resume_list(
    callback: CallbackQuery,
    callback_data: ResumeCallback,
) -> None:
    """
    Show user's resumes.
    """

    token = await token_storage.get(callback.from_user.id)

    if not token:

        await callback.answer(
            "Please login first.",
            show_alert=True,
        )

        return

    page = callback_data.page or 1

    response = await resume_service.get_all(
        token=token,
        page=page,
    )

    resumes = response["data"]

    current_page = response["current_page"]
    last_page = response["last_page"]

    if not resumes:

        await callback.message.edit_text(
            text=(
                "📄 <b>My Resumes</b>\n\n"
                "You don't have any resumes yet."
            ),
            reply_markup=resume_menu_keyboard(),
            parse_mode="HTML",
        )

        await callback.answer()

        return

    text = "📄 <b>My Resumes</b>\n\n"

    for index, resume in enumerate(resumes, start=1):

        text += (
            f"{index}. "
            f"<b>{resume['title']}</b>\n"
        )

    await callback.message.edit_text(
        text=text,
        reply_markup=pagination_keyboard(
            page=current_page,
            has_prev=current_page > 1,
            has_next=current_page < last_page,
        ),
        parse_mode="HTML",
    )

    await callback.answer()