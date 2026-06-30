from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class ResumeState(StatesGroup):
    title = State()
    template = State()
    section_menu = State()
    section_field = State()
    section_item_more = State()
    preview = State()
    edit_title = State()
    edit_sections = State()