from enum import StrEnum


class ResumeAction(StrEnum):
    MENU = "menu"
    LIST = "list"
    VIEW = "view"
    CREATE = "create"
    SAVE = "save"
    EDIT = "edit"
    EDIT_PREVIEW = "edit_preview"
    DELETE = "delete"
    CONFIRM_DELETE = "confirm_delete"
    DUPLICATE = "duplicate"
    EXPORT = "export"
    TEMPLATE = "template"
    PAGE = "page"
    CANCEL = "cancel"


class SectionType(StrEnum):
    SUMMARY = "summary"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"


class SectionAction(StrEnum):
    CHOOSE = "choose"
    FINISH = "finish"


class AuthAction(StrEnum):
    LOGIN = "login"
    REGISTER = "register"
    LOGOUT = "logout"