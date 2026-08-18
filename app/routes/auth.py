from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    full_name: str
    password: str


@router.post("/auth/login")
async def login(payload: LoginRequest):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password are required.")
    return {"message": "Login successful in demo mode.", "username": payload.username, "status": "demo"}


@router.post("/auth/register")
async def register(payload: RegisterRequest):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password are required.")
    return {"message": "Registration successful in demo mode.", "username": payload.username, "status": "demo"}


@router.post("/auth/logout")
async def logout():
    return {"message": "Logged out successfully."}
