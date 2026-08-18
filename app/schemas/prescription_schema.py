from pydantic import BaseModel


class PrescriptionConfirmData(BaseModel):
    prescription_id: int | None = None
    title: str | None = None
    medicine_name: str | None = None
    strength: str | None = None
    frequency: str | None = None
    duration: str | None = None
    instructions: str | None = None
    confidence: float | None = 0.0
    status: str = "pending"
