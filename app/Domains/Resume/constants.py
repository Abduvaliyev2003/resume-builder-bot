from enum import Enum


class ResumeSection(str, Enum):
    PERSONAL = "personal"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"
    LANGUAGES = "languages"
    PROJECTS = "projects"
    CERTIFICATES = "certificates"
    SOCIAL = "social"


SECTION_ORDER = [
    ResumeSection.PERSONAL,
    ResumeSection.EXPERIENCE,
    ResumeSection.EDUCATION,
    ResumeSection.SKILLS,
    ResumeSection.LANGUAGES,
    ResumeSection.PROJECTS,
    ResumeSection.CERTIFICATES,
    ResumeSection.SOCIAL,
]