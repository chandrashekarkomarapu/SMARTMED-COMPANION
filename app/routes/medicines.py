from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.medicine import Medicine
from app.schemas.medicine_schema import MedicineCreate, MedicineUpdate

router = APIRouter(tags=["medicines"])


@router.get("/medicines")
async def medicines_page(request: Request, q: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Medicine)
    if q:
        query = query.filter(Medicine.name.ilike(f"%{q}%"))
    medicines = query.all()
    try:
        template = request.app.state.templates.env.get_template("medicines.html")
        html_content = template.render(request=request, medicines=medicines, search_query=q or "")
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading medicines page: {str(e)}</h1>", status_code=500)


@router.get("/medicines/search")
async def search_medicines(q: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Medicine)
    if q:
        query = query.filter(Medicine.name.ilike(f"%{q}%"))
    results = query.all()
    return [{"id": item.id, "name": item.name, "strength": item.strength, "frequency": item.frequency} for item in results]


@router.get("/medicines/{medicine_id}")
async def get_medicine(medicine_id: int, db: Session = Depends(get_db)):
    item = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    return {"id": item.id, "name": item.name, "strength": item.strength, "frequency": item.frequency, "duration": item.duration, "instructions": item.instructions, "source": item.source}


@router.post("/medicines")
async def create_medicine(payload: MedicineCreate, db: Session = Depends(get_db)):
    item = Medicine(user_id=1, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return JSONResponse({"status": "success", "medicine": {"id": item.id, "name": item.name}}, status_code=201)


@router.put("/medicines/{medicine_id}")
async def update_medicine(medicine_id: int, payload: MedicineUpdate, db: Session = Depends(get_db)):
    item = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(item, key, value)
    db.commit()
    return {"status": "success", "message": "Medicine updated."}


@router.delete("/medicines/{medicine_id}")
async def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    item = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    db.delete(item)
    db.commit()
    return {"status": "success", "message": "Medicine deleted."}
