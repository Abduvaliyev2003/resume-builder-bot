from app.Shared.enums import SectionType

# ==========================================================
# SECTION QUESTIONS
# ==========================================================

SECTION_FIELDS: dict[SectionType, list[tuple[str, str]]] = {
    SectionType.CONTACT: [
        ("name", "👤 To'liq ismingiz?"),
        ("title", "💼 Kasbingiz yoki Professional Title?"),
        ("email", "📧 Email manzilingiz?"),
        ("phone_country", "🌍 Telefon kodi? (Masalan: +998)"),
        ("phone", "📱 Telefon raqamingiz?"),
        ("address", "📍 Manzilingiz?"),
    ],

    SectionType.SUMMARY: [
        ("text", "✍️ O'zingiz haqingizda qisqacha yozing:"),
    ],

    SectionType.EXPERIENCE: [
        ("company", "🏢 Kompaniya nomi?"),
        ("role", "💼 Lavozimingiz?"),
        ("duration", "📅 Ish davri? (Masalan: Jan 2023 - Present)"),
        ("description", "📝 Qisqacha tavsif?"),
    ],

    SectionType.EDUCATION: [
        ("school", "🏫 Universitet yoki maktab nomi?"),
        ("degree", "🎓 Yo'nalish yoki Degree?"),
        ("year", "📅 Bitirgan yil?"),
    ],

    SectionType.CERTIFICATIONS: [
        ("name", "📜 Sertifikat nomi?"),
        ("organization", "🏢 Sertifikatni bergan tashkilot?"),
        ("issue_date", "📅 Berilgan sana?"),
        ("credential_id", "🆔 Credential ID (bo'lmasa '-' yozing)"),
    ],

    SectionType.LANGUAGES: [
        ("language", "🌐 Til nomi?"),
        ("level", "📊 Darajasi? (A1, B2, C1, Native...)"),
    ],
}

# ==========================================================
# SINGLE SECTION
# ==========================================================

SINGLE_SECTIONS = {
    SectionType.CONTACT,
    SectionType.SUMMARY,
}

# ==========================================================
# SKILLS
# ==========================================================

SKILLS_PROMPT = (
    "🛠 Skilllaringizni vergul bilan yozing.\n\n"
    "Masalan:\n"
    "PHP, Laravel, PostgreSQL, Docker"
)

# ==========================================================
# TITLES
# ==========================================================

SECTION_TITLES = {
    SectionType.CONTACT: "👤 Contact",
    SectionType.SUMMARY: "📄 Summary",
    SectionType.SKILLS: "🛠 Skills",
    SectionType.EXPERIENCE: "💼 Experience",
    SectionType.EDUCATION: "🎓 Education",
    SectionType.CERTIFICATIONS: "📜 Certifications",
    SectionType.LANGUAGES: "🌐 Languages",
}

# ==========================================================
# ORDER
# ==========================================================

SECTION_ORDER = [
    SectionType.CONTACT,
    SectionType.SUMMARY,
    SectionType.SKILLS,
    SectionType.EXPERIENCE,
    SectionType.EDUCATION,
    SectionType.CERTIFICATIONS,
    SectionType.LANGUAGES,
]

# ==========================================================
# DEFAULT CONTENT
# ==========================================================


def default_content(section_type: SectionType) -> dict:
    """
    Website bilan bir xil default structure.
    """

    if section_type == SectionType.CONTACT:
        return {
            "name": "",
            "title": "",
            "email": "",
            "phone": "",
            "phone_country": "+998",
            "address": "",
            "photo": None,
        }

    if section_type == SectionType.SUMMARY:
        return {
            "text": "",
        }

    if section_type == SectionType.SKILLS:
        return {
            "list": [],
        }

    if section_type == SectionType.EXPERIENCE:
        return {
            "items": [],
        }

    if section_type == SectionType.EDUCATION:
        return {
            "items": [],
        }

    if section_type == SectionType.CERTIFICATIONS:
        return {
            "items": [],
        }

    if section_type == SectionType.LANGUAGES:
        return {
            "items": [],
        }

    return {}

# ==========================================================
# BUILD PAYLOAD
# ==========================================================


def build_sections_payload(
    filled: dict[SectionType, dict],
) -> list[dict]:
    """
    Website yuboradigan payload bilan bir xil JSON hosil qiladi.
    """

    payload: list[dict] = []

    for index, section_type in enumerate(SECTION_ORDER, start=1):
        payload.append(
            {
                "section_type": section_type.value,
                "content": filled.get(
                    section_type,
                    default_content(section_type),
                ),
                "order_index": index,
            }
        )

    return payload