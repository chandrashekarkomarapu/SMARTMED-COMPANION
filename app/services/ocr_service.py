from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from app.config.settings import settings

# Try to import optional dependencies
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import fitz
    FITZ_AVAILABLE = True
except ImportError:
    FITZ_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

try:
    from PIL import Image, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def _tesseract_available() -> bool:
    if not PYTESSERACT_AVAILABLE:
        return False
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False


def _preprocess_image(image: Any) -> Any:
    if not PIL_AVAILABLE or not CV2_AVAILABLE or not NUMPY_AVAILABLE:
        return image
    
    img = ImageOps.exif_transpose(image).convert("L")
    img = ImageOps.autocontrast(img)
    img = img.resize((img.width * 2, img.height * 2))
    arr = np.array(img)
    arr = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return Image.fromarray(arr)


def process_file(file_path: str) -> dict[str, Any]:
    lower = file_path.lower()
    try:
        if lower.endswith(".pdf"):
            return _ocr_pdf(file_path)
        if lower.endswith((".jpg", ".jpeg", ".png")):
            return _ocr_image(file_path)
        return {"text": "", "confidence": 0.0, "status": "error", "error": "Please upload a JPG, PNG, or PDF prescription."}
    except Exception as exc:
        return {"text": "", "confidence": 0.0, "status": "error", "error": f"Unable to read the prescription. {exc}"}


def _ocr_image(file_path: str) -> dict[str, Any]:
    if not PYTESSERACT_AVAILABLE or not PIL_AVAILABLE:
        return {
            "text": "",
            "confidence": 0.0,
            "status": "error",
            "error": "OCR functionality is not available. Please install required dependencies: pillow, pytesseract.",
        }
    
    if not _tesseract_available():
        return {
            "text": "",
            "confidence": 0.0,
            "status": "error",
            "error": "Tesseract OCR is not installed or configured. Please install Tesseract OCR for Windows and ensure the tesseract command is available on PATH.",
        }
    try:
        image = Image.open(file_path)
        processed = _preprocess_image(image)
        text = pytesseract.image_to_string(processed, config=f"--psm 6 -l {settings.OCR_LANGUAGE}")
        data = pytesseract.image_to_data(processed, config=f"--psm 6 -l {settings.OCR_LANGUAGE}", output_type=pytesseract.Output.DICT)
        conf_values = [int(value) for value in data.get("conf", []) if str(value).isdigit()]
        confidence = round(sum(conf_values) / len(conf_values), 2) if conf_values else 0.0
        return {"text": text.strip(), "confidence": confidence, "status": "success"}
    except Exception as exc:
        return {"text": "", "confidence": 0.0, "status": "error", "error": f"Unable to read the prescription image. {exc}"}


def _ocr_pdf(file_path: str) -> dict[str, Any]:
    if not PYTESSERACT_AVAILABLE or not FITZ_AVAILABLE:
        return {
            "text": "",
            "confidence": 0.0,
            "status": "error",
            "error": "PDF OCR functionality is not available. Please install required dependencies: pymupdf, pytesseract, pillow.",
        }
    
    if not _tesseract_available():
        return {
            "text": "",
            "confidence": 0.0,
            "status": "error",
            "error": "Tesseract OCR is not installed or configured. Please install Tesseract OCR for Windows and ensure the tesseract command is available on PATH.",
        }
    try:
        doc = fitz.open(file_path)
        chunks: list[str] = []
        confs: list[float] = []
        for page_index in range(doc.page_count):
            page = doc.load_page(page_index)
            image = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            temp_path = str(Path(file_path).with_name(f"{Path(file_path).stem}_{page_index}.png"))
            image.save(temp_path)
            result = _ocr_image(temp_path)
            if result.get("status") == "success":
                chunks.append(result["text"])
                confs.append(float(result.get("confidence", 0.0)))
            if os.path.exists(temp_path):
                os.remove(temp_path)
        text = "\n".join(chunks).strip()
        confidence = round(sum(confs) / len(confs), 2) if confs else 0.0
        if not text:
            return {"text": "", "confidence": 0.0, "status": "error", "error": "Unable to read the prescription PDF. Please try a clearer document."}
        return {"text": text, "confidence": confidence, "status": "success"}
    except Exception as exc:
        return {"text": "", "confidence": 0.0, "status": "error", "error": f"Unable to read the prescription PDF. {exc}"}


def extract_confidence_label(confidence: float | None) -> str:
    if confidence is None:
        return "Uncertain"
    if confidence >= 80:
        return "High confidence"
    if confidence >= 60:
        return "Moderate confidence"
    return "Uncertain OCR result — please verify."
