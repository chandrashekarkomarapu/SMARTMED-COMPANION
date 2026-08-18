from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.medicine import Medicine
from app.models.prescription import Prescription
from app.models.reminder import Reminder
from app.models.safety_alert import SafetyAlert

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()
    reminders = db.query(Reminder).all()[:5]
    prescriptions = db.query(Prescription).all()[:5]
    alerts = db.query(SafetyAlert).all()[:5]
    
    try:
        # Use the app state's Jinja2 templates environment
        template = request.app.state.templates.env.get_template("dashboard.html")
        html_content = template.render(
            request=request,
            medicines=medicines,
            reminders=reminders,
            prescriptions=prescriptions,
            alerts=alerts,
            welcome_name="Alex Johnson",
        )
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading dashboard: {str(e)}</h1>", status_code=500)
