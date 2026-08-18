from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.reminder import Reminder
from app.schemas.reminder_schema import ReminderCreate, ReminderUpdate

router = APIRouter(tags=["reminders"])


@router.get("/reminders")
async def reminders_page(request: Request, db: Session = Depends(get_db)):
    reminders = db.query(Reminder).all()
    try:
        template = request.app.state.templates.env.get_template("reminders.html")
        html_content = template.render(request=request, reminders=reminders)
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading reminders page: {str(e)}</h1>", status_code=500)


@router.get("/reminders/list")
async def list_reminders(db: Session = Depends(get_db)):
    items = db.query(Reminder).all()
    return [{"id": item.id, "medicine_name": item.medicine_name, "time": item.time, "frequency": item.frequency, "status": item.status} for item in items]


@router.post("/reminders")
async def create_reminder(payload: ReminderCreate, db: Session = Depends(get_db)):
    reminder = Reminder(user_id=1, medicine_name=payload.medicine_name, time=payload.time, frequency=payload.frequency, notes=payload.notes)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return JSONResponse({"status": "success", "reminder": {"id": reminder.id, "medicine_name": reminder.medicine_name, "time": reminder.time}}, status_code=201)


@router.put("/reminders/{reminder_id}")
async def update_reminder(reminder_id: int, payload: ReminderUpdate, db: Session = Depends(get_db)):
    item = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(item, key, value)
    db.commit()
    return {"status": "success", "message": "Reminder updated."}


@router.delete("/reminders/{reminder_id}")
async def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    item = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    db.delete(item)
    db.commit()
    return {"status": "success", "message": "Reminder deleted."}


@router.post("/reminders/{reminder_id}/taken")
async def mark_taken(reminder_id: int, db: Session = Depends(get_db)):
    item = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    item.status = "taken"
    item.is_taken = True
    db.commit()
    return {"status": "success", "message": "Reminder marked as taken."}


@router.post("/reminders/{reminder_id}/missed")
async def mark_missed(reminder_id: int, db: Session = Depends(get_db)):
    item = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    item.status = "missed"
    item.is_taken = False
    db.commit()
    return {"status": "success", "message": "Reminder marked as missed."}
