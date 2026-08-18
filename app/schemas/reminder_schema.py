from pydantic import BaseModel, Field


class ReminderCreate(BaseModel):
    medicine_name: str = Field(..., min_length=1, max_length=200)
    time: str = Field(..., min_length=1)
    frequency: str = "Once daily"
    notes: str | None = None


class ReminderUpdate(BaseModel):
    medicine_name: str | None = None
    time: str | None = None
    frequency: str | None = None
    notes: str | None = None
