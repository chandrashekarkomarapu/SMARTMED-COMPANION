from datetime import datetime


def reminder_status_for_time(time_value: str) -> str:
    try:
        now = datetime.now().strftime("%H:%M")
        if now > time_value:
            return "upcoming"
    except Exception:
        pass
    return "upcoming"
