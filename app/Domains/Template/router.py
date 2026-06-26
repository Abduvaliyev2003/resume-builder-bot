from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery

from app.Domains.Template.service import template_service
from app.Domains.Template.keyboards import templates_keyboard

router = Router(name="template")

@router.callback_query(F.data == "templates")
async def templates(callback: CallbackQuery):

    templates = await template_service.get_templates()

    await callback.message.answer(
        text="📑 Available Templates",
        reply_markup=templates_keyboard(
            templates
        ),
    )

    await callback.answer()

@router.callback_query(F.data.startswith("template:"))
async def template_detail(callback: CallbackQuery):

    template_id = callback.data.split(":")[1]

    template = await template_service.get_template(
        template_id
    )

    await callback.message.answer(

        text=(
            f"📄 <b>{template['name']}</b>\n\n"
            f"{template['description']}"
        )

    )

    await callback.answer()