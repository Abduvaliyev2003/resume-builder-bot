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
    CONTACT = "contact"
    SUMMARY = "summary"
    SKILLS = "skills"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    CERTIFICATIONS = "certifications"
    LANGUAGES = "languages"


class SectionAction(StrEnum):
    CHOOSE = "choose"
    FINISH = "finish"
    ADD_MORE = "add_more"
    STOP_ITEMS = "stop_items"


class AuthAction(StrEnum):
    LOGIN = "login"
    REGISTER = "register"
    LOGOUT = "logout"