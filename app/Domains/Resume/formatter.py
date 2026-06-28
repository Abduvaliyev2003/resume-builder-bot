from typing import Any


class ResumeFormatter:

    @staticmethod
    def format_resume(
        resume: dict[str, Any],
    ) -> str:
        """
        Format resume for Telegram HTML.
        """

        lines: list[str] = []

        lines.append("📄 <b>Resume Preview</b>")
        lines.append("")

        lines.append(
            f"📝 <b>Title:</b> {resume.get('title', '-')}"
        )

        template = resume.get("template")

        if template:
            lines.append(
                f"🎨 <b>Template:</b> {template.get('name', '-')}"
            )

        lines.append("")

        sections = resume.get("sections", [])

        for section in sections:

            section_type = section.get("section_type")

            content = section.get("content", {})

            # -----------------------
            # Contact
            # -----------------------

            if section_type == "contact":

                lines.append("👤 <b>Contact</b>")

                lines.append(
                    f"Name: {content.get('name', '-')}"
                )

                lines.append(
                    f"Position: {content.get('title', '-')}"
                )

                lines.append(
                    f"Email: {content.get('email', '-')}"
                )

                lines.append(
                    f"Phone: {content.get('phone', '-')}"
                )

                lines.append(
                    f"Address: {content.get('address', '-')}"
                )

                lines.append("")

            # -----------------------
            # Summary
            # -----------------------

            elif section_type == "summary":

                lines.append("📝 <b>Summary</b>")

                lines.append(
                    content.get("text", "-")
                )

                lines.append("")

            # -----------------------
            # Skills
            # -----------------------

            elif section_type == "skills":

                lines.append("🛠 <b>Skills</b>")

                for skill in content.get("list", []):

                    lines.append(
                        f"• {skill}"
                    )

                lines.append("")

            # -----------------------
            # Experience
            # -----------------------

            elif section_type == "experience":

                lines.append("💼 <b>Experience</b>")

                for item in content.get("items", []):

                    lines.append(
                        f"• <b>{item.get('position', '-')}</b>"
                    )

                    lines.append(
                        item.get("company", "-")
                    )

                    start = item.get("start_date", "")

                    end = item.get("end_date", "Present")

                    lines.append(
                        f"{start} - {end}"
                    )

                    description = item.get("description")

                    if description:
                        lines.append(description)

                    lines.append("")

            # -----------------------
            # Education
            # -----------------------

            elif section_type == "education":

                lines.append("🎓 <b>Education</b>")

                for item in content.get("items", []):

                    lines.append(
                        f"• {item.get('institution', '-')}"
                    )

                    lines.append(
                        item.get("degree", "-")
                    )

                    lines.append(
                        str(item.get("year", "-"))
                    )

                    lines.append("")

            # -----------------------
            # Certifications
            # -----------------------

            elif section_type == "certifications":

                lines.append("🏆 <b>Certificates</b>")

                for certificate in content.get("items", []):

                    lines.append(
                        f"• {certificate}"
                    )

                lines.append("")

            # -----------------------
            # Languages
            # -----------------------

            elif section_type == "languages":

                lines.append("🌍 <b>Languages</b>")

                for language in content.get("items", []):

                    lines.append(
                        f"• {language}"
                    )

                lines.append("")

        return "\n".join(lines)


resume_formatter = ResumeFormatter()