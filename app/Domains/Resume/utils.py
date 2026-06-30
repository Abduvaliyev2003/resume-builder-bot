import json
from typing import Any


def parse_sections(raw_text: str) -> list[dict[str, Any]]:
    """Parse and validate API sections payload from Telegram text."""

    try:
        sections = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError("JSON array yuboring.") from exc

    if not isinstance(sections, list):
        raise ValueError("sections array bo'lishi kerak.")

    for index, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            raise ValueError(f"{index}-section object bo'lishi kerak.")

        if not isinstance(section.get("section_type"), str) or not section["section_type"].strip():
            raise ValueError(f"{index}-section uchun section_type majburiy.")

        if "content" not in section or not isinstance(section["content"], list):
            raise ValueError(f"{index}-section uchun content array majburiy.")

        order_index = section.get("order_index")

        if order_index is not None and not isinstance(order_index, int):
            raise ValueError(f"{index}-section uchun order_index integer bo'lishi kerak.")

    return sections