from pydantic import BaseModel, Field


class MedicineCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    strength: str | None = None
    frequency: str | None = None
    duration: str | None = None
    instructions: str | None = None
    source: str | None = "User-entered"


class MedicineUpdate(BaseModel):
    name: str | None = None
    strength: str | None = None
    frequency: str | None = None
    duration: str | None = None
    instructions: str | None = None
    source: str | None = None
