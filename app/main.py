from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader, Environment

from app.config.settings import settings
from app.database.database import init_db
from app.database.seed import seed_demo_data
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.routes.emergency import router as emergency_router
from app.routes.medicines import router as medicines_router
from app.routes.prescriptions import router as prescriptions_router
from app.routes.reminders import router as reminders_router
from app.routes.safety import router as safety_router

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="SmartMed Companion",
    description="Multimodal Prescription & Medication Safety Assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")
app.mount("/uploads", StaticFiles(directory=str(BASE_DIR / "uploads")), name="uploads")

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(prescriptions_router)
app.include_router(medicines_router)
app.include_router(reminders_router)
app.include_router(safety_router)
app.include_router(emergency_router)

# Initialize Jinja2Templates - disable caching to avoid issues
template_dir = str(BASE_DIR / "frontend" / "templates")
env = Environment(
    loader=FileSystemLoader(template_dir),
    auto_reload=True  # Auto-reload templates on change
)
# Create a new dict for cache to replace any corrupted one
env.cache = {}
app.state.templates = Jinja2Templates(env=env)


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    seed_demo_data()


@app.get("/")
async def root(request: Request):
    return RedirectResponse(url="/dashboard")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
