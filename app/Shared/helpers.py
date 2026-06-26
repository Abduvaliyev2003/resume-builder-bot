from datetime import datetime


def format_datetime(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")

def success(text: str) -> str:
    return f"✅ {text}"

def error(text: str) -> str:
    return f"❌ {text}"

def warning(text: str) -> str:
    return f"⚠️ {text}"