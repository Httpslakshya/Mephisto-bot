import re

def escape_markdown(text):
    """Escape MarkdownV2 special characters for Telegram messages."""
    escape_chars = r"_*[]()~`>#+=|{}.!\\-"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text) 