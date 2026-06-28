from typing import Any


class ResumeFormatter:

    @staticmethod
    def format_resume(resume: dict[str, Any]) -> str:
        """
        Resume preview for Telegram.
        """

        lines: list[str] = []

        lines.append("📄 <b>Resume</b>\n")

        lines.append(
            f"📝 <b>Title:</b> {resume.get('title', '-')}"
        )

        template = resume.get("template")

        if template:
            lines.append(
                f"🎨 <b>Template:</b> {template.get('name')}"
            )

        lines.append("")

        sections = resume.get("sections", [])

        for section in sections:

            section_type = section.get("section_type")

            content = section.get("content", {})

            if section_type == "personal":

                lines.append("👤 <b>Personal</b>")

                lines.append(
                    f"Name: {content.get('full_name','-')}"
                )

                lines.append(
                    f"Email: {content.get('email','-')}"
                )

                lines.append(
                    f"Phone: {content.get('phone','-')}"
                )

            elif section_type == "experience":

                lines.append("\n💼 <b>Experience</b>")

                lines.append(
                    f"{content.get('position','-')}"
                )

                lines.append(
                    f"{content.get('company','-')}"
                )

            elif section_type == "education":

                lines.append("\n🎓 <b>Education</b>")

                lines.append(
                    f"{content.get('university','-')}"
                )

                lines.append(
                    f"{content.get('degree','-')}"
                )

            elif section_type == "skills":

                lines.append("\n🛠 <b>Skills</b>")

                for skill in content.get("items", []):

                    lines.append(
                        f"• {skill}"
                    )

            elif section_type == "languages":

                lines.append("\n🌍 <b>Languages</b>")

                for language in content.get("items", []):

                    lines.append(
                        f"• {language}"
                    )

            elif section_type == "projects":

                lines.append("\n🚀 <b>Projects</b>")

                for project in content.get("items", []):

                    lines.append(
                        f"• {project}"
                    )

            elif section_type == "certificates":

                lines.append("\n🏆 <b>Certificates</b>")

                for certificate in content.get("items", []):

                    lines.append(
                        f"• {certificate}"
                    )

            elif section_type == "social":

                lines.append("\n🔗 <b>Social Links</b>")

                for social in content.get("items", []):

                    lines.append(
                        f"• {social}"
                    )

        return "\n".join(lines)


resume_formatter = ResumeFormatter()