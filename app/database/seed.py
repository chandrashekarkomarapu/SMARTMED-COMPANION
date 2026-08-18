from app.database.database import SessionLocal
from app.models.medicine import Medicine
from app.models.reminder import Reminder
from app.models.safety_alert import SafetyAlert
from app.models.user import User


def seed_demo_data() -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "alex").first()
        if user is None:
            user = User(username="alex", full_name="Alex Johnson", password_hash="demo-password", preferred_language="en")
            db.add(user)
            db.commit()
            db.refresh(user)

        demo_medicines = [
            ("Amoxicillin", "500 mg", "Three times daily", "5 days", "After food", "Demo medication information"),
            ("Paracetamol", "500 mg", "As needed", "As directed", "As directed", "Demo medication information"),
            ("Cetirizine", "10 mg", "Once daily", "7 days", "Before bed", "Demo medication information"),
        ]
        for name, strength, frequency, duration, instructions, source in demo_medicines:
            exists = db.query(Medicine).filter(Medicine.user_id == user.id, Medicine.name == name).first()
            if not exists:
                db.add(Medicine(
                    user_id=user.id,
                    name=name,
                    strength=strength,
                    frequency=frequency,
                    duration=duration,
                    instructions=instructions,
                    source=source,
                ))

        if not db.query(Reminder).filter(Reminder.user_id == user.id).first():
            db.add(Reminder(user_id=user.id, medicine_name="Amoxicillin", time="08:00", frequency="Three times daily", notes="Demo reminder"))
            db.add(Reminder(user_id=user.id, medicine_name="Cetirizine", time="21:00", frequency="Once daily", notes="Demo reminder"))

        if not db.query(SafetyAlert).filter(SafetyAlert.user_id == user.id).first():
            db.add(SafetyAlert(
                user_id=user.id,
                severity="LOW",
                medicine_names="Amoxicillin, Paracetamol",
                description="Demo medication information used for presentation only.",
                source="Demo medication information",
                recommendation="Please contact your doctor or pharmacist before making changes to your medicines.",
            ))

        db.commit()
    finally:
        db.close()
