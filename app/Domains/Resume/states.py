from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class ResumeState(StatesGroup):

    title = State()

    template = State()

    personal = State()

    experience = State()

    education = State()

    skills = State()

    languages = State()

    projects = State()

    certificates = State()

    social = State()

    preview = State()