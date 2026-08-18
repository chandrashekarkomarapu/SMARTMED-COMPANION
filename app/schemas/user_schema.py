from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=200)
    password_hash: str = Field(..., min_length=6)
    preferred_language: str = "en"


class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    preferred_language: str = "en"
