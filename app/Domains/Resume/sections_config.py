from app.Shared.enums import SectionType


SECTION_FIELDS: dict[SectionType, list[tuple[str, str]]] = {
    SectionType.SUMMARY: [
        ("text", "✍️ Summary matnini kiriting:"),
    ],
    SectionType.EXPERIENCE: [
        ("company", "🏢 Kompaniya nomi?"),
        ("position", "💼 Lavozim?"),
        ("start_date", "📅 Boshlanish sanasi? (masalan: 2021)"),
        ("end_date", "📅 Tugash sanasi? (hozir ishlayotgan bo'lsangiz 'Present' deb yozing)"),
        ("description", "📝 Qisqacha tavsif?"),
    ],
    SectionType.EDUCATION: [
        ("institution", "🎓 Ta'lim muassasasi nomi?"),
        ("degree", "📚 Daraja / yo'nalish?"),
        ("start_date", "📅 Boshlanish yili?"),
        ("end_date", "📅 Tugash yili?"),
    ],
    SectionType.SKILLS: [
        ("skills_list", "🛠 Skill'laringizni vergul bilan ajratib yozing (masalan: Python, SQL, Docker)"),
    ],
}

SECTION_TITLES: dict[SectionType, str] = {
    SectionType.SUMMARY: "📄 Summary",
    SectionType.EXPERIENCE: "💼 Experience",
    SectionType.EDUCATION: "🎓 Education",
    SectionType.SKILLS: "🛠 Skills",
}


def build_section_content(section_type: SectionType, answers: dict[str, str]) -> list[dict]:
    """Convert collected field answers into the API's content array format."""

    if section_type == SectionType.SUMMARY:
        return [{"text": answers["text"]}]

    if section_type == SectionType.SKILLS:
        skills = [s.strip() for s in answers["skills_list"].split(",") if s.strip()]
        return [{"name": skill} for skill in skills]

    
    return [dict(answers)]