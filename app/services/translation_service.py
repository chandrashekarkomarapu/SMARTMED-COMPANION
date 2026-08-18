from app.config.languages import translate_text


def translate_ui(key: str, language: str = "en") -> str:
    return translate_text(key, language)
