import io
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pymupdf as fitz
from fastapi.testclient import TestClient

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from app.main import app
from app.database.database import init_db
from app.database.seed import seed_demo_data
from app.services.ocr_service import process_file
from app.services.prescription_parser import extract_fields
from app.services.medication_safety import build_safety_report, check_interactions, detect_duplicate_medicines
from app.services.drug_information import get_medicine_info
from app.services.speech_service import browser_voice_support, speech_languages
from app.services.translation_service import translate_ui

init_db()
seed_demo_data()
client = TestClient(app)

tests_run = 0
tests_passed = 0
tests_failed = 0
results = []

def record(name: str, passed: bool, detail: str = ""):
    global tests_run, tests_passed, tests_failed
    tests_run += 1
    if passed:
        tests_passed += 1
        results.append((name, "PASS", detail))
        print(f"  [PASS] {name}" + (f" - {detail}" if detail else ""))
    else:
        tests_failed += 1
        results.append((name, "FAIL", detail))
        print(f"  [FAIL] {name}" + (f" - {detail}" if detail else ""))

print("=" * 80)
print("  SMARTMED COMPANION - FULL SYSTEM VERIFICATION & ENDPOINT AUDIT")
print("=" * 80)

# SECTION 1: CORE / SYSTEM ENDPOINTS
print("\n--- SECTION 1: Core & System Endpoints ---")
res = client.get("/health")
record("GET /health", res.status_code == 200 and res.json().get("status") == "ok", f"Status: {res.status_code}")

res = client.get("/", follow_redirects=False)
record("GET / (Root redirect to /dashboard)", res.status_code in [301, 302, 307] and "/dashboard" in res.headers.get("location", ""), f"Status: {res.status_code}")

res = client.get("/docs")
record("GET /docs (Swagger UI)", res.status_code == 200 and "swagger" in res.text.lower(), f"Status: {res.status_code}")

res = client.get("/openapi.json")
record("GET /openapi.json", res.status_code == 200 and "paths" in res.json(), f"Status: {res.status_code}")

# SECTION 2: AUTHENTICATION ENDPOINTS
print("\n--- SECTION 2: Authentication Endpoints ---")
res = client.post("/auth/login", json={"username": "alex", "password": "demo-password"})
record("POST /auth/login (Valid credentials)", res.status_code == 200 and res.json().get("status") == "demo", f"Response: {res.json().get('message')}")

res = client.post("/auth/login", json={"username": "", "password": ""})
record("POST /auth/login (Empty credentials validation)", res.status_code == 400, f"Status: {res.status_code}")

res = client.post("/auth/register", json={"username": "newuser", "full_name": "New User", "password": "password123"})
record("POST /auth/register (Valid registration)", res.status_code == 200 and res.json().get("status") == "demo", f"Response: {res.json().get('message')}")

res = client.post("/auth/register", json={"username": "", "full_name": "New User", "password": ""})
record("POST /auth/register (Empty validation)", res.status_code == 400, f"Status: {res.status_code}")

res = client.post("/auth/logout")
record("POST /auth/logout", res.status_code == 200, f"Response: {res.json().get('message')}")

# SECTION 3: HTML VIEWS / UI PAGES
print("\n--- SECTION 3: HTML Pages & Jinja2 Templates ---")
res = client.get("/dashboard")
record("GET /dashboard (Dashboard UI)", res.status_code == 200 and "Alex Johnson" in res.text and "SmartMed" in res.text, f"Size: {len(res.content)} bytes")

res = client.get("/scanner")
record("GET /scanner (Scanner UI)", res.status_code == 200 and "Prescription scanner" in res.text, f"Size: {len(res.content)} bytes")

res = client.get("/medicines")
record("GET /medicines (Medicines UI)", res.status_code == 200 and "Amoxicillin" in res.text, f"Size: {len(res.content)} bytes")

res = client.get("/reminders")
record("GET /reminders (Reminders UI)", res.status_code == 200 and "Reminders" in res.text, f"Size: {len(res.content)} bytes")

res = client.get("/safety")
record("GET /safety (Safety UI)", res.status_code == 200 and "Safety" in res.text, f"Size: {len(res.content)} bytes")

res = client.get("/emergency")
record("GET /emergency (Emergency UI)", res.status_code == 200 and "Emergency" in res.text, f"Size: {len(res.content)} bytes")

# SECTION 4: MEDICINES CRUD & SEARCH API
print("\n--- SECTION 4: Medicines API ---")
res = client.get("/medicines/search?q=Amox")
record("GET /medicines/search?q=Amox", res.status_code == 200 and any(m["name"] == "Amoxicillin" for m in res.json()), f"Found: {len(res.json())} matches")

new_med = {
    "name": "Ibuprofen",
    "strength": "400 mg",
    "frequency": "Twice daily",
    "duration": "3 days",
    "instructions": "After food",
    "source": "Doctor prescription"
}
res = client.post("/medicines", json=new_med)
created_med_id = res.json().get("medicine", {}).get("id") if res.status_code == 201 else None
record("POST /medicines (Create Medicine)", res.status_code == 201 and created_med_id is not None, f"Created ID: {created_med_id}")

if created_med_id:
    res = client.get(f"/medicines/{created_med_id}")
    record(f"GET /medicines/{created_med_id} (Read Medicine)", res.status_code == 200 and res.json().get("name") == "Ibuprofen", f"Name: {res.json().get('name')}")
    res = client.put(f"/medicines/{created_med_id}", json={"strength": "600 mg", "frequency": "Once daily"})
    record(f"PUT /medicines/{created_med_id} (Update Medicine)", res.status_code == 200 and res.json().get("status") == "success", f"Response: {res.json().get('message')}")
    res = client.delete(f"/medicines/{created_med_id}")
    record(f"DELETE /medicines/{created_med_id} (Delete Medicine)", res.status_code == 200 and res.json().get("status") == "success", f"Response: {res.json().get('message')}")
    res404 = client.get(f"/medicines/{created_med_id}")
    record(f"GET /medicines/{created_med_id} after DELETE returns 404", res404.status_code == 404, "Correct 404 returned")

# SECTION 5: REMINDERS API
print("\n--- SECTION 5: Reminders API ---")
res = client.get("/reminders/list")
record("GET /reminders/list", res.status_code == 200 and isinstance(res.json(), list), f"Total reminders: {len(res.json())}")

new_rem = {
    "medicine_name": "Metformin",
    "time": "09:00",
    "frequency": "Twice daily",
    "notes": "With breakfast"
}
res = client.post("/reminders", json=new_rem)
created_rem_id = res.json().get("reminder", {}).get("id") if res.status_code == 201 else None
record("POST /reminders (Create Reminder)", res.status_code == 201 and created_rem_id is not None, f"Created ID: {created_rem_id}")

if created_rem_id:
    res = client.put(f"/reminders/{created_rem_id}", json={"time": "09:30", "notes": "After breakfast"})
    record(f"PUT /reminders/{created_rem_id} (Update Reminder)", res.status_code == 200 and res.json().get("status") == "success", f"Response: {res.json().get('message')}")
    res = client.post(f"/reminders/{created_rem_id}/taken")
    record(f"POST /reminders/{created_rem_id}/taken", res.status_code == 200 and res.json().get("status") == "success", f"Response: {res.json().get('message')}")
    res = client.post(f"/reminders/{created_rem_id}/missed")
    record(f"POST /reminders/{created_rem_id}/missed", res.status_code == 200 and res.json().get("status") == "success", f"Response: {res.json().get('message')}")
    res = client.delete(f"/reminders/{created_rem_id}")
    record(f"DELETE /reminders/{created_rem_id}", res.status_code == 200 and res.json().get("status") == "success", f"Response: {res.json().get('message')}")

# SECTION 6: MEDICATION SAFETY & DRUG INFORMATION
print("\n--- SECTION 6: Medication Safety & Interactions ---")
res = client.post("/safety/check", json=["Amoxicillin", "Paracetamol"])
record("POST /safety/check (Interaction test)", res.status_code == 200 and "report" in res.json(), f"Status: {res.json().get('report', {}).get('status')}")

report = build_safety_report(["Amoxicillin", "amoxicillin", "Paracetamol"])
has_dup = len(report.get("duplicate_names", [])) > 0
record("Medication Safety: Duplicate Drug Detection", has_dup, f"Duplicates: {report.get('duplicate_names')}")

info = get_medicine_info("amoxicillin")
record("Drug Info: Database Lookup (Amoxicillin)", info.get("medicine_name") == "Amoxicillin" and "bacterial" in info.get("purpose", "").lower(), f"Purpose: {info.get('purpose')[:50]}...")

# SECTION 7: OCR ENGINE & PRESCRIPTION PROCESSING WITH DEMO IMAGES & PDF
print("\n--- SECTION 7: OCR Engine & Multimodal Tests (PNG, JPG, PDF) ---")
upload_dir = Path("uploads/prescriptions")
upload_dir.mkdir(parents=True, exist_ok=True)

def create_demo_prescription_image(filename: str, img_format: str = "PNG") -> Path:
    img_path = upload_dir / filename
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
    img.save(str(img_path), format=img_format)
    return img_path

def create_demo_prescription_pdf(filename: str) -> Path:
    pdf_path = upload_dir / filename
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    text = (
        "PRESCRIPTION REPORT\n\n"
        "Clinic: Smart Health Clinic\n"
        "Patient: Alex Johnson\n"
        "Medicine: Cetirizine 10mg\n"
        "Frequency: Once daily\n"
        "Duration: 14 days\n"
        "Instructions: Take before bedtime\n"
    )
    page.insert_text((50, 80), text, fontsize=16)
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path

png_file = create_demo_prescription_image("demo_prescription_test.png", "PNG")
png_ocr = process_file(str(png_file))
png_ok = png_ocr.get("status") == "success" and "Amoxicillin" in png_ocr.get("text", "")
record("OCR Engine: Process PNG Demo Image", png_ok, f"Confidence: {png_ocr.get('confidence')}% | Text length: {len(png_ocr.get('text', ''))}")

jpg_file = create_demo_prescription_image("demo_prescription_test.jpg", "JPEG")
jpg_ocr = process_file(str(jpg_file))
jpg_ok = jpg_ocr.get("status") == "success" and "Amoxicillin" in jpg_ocr.get("text", "")
record("OCR Engine: Process JPG Demo Image", jpg_ok, f"Confidence: {jpg_ocr.get('confidence')}% | Text length: {len(jpg_ocr.get('text', ''))}")

pdf_file = create_demo_prescription_pdf("demo_prescription_test.pdf")
pdf_ocr = process_file(str(pdf_file))
pdf_ok = pdf_ocr.get("status") == "success" and "Cetirizine" in pdf_ocr.get("text", "")
record("OCR Engine: Process PDF Demo Document", pdf_ok, f"Confidence: {pdf_ocr.get('confidence')}% | Extracted: {pdf_ocr.get('text', '')[:40]}...")

parsed_fields = extract_fields(png_ocr.get("text", ""), png_ocr.get("confidence", 0.0))
parser_ok = (
    parsed_fields.get("medicine_name") is not None
    and "500" in str(parsed_fields.get("strength", ""))
    and "daily" in str(parsed_fields.get("frequency", "")).lower()
    and "7 days" in str(parsed_fields.get("duration", ""))
)
record("Prescription Parser: Field Extraction", parser_ok, f"Parsed: {parsed_fields}")

with open(str(png_file), "rb") as f:
    res = client.post("/prescriptions/upload", files={"file": ("demo_prescription.png", f, "image/png")})
upload_ok = res.status_code == 200 and res.json().get("status") == "success"
presc_id = res.json().get("id") if upload_ok else None
record("POST /prescriptions/upload (File Upload + OCR + Parser + DB Save)", upload_ok, f"Prescription ID: {presc_id}, Confidence: {res.json().get('confidence')}%")

if presc_id:
    confirm_json = {
        "prescription_id": presc_id,
        "medicine_name": "Amoxicillin",
        "strength": "500mg",
        "frequency": "Twice daily",
        "duration": "7 days",
        "instructions": "Take after food with water"
    }
    res = client.post("/prescriptions/confirm", json=confirm_json)
    record("POST /prescriptions/confirm (JSON Payload)", res.status_code == 200 and res.json().get("status") == "success", f"Status: {res.json().get('message')}")

    confirm_form = {
        "prescription_id": str(presc_id),
        "medicine_name": "Amoxicillin",
        "strength": "500mg",
        "frequency": "Twice daily",
        "duration": "7 days",
        "instructions": "Take after food with water"
    }
    res = client.post("/prescriptions/confirm", data=confirm_form)
    record("POST /prescriptions/confirm (Form Data Payload)", res.status_code == 200 and res.json().get("status") == "success", f"Status: {res.json().get('message')}")

res = client.get("/prescriptions")
record("GET /prescriptions (List prescriptions)", res.status_code == 200 and isinstance(res.json(), list) and len(res.json()) > 0, f"Found {len(res.json())} prescription records")

# SECTION 8: AUXILIARY SERVICES
print("\n--- SECTION 8: Auxiliary Services ---")
voice_ok = browser_voice_support() and "en" in speech_languages()
record("Speech Service: Browser Support & Languages", voice_ok, f"Languages: {speech_languages()}")

tr_en = translate_ui("dashboard", "en")
tr_te = translate_ui("dashboard", "te")
tr_hi = translate_ui("dashboard", "hi")
tr_ok = tr_en != "" and tr_te != "" and tr_hi != ""
record("Translation Service: Multi-language Support (EN, TE, HI)", tr_ok, f"EN: '{tr_en}', TE: '{tr_te}', HI: '{tr_hi}'")

print("\n" + "=" * 80)
print(f"  TOTAL TESTS RUN   : {tests_run}")
print(f"  TESTS PASSED      : {tests_passed}")
print(f"  TESTS FAILED      : {tests_failed}")
print(f"  SUCCESS RATE      : {(tests_passed / tests_run * 100):.1f}%")
print("=" * 80)

if tests_failed == 0:
    print("\n  [SUCCESS] All endpoints, services, and OCR functionalities are working properly!\n")
    sys.exit(0)
else:
    print(f"\n  [ERROR] {tests_failed} test(s) failed.\n")
    sys.exit(1)
