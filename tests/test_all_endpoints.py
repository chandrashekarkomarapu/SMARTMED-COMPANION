import pytest
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pymupdf as fitz
from fastapi.testclient import TestClient

from app.main import app
from app.database.database import init_db
from app.database.seed import seed_demo_data
from app.services.ocr_service import process_file
from app.services.prescription_parser import extract_fields
from app.services.medication_safety import build_safety_report, check_interactions, detect_duplicate_medicines
from app.services.drug_information import get_medicine_info
from app.services.speech_service import browser_voice_support, speech_languages
from app.services.translation_service import translate_ui

@pytest.fixture(scope="module")
def client():
    init_db()
    seed_demo_data()
    return TestClient(app)

def test_system_endpoints(client):
    # Health check
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

    # Root redirect
    res = client.get("/", follow_redirects=False)
    assert res.status_code in [301, 302, 307]
    assert "/dashboard" in res.headers.get("location", "")

    # Docs
    res = client.get("/docs")
    assert res.status_code == 200

    # OpenAPI schema
    res = client.get("/openapi.json")
    assert res.status_code == 200
    assert "paths" in res.json()

def test_auth_endpoints(client):
    # Login
    res = client.post("/auth/login", json={"username": "alex", "password": "demo-password"})
    assert res.status_code == 200
    assert res.json().get("status") == "demo"

    # Login empty
    res = client.post("/auth/login", json={"username": "", "password": ""})
    assert res.status_code == 400

    # Register
    res = client.post("/auth/register", json={"username": "testuser", "full_name": "Test User", "password": "password123"})
    assert res.status_code == 200

    # Register empty
    res = client.post("/auth/register", json={"username": "", "full_name": "Test User", "password": ""})
    assert res.status_code == 400

    # Logout
    res = client.post("/auth/logout")
    assert res.status_code == 200

def test_html_ui_pages(client):
    pages = ["/dashboard", "/scanner", "/medicines", "/reminders", "/safety", "/emergency"]
    for page in pages:
        res = client.get(page)
        assert res.status_code == 200
        assert len(res.content) > 1000

def test_medicines_api(client):
    # Search
    res = client.get("/medicines/search?q=Amox")
    assert res.status_code == 200
    assert any(m["name"] == "Amoxicillin" for m in res.json())

    # Create
    new_med = {
        "name": "Amoxicillin Test",
        "strength": "500 mg",
        "frequency": "Twice daily",
        "duration": "5 days",
        "instructions": "After meals",
        "source": "Doctor prescription"
    }
    res = client.post("/medicines", json=new_med)
    assert res.status_code == 201
    med_id = res.json()["medicine"]["id"]

    # Read
    res = client.get(f"/medicines/{med_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Amoxicillin Test"

    # Update
    res = client.put(f"/medicines/{med_id}", json={"strength": "1000 mg"})
    assert res.status_code == 200

    # Delete
    res = client.delete(f"/medicines/{med_id}")
    assert res.status_code == 200

    # Verify 404
    res = client.get(f"/medicines/{med_id}")
    assert res.status_code == 404

def test_reminders_api(client):
    # List
    res = client.get("/reminders/list")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # Create
    new_rem = {
        "medicine_name": "Cetirizine Test",
        "time": "22:00",
        "frequency": "Once daily",
        "notes": "Before bed"
    }
    res = client.post("/reminders", json=new_rem)
    assert res.status_code == 201
    rem_id = res.json()["reminder"]["id"]

    # Update
    res = client.put(f"/reminders/{rem_id}", json={"time": "22:30"})
    assert res.status_code == 200

    # Taken
    res = client.post(f"/reminders/{rem_id}/taken")
    assert res.status_code == 200

    # Missed
    res = client.post(f"/reminders/{rem_id}/missed")
    assert res.status_code == 200

    # Delete
    res = client.delete(f"/reminders/{rem_id}")
    assert res.status_code == 200

def test_safety_and_drug_information(client):
    # Safety report endpoint
    res = client.post("/safety/check", json=["Amoxicillin", "Paracetamol"])
    assert res.status_code == 200
    assert "report" in res.json()

    # Duplicate detection
    report = build_safety_report(["Amoxicillin", "amoxicillin"])
    assert "amoxicillin" in report["duplicate_names"]

    # Drug lookup
    info = get_medicine_info("amoxicillin")
    assert info["medicine_name"] == "Amoxicillin"
    assert "bacterial" in info["purpose"].lower()

def test_ocr_and_prescription_workflow(client):
    upload_dir = Path("uploads/prescriptions")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Create demo PNG prescription
    png_path = upload_dir / "test_pytest_prescription.png"
    img = Image.new("RGB", (700, 300), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        font_bold = ImageFont.truetype("arialbd.ttf", 24)
    except Exception:
        font = font_bold = ImageFont.load_default()

    draw.text((30, 20), "MEDICAL PRESCRIPTION", fill="black", font=font_bold)
    draw.text((30, 65), "Doctor: Dr. Sarah Smith, MD", fill="black", font=font)
    draw.text((30, 105), "Patient: Alex Johnson", fill="black", font=font)
    draw.text((30, 145), "Medicine: Amoxicillin 500mg", fill="black", font=font)
    draw.text((30, 185), "Frequency: Twice daily", fill="black", font=font)
    draw.text((30, 225), "Duration: 7 days", fill="black", font=font)
    draw.text((30, 265), "Instructions: Take after food with water", fill="black", font=font)
    img.save(str(png_path), format="PNG")

    # 2. OCR process_file
    ocr_result = process_file(str(png_path))
    assert ocr_result["status"] == "success"
    assert "Amoxicillin" in ocr_result["text"]
    assert ocr_result["confidence"] > 0

    # 3. Prescription parser
    parsed = extract_fields(ocr_result["text"], ocr_result["confidence"])
    assert parsed["medicine_name"] is not None
    assert "500" in str(parsed["strength"])
    assert "Twice daily" in str(parsed["frequency"])
    assert "7 days" in str(parsed["duration"])

    # 4. Upload prescription API endpoint
    with open(str(png_path), "rb") as f:
        res = client.post("/prescriptions/upload", files={"file": ("test_pytest_prescription.png", f, "image/png")})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    presc_id = data["id"]

    # 5. Confirm prescription API endpoint (JSON)
    confirm_payload = {
        "prescription_id": presc_id,
        "medicine_name": "Amoxicillin",
        "strength": "500mg",
        "frequency": "Twice daily",
        "duration": "7 days",
        "instructions": "Take after food with water"
    }
    res = client.post("/prescriptions/confirm", json=confirm_payload)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # 6. List prescriptions
    res = client.get("/prescriptions")
    assert res.status_code == 200
    assert len(res.json()) > 0

def test_auxiliary_services():
    assert browser_voice_support() is True
    assert "en" in speech_languages()
    assert translate_ui("dashboard", "en") == "Dashboard"
    assert translate_ui("dashboard", "te") != ""
    assert translate_ui("dashboard", "hi") != ""
