from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class ResumeState(
    StatesGroup,
):
    title = State()

    template = State()

    sections = State()

    preview = State()

    edit_title = State()

    edit_sections = State()
