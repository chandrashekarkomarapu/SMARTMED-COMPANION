from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
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
        return JSONResponse({"status": "error", "message": result.get("error", "Unable to read the prescription.")}, status_code=400)

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
    prescription_id: int,
    medicine_name: str = "",
    strength: str = "",
    frequency: str = "",
    duration: str = "",
    instructions: str = "",
    db: Session = Depends(get_db),
):
    record = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    record.status = "confirmed"
    db.commit()
    return JSONResponse({
        "status": "success",
        "message": "Prescription confirmed and ready to save.",
        "data": {
            "prescription_id": prescription_id,
            "medicine_name": medicine_name,
            "strength": strength,
            "frequency": frequency,
            "duration": duration,
            "instructions": instructions,
        },
    })
