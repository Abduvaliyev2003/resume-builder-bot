from aiogram.filters.callback_data import CallbackData

from app.Shared.enums import ResumeAction, AuthAction, SectionAction, SectionType


class ResumeCallback(CallbackData, prefix="resume"):
    action: ResumeAction
    resume_id: str | None = None
    template_id: str | None = None
    page: int | None = None


class SectionCallback(CallbackData, prefix="section"):
    action: SectionAction
    section_type: SectionType | None = None


class TemplateCallback(CallbackData, prefix="template"):
    action: str
    template_id: str | None = None


class ProfileCallback(CallbackData, prefix="profile"):
    action: str


class AuthCallback(CallbackData, prefix="auth"):
    action: AuthAction


class AICallback(CallbackData, prefix="ai"):
    action: str
    resume_id: str | None = None