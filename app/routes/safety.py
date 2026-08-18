from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.medicine import Medicine
from app.models.safety_alert import SafetyAlert
from app.services.medication_safety import build_safety_report

router = APIRouter(tags=["safety"])


@router.get("/safety")
async def safety_page(request: Request, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()
    alerts = db.query(SafetyAlert).all()
    try:
        template = request.app.state.templates.env.get_template("safety.html")
        html_content = template.render(request=request, medicines=medicines, alerts=alerts)
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading safety page: {str(e)}</h1>", status_code=500)


@router.post("/safety/check")
async def check_safety(medicine_names: list[str], db: Session = Depends(get_db)):
    del db
    report = build_safety_report(medicine_names)
    return JSONResponse({"status": "success", "report": report})
