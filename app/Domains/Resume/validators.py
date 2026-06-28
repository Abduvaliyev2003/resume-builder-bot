import re


TITLE_MAX_LENGTH = 255


def validate_title(title: str) -> bool:
    """
    Validate resume title.
    """

    return (
        isinstance(title, str)
        and len(title.strip()) > 0
        and len(title) <= TITLE_MAX_LENGTH
    )


def validate_uuid(value: str) -> bool:
    """
    Validate UUID.
    """

    pattern = (
        r"^[0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12}$"
    )

    return bool(re.match(pattern, value))