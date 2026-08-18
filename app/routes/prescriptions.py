from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.medicine import Medicine
from app.models.prescription import Prescription
from app.services.ocr_service import process_file
from app.services.prescription_parser import extract_fields
from app.utils.logger import logger
from app.utils.validators import get_upload_directory, sanitize_filename, validate_upload

router = APIRouter(tags=["prescriptions"])


@router.get("/prescriptions")
async def get_prescriptions(db: Session = Depends(get_db)):
    items = db.query(Prescription).all()
    return [{"id": item.id, "title": item.title, "status": item.status, "medicine_count": item.medicine_count} for item in items]


@router.get("/scanner")
async def scanner_page(request: Request):
    try:
        template = request.app.state.templates.env.get_template("scanner.html")
        html_content = template.render(request=request)
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading scanner page: {str(e)}</h1>", status_code=500)


@router.post("/prescriptions/upload")
async def upload_prescription(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Please select a prescription file.")

    valid, error = validate_upload(file.filename, file.size)
    if not valid:
        raise HTTPException(status_code=400, detail=error or "Invalid file.")

    upload_dir = get_upload_directory()
    original_name = sanitize_filename(file.filename)
    safe_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{original_name}"
    target_path = upload_dir / safe_name

    try:
        content = await file.read()
        target_path.write_bytes(content)
    except Exception as exc:
        logger.exception("Error saving uploaded prescription")
        raise HTTPException(status_code=500, detail="Something went wrong while saving your prescription file.") from exc

    try:
        result = process_file(str(target_path))
    except Exception as exc:
        logger.exception("OCR processing failed")
        raise HTTPException(status_code=500, detail="Unable to read the prescription. Please try a clearer image.") from exc

    if result.get("status") == "error":
        message = result.get("error", "Unable to read the prescription.")
        return JSONResponse({"status": "error", "message": message, "detail": message}, status_code=400)

    parsed = extract_fields(result.get("text", ""), result.get("confidence", 0.0))
    record = Prescription(
        user_id=1,
        title=original_name,
        file_name=safe_name,
        file_path=str(target_path),
        extracted_text=result.get("text", ""),
        confidence=result.get("confidence", 0.0),
        status="pending",
        medicine_count=1 if parsed.get("medicine_name") else 0,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return JSONResponse({
        "status": "success",
        "id": record.id,
        "filename": safe_name,
        "text": result.get("text", ""),
        "confidence": result.get("confidence", 0.0),
        "parsed": parsed,
        "message": "Prescription uploaded and parsed.",
    })


@router.post("/prescriptions/confirm")
async def confirm_prescription(
    request: Request,
    prescription_id: int | None = Query(default=None),
    medicine_name: str = Query(default=""),
    strength: str = Query(default=""),
    frequency: str = Query(default=""),
    duration: str = Query(default=""),
    instructions: str = Query(default=""),
    db: Session = Depends(get_db),
):
    pid = prescription_id
    m_name = medicine_name
    m_strength = strength
    m_freq = frequency
    m_dur = duration
    m_inst = instructions

    content_type = request.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        try:
            body = await request.json()
            if isinstance(body, dict):
                pid = body.get("prescription_id", pid)
                m_name = body.get("medicine_name", m_name)
                m_strength = body.get("strength", m_strength)
                m_freq = body.get("frequency", m_freq)
                m_dur = body.get("duration", m_dur)
                m_inst = body.get("instructions", m_inst)
        except Exception:
            pass
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        try:
            form = await request.form()
            if form:
                if "prescription_id" in form:
                    try:
                        pid = int(form["prescription_id"])
                    except (ValueError, TypeError):
                        pass
                m_name = str(form.get("medicine_name", m_name))
                m_strength = str(form.get("strength", m_strength))
                m_freq = str(form.get("frequency", m_freq))
                m_dur = str(form.get("duration", m_dur))
                m_inst = str(form.get("instructions", m_inst))
        except Exception:
            pass

    if pid is None:
        raise HTTPException(status_code=400, detail="Prescription ID is required.")

    record = db.query(Prescription).filter(Prescription.id == pid).first()
    if not record:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    record.status = "confirmed"

    # Save to Medicine table if medicine_name is provided
    if m_name and m_name.strip():
        existing_med = db.query(Medicine).filter(Medicine.user_id == record.user_id, Medicine.name == m_name.strip()).first()
        if not existing_med:
            new_med = Medicine(
                user_id=record.user_id,
                name=m_name.strip(),
                strength=m_strength.strip() if m_strength else None,
                frequency=m_freq.strip() if m_freq else None,
                duration=m_dur.strip() if m_dur else None,
                instructions=m_inst.strip() if m_inst else None,
                source=f"Prescription #{record.id}",
            )
            db.add(new_med)
    db.commit()

    return JSONResponse({
        "status": "success",
        "message": "Prescription confirmed and saved.",
        "data": {
            "prescription_id": pid,
            "medicine_name": m_name,
            "strength": m_strength,
            "frequency": m_freq,
            "duration": m_dur,
            "instructions": m_inst,
        },
    })
