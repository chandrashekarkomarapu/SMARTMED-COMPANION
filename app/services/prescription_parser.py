import re


def extract_fields(ocr_text: str | None, confidence: float | None = 0.0) -> dict:
    text = (ocr_text or "").strip()
    if not text:
        return {
            "medicine_name": None,
            "strength": None,
            "frequency": "Uncertain",
            "duration": None,
            "instructions": None,
            "confidence": float(confidence or 0.0),
        }

    def find(patterns):
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                value = match.group(1).strip()
                if value:
                    return value
        return None

    medicine_name = find([
        r"(?:medicine|medicines|drug)\s*:?\s*([A-Za-z][A-Za-z0-9 .-]{2,40})",
        r"^\s*([A-Z][A-Za-z0-9 .-]{2,40})\s*$",
    ])
    strength = find([
        r"(?:strength|dose)\s*:?\s*([0-9]+\s*(?:mg|mcg|g|ml|iu))",
        r"([0-9]+\s*(?:mg|mcg|g|ml|iu))",
    ])
    frequency_value = find([
        r"(?:frequency|take|dosage)\s*:?\s*([A-Za-z0-9 /,.-]+(?:daily|weekly|twice|once|three|times|hour|hours))",
        r"(once daily|twice daily|three times daily|daily|weekly|every [0-9]+ hours|OD|BD|TDS)",
    ])
    duration = find([
        r"(?:duration|for)\s*:?\s*([0-9]+\s*(?:day|days|week|weeks|month|months))",
        r"([0-9]+\s*(?:day|days|week|weeks|month|months))",
    ])
    instructions = find([
        r"(?:instructions|instruction|take)\s*:?\s*([A-Za-z0-9 ,.-]+(?:after food|before food|with water|empty stomach|morning|night))",
        r"(after food|before food|with water|empty stomach)",
    ])

    if not medicine_name:
        for line in text.splitlines():
            cleaned = line.strip()
            if len(cleaned) > 2 and not re.fullmatch(r"[\W_]+", cleaned):
                medicine_name = cleaned
                break

    result = {
        "medicine_name": medicine_name,
        "strength": strength,
        "frequency": frequency_value or "Uncertain",
        "duration": duration,
        "instructions": instructions,
        "confidence": float(confidence or 0.0),
    }

    if confidence is not None and confidence < 60:
        result["frequency"] = "Uncertain"
    return result
