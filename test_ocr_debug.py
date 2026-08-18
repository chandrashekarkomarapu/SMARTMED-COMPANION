#!/usr/bin/env python
"""Debug and verification script for OCR functionality."""

import sys
import io
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=" * 70)
print("  SmartMed Companion - OCR Verification Test")
print("=" * 70)

# Test 1: Check dependencies
print("\n[TEST 1] Checking dependencies...")
try:
    import pytesseract
    print("  [OK] pytesseract imported successfully")
except ImportError as e:
    print(f"  [WARN] pytesseract not installed: {e}")

try:
    from PIL import Image, ImageDraw, ImageFont
    print("  [OK] PIL (Pillow) imported successfully")
except ImportError as e:
    print(f"  [FAIL] PIL not installed: {e}")
    sys.exit(1)

try:
    import cv2
    print("  [OK] OpenCV imported successfully")
except ImportError as e:
    print(f"  [WARN] OpenCV not installed: {e}")

try:
    import numpy as np
    print("  [OK] NumPy imported successfully")
except ImportError as e:
    print(f"  [WARN] NumPy not installed: {e}")

try:
    import pymupdf as fitz
    print("  [OK] PyMuPDF imported successfully")
except ImportError:
    try:
        import fitz
        print("  [OK] PyMuPDF (fitz) imported successfully")
    except ImportError as e:
        print(f"  [WARN] PyMuPDF not installed: {e}")

try:
    import winocr
    print("  [OK] WinOCR (Windows Native OCR) imported successfully")
except ImportError:
    print("  [INFO] winocr not installed")

# Test 2: Check OCR service
print("\n[TEST 2] Checking OCR service...")
try:
    from app.services.ocr_service import process_file, _ocr_image, _tesseract_available, _ocr_engine_available
    print("  [OK] OCR service imported successfully")
    
    tess_ok = _tesseract_available()
    engine_ok = _ocr_engine_available()
    print(f"  Tesseract Available: {tess_ok}")
    print(f"  OCR Engine Available: {engine_ok}")
    if not engine_ok:
        print("  [FAIL] No OCR engine available")
        sys.exit(1)
    else:
        print("  [OK] OCR Engine is ready")
except Exception as e:
    print(f"  [FAIL] Failed to import OCR service: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Check upload directory
print("\n[TEST 3] Checking upload directory...")
try:
    from app.utils.validators import get_upload_directory
    upload_dir = get_upload_directory()
    print(f"  [OK] Upload directory: {upload_dir}")
    print(f"  [OK] Directory exists: {upload_dir.exists()}")
except Exception as e:
    print(f"  [FAIL] Failed to get upload directory: {e}")
    sys.exit(1)

# Test 4: Create a test prescription image
print("\n[TEST 4] Creating test prescription image...")
try:
    test_img_path = upload_dir / "test_ocr_demo.png"
    img = Image.new('RGB', (600, 250), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        font_bold = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font = font_bold = ImageFont.load_default()
    
    draw.text((20, 20), "PRESCRIPTION", fill="black", font=font_bold)
    draw.text((20, 60), "Patient: John Doe", fill="black", font=font)
    draw.text((20, 100), "Medicine: Amoxicillin 500mg", fill="black", font=font)
    draw.text((20, 140), "Frequency: Twice daily", fill="black", font=font)
    draw.text((20, 180), "Duration: 7 days", fill="black", font=font)
    draw.text((20, 220), "Instructions: Take after food with water", fill="black", font=font)
    
    img.save(str(test_img_path))
    print(f"  [OK] Test image created: {test_img_path}")
except Exception as e:
    print(f"  [FAIL] Failed to create test image: {e}")
    sys.exit(1)

# Test 5: Test OCR process_file on the created image
print("\n[TEST 5] Testing OCR engine output on demo image...")
try:
    result = process_file(str(test_img_path))
    print(f"  Status: {result.get('status')}")
    if result.get('status') == 'success':
        print(f"  [OK] OCR successful!")
        print(f"  Extracted text:\n---\n{result.get('text', 'N/A')}\n---")
        print(f"  Confidence: {result.get('confidence', 'N/A')}%")
        
        # Also test field extraction
        from app.services.prescription_parser import extract_fields
        parsed = extract_fields(result.get('text', ''), result.get('confidence', 0.0))
        print(f"  Parsed Fields: {parsed}")
        assert parsed.get("medicine_name"), "Medicine name should be extracted"
        print("  [OK] Field extraction verified successfully")
    else:
        print(f"  [FAIL] OCR failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)
except Exception as e:
    print(f"  [FAIL] Exception during OCR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Test upload via FastAPI TestClient
print("\n[TEST 6] Testing prescription upload endpoint...")
try:
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    with open(str(test_img_path), "rb") as f:
        response = client.post("/prescriptions/upload", files={"file": ("test_ocr_demo.png", f, "image/png")})
    
    print(f"  Response status: {response.status_code}")
    data = response.json()
    
    if response.status_code == 200 and data.get("status") == "success":
        print("  [OK] Prescription upload & OCR API successful!")
        print(f"  Prescription ID: {data.get('id')}")
        print(f"  Confidence: {data.get('confidence')}%")
        print(f"  Parsed Medicine: {data.get('parsed', {}).get('medicine_name')}")
        print(f"  Parsed Frequency: {data.get('parsed', {}).get('frequency')}")
    else:
        print(f"  [FAIL] Upload failed: {data}")
        sys.exit(1)
except Exception as e:
    print(f"  [FAIL] Exception during API test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("  ALL OCR AND ENDPOINT TESTS PASSED SUCCESSFULLY!")
print("=" * 70)
sys.exit(0)
