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
    import pymupdf as fitz
    FITZ_AVAILABLE = True
except ImportError:
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
    import winocr
    WINOCR_AVAILABLE = True
except ImportError:
    WINOCR_AVAILABLE = False

try:
    from PIL import Image, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

COMMON_TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
]


def _configure_tesseract() -> bool:
    if not PYTESSERACT_AVAILABLE:
        return False
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        pass

    for path in COMMON_TESSERACT_PATHS:
        if os.path.exists(path):
            try:
                pytesseract.pytesseract.tesseract_cmd = path
                pytesseract.get_tesseract_version()
                return True
            except Exception:
                continue
    return False


def _tesseract_available() -> bool:
    return _configure_tesseract()


def _ocr_engine_available() -> bool:
    return _tesseract_available() or WINOCR_AVAILABLE


def _preprocess_image(image: Any) -> Any:
    """
    Preprocess image for better OCR accuracy.
    Applies EXIF rotation, grayscale conversion, contrast enhancement, and thresholding.
    """
    if not PIL_AVAILABLE or not CV2_AVAILABLE or not NUMPY_AVAILABLE:
        return image

    try:
        # Fix image orientation based on EXIF data
        img = ImageOps.exif_transpose(image).convert("L")

        # Enhance contrast for better text visibility
        img = ImageOps.autocontrast(img)

        # Upscale image to improve OCR accuracy
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)

        # Convert to numpy array for OpenCV processing
        arr = np.array(img)

        # Apply binary thresholding with Otsu's method for binarization
        arr = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Convert back to PIL Image
        return Image.fromarray(arr)
    except Exception as exc:
        from app.utils.logger import logger
        logger.warning(f"Image preprocessing failed: {exc}. Proceeding with original image.")
        return image


def process_file(file_path: str) -> dict[str, Any]:
    """
    Process a file (PDF or image) and extract text using OCR.

    Args:
        file_path: Path to the file to process

    Returns:
        Dict with keys: text, confidence, status, error (if applicable)
    """
    from app.utils.logger import logger

    file = Path(file_path)
    if not file.exists():
        logger.error(f"File not found: {file_path}")
        return {"text": "", "confidence": 0.0, "status": "error", "error": f"File not found: {file_path}"}

    if file.stat().st_size == 0:
        logger.error(f"File is empty: {file_path}")
        return {"text": "", "confidence": 0.0, "status": "error", "error": "Uploaded file is empty."}

    logger.info(f"Processing file: {file_path} (Size: {file.stat().st_size} bytes)")

    lower = file_path.lower()
    try:
        if lower.endswith(".pdf"):
            logger.info("Processing as PDF")
            return _ocr_pdf(file_path)
        elif lower.endswith((".jpg", ".jpeg", ".png")):
            logger.info("Processing as image")
            return _ocr_image(file_path)
        else:
            error = "Please upload a JPG, PNG, or PDF prescription."
            logger.warning(f"Invalid file type: {file_path}")
            return {"text": "", "confidence": 0.0, "status": "error", "error": error}
    except Exception as exc:
        logger.exception(f"Error processing file {file_path}: {exc}")
        return {"text": "", "confidence": 0.0, "status": "error", "error": f"Unable to read the prescription. {exc}"}


def _run_winocr(img: Any, lang: str = "en") -> dict:
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is not None and loop.is_running():
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(winocr.recognize_pil_sync, img, lang)
            return future.result()
    else:
        return winocr.recognize_pil_sync(img, lang)


def _ocr_image(file_path: str) -> dict[str, Any]:
    """
    Extract text from an image file using Tesseract or WinOCR.

    Args:
        file_path: Path to the image file

    Returns:
        Dict with keys: text, confidence, status, error (if applicable)
    """
    from app.utils.logger import logger

    if not PIL_AVAILABLE:
        error = "Image processing library (Pillow) is not installed."
        logger.error(error)
        return {"text": "", "confidence": 0.0, "status": "error", "error": error}

    if not _ocr_engine_available():
        error = "No OCR engine is available. Please ensure Tesseract OCR or Windows OCR dependencies are installed."
        logger.error(error)
        return {"text": "", "confidence": 0.0, "status": "error", "error": error}

    try:
        logger.info(f"Opening image: {file_path}")
        image = Image.open(file_path)

        if image.width < 100 or image.height < 100:
            logger.warning(f"Image too small: {image.width}x{image.height}.")

        # 1. Try Tesseract OCR if available
        if _tesseract_available():
            try:
                processed = _preprocess_image(image)
                text = pytesseract.image_to_string(processed, config=f"--psm 6 -l {settings.OCR_LANGUAGE}")
                data = pytesseract.image_to_data(processed, config=f"--psm 6 -l {settings.OCR_LANGUAGE}", output_type=pytesseract.Output.DICT)
                conf_values = [float(value) for value in data.get("conf", []) if str(value).strip().replace(".", "", 1).isdigit() and float(value) >= 0]
                confidence = round(sum(conf_values) / len(conf_values), 2) if conf_values else 0.0
                if text.strip():
                    logger.info(f"Tesseract OCR completed. Length: {len(text)}, confidence: {confidence}%")
                    return {"text": text.strip(), "confidence": confidence, "status": "success"}
                logger.warning("Tesseract returned no text; trying Windows OCR.")
            except Exception as exc:
                logger.warning(f"Tesseract failed: {exc}; trying Windows OCR.")

        # 2. Try WinOCR (Windows Native OCR) fallback
        if WINOCR_AVAILABLE:
            lang_code = settings.OCR_LANGUAGE if settings.OCR_LANGUAGE in ["en", "en-US"] else "en"
            # Try with preprocessed image first, then fallback to original if empty
            processed = _preprocess_image(image)
            result = _run_winocr(processed, lang_code)
            lines = [line.get("text", "").strip() for line in result.get("lines", []) if line.get("text", "").strip()]
            if not lines:
                # Try original image without binarization
                result = _run_winocr(image, lang_code)
                lines = [line.get("text", "").strip() for line in result.get("lines", []) if line.get("text", "").strip()]

            text = "\n".join(lines).strip() if lines else result.get("text", "").strip()
            # Estimate confidence based on recognized words and line structure
            confidence = 92.0 if len(lines) >= 2 else (80.0 if text else 0.0)
            logger.info(f"WinOCR completed. Length: {len(text)}, confidence: {confidence}%")
            return {"text": text, "confidence": confidence, "status": "success"}

        return {"text": "", "confidence": 0.0, "status": "error", "error": "No OCR engine available."}

    except FileNotFoundError:
        error = f"Image file not found: {file_path}"
        logger.error(error)
        return {"text": "", "confidence": 0.0, "status": "error", "error": error}
    except Exception as exc:
        error = f"Unable to read the prescription image. {exc}"
        logger.exception(f"OCR image processing error: {error}")
        return {"text": "", "confidence": 0.0, "status": "error", "error": error}


def _ocr_pdf(file_path: str) -> dict[str, Any]:
    """
    Extract text from a PDF file using OCR on rendered pages.

    Args:
        file_path: Path to the PDF file

    Returns:
        Dict with keys: text, confidence, status, error (if applicable)
    """
    from app.utils.logger import logger

    if not FITZ_AVAILABLE:
        error = "PDF OCR functionality is not available. PyMuPDF is not installed."
        logger.error(error)
        return {"text": "", "confidence": 0.0, "status": "error", "error": error}

    try:
        logger.info(f"Opening PDF: {file_path}")
        doc = fitz.open(file_path)
        logger.info(f"PDF has {doc.page_count} pages")

        chunks: list[str] = []
        confs: list[float] = []

        for page_index in range(doc.page_count):
            try:
                page = doc.load_page(page_index)
                page_text = page.get_text("text").strip()
                if page_text:
                    chunks.append(page_text)
                    confs.append(100.0)
                    continue

                if not _ocr_engine_available():
                    continue
                image = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                temp_path = str(Path(file_path).with_name(f"{Path(file_path).stem}_{page_index}.png"))
                image.save(temp_path)

                result = _ocr_image(temp_path)
                if result.get("status") == "success":
                    chunks.append(result["text"])
                    confs.append(float(result.get("confidence", 0.0)))

                if os.path.exists(temp_path):
                    os.remove(temp_path)

            except Exception as exc:
                logger.exception(f"Error processing PDF page {page_index + 1}: {exc}")
                continue

        text = "\n".join(chunks).strip()
        confidence = round(sum(confs) / len(confs), 2) if confs else 0.0

        if not text:
            error = "Unable to read the prescription PDF. Please try a clearer document."
            logger.warning(error)
            return {"text": "", "confidence": 0.0, "status": "error", "error": error}

        logger.info(f"PDF OCR completed. Total text length: {len(text)}, average confidence: {confidence}%")
        return {"text": text, "confidence": confidence, "status": "success"}

    except FileNotFoundError:
        error = f"PDF file not found: {file_path}"
        logger.error(error)
        return {"text": "", "confidence": 0.0, "status": "error", "error": error}
    except Exception as exc:
        error = f"Unable to read the prescription PDF. {exc}"
        logger.exception(f"PDF processing error: {error}")
        return {"text": "", "confidence": 0.0, "status": "error", "error": error}


def extract_confidence_label(confidence: float | None) -> str:
    if confidence is None:
        return "Uncertain"
    if confidence >= 80:
        return "High confidence"
    if confidence >= 60:
        return "Moderate confidence"
    return "Uncertain OCR result — please verify."
