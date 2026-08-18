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

    def labeled_value(labels):
        label_pattern = "|".join(labels)
        match = re.search(rf"^\s*(?:{label_pattern})\s*:\s*(.+?)\s*$", text, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else None

    medicine_name = find([
        r"(?:medicine|medicines|medication|drug|rx)\s*:?\s*([A-Za-z][A-Za-z .-]{2,60}?)(?=\s+[0-9]+\s*(?:mg|mcg|g|ml|iu)\b|\s*$)",
        r"^\s*([A-Za-z][A-Za-z .-]{2,60}?)(?=\s+[0-9]+\s*(?:mg|mcg|g|ml|iu)\b)",
    ])
    strength = find([
        r"(?:strength|dose)\s*:?\s*([0-9]+\s*(?:mg|mcg|g|ml|iu))",
        r"([0-9]+(?:\.\d+)?\s*(?:mg|mcg|g|ml|iu)(?:\s*/\s*[0-9]+\s*(?:ml|g))?)",
    ])
    strength = strength or (re.search(r"[0-9]+(?:\.\d+)?\s*(?:mg|mcg|g|ml|iu)(?:\s*/\s*[0-9]+\s*(?:ml|g))?", labeled_value(["medicine", "medicines", "medication", "drug", "rx"]) or "", re.IGNORECASE) or [None])[0]
    frequency_value = find([
        r"(?:frequency|dosage)\s*:?\s*([A-Za-z0-9 /,.-]+(?:daily|weekly|twice|once|three|times|hour|hours))",
        r"(once daily|twice daily|three times daily|daily|weekly|every\s+[0-9]+\s+hours?|OD|BD|TDS|QID|BID)",
    ])
    frequency_value = frequency_value or labeled_value(["frequency", "dosage", "schedule"])
    duration = find([
        r"(?:duration|for)\s*:?\s*([0-9]+\s*(?:days|day|weeks|week|months|month))",
        r"([0-9]+\s*(?:days|day|weeks|week|months|month))",
    ])
    duration = duration or labeled_value(["duration", "length"])
    instructions = find([
        r"(?:instructions|instruction|directions)\s*:?\s*(.+?)(?:\n|$)",
        r"(after food|before food|with water|empty stomach|before bedtime|after meals?|before meals?)",
    ])
    instructions = instructions or labeled_value(["instructions", "instruction", "directions"])

    if not medicine_name:
        for line in text.splitlines():
            cleaned = line.strip()
            dose_match = re.search(r"\b[0-9]+\s*(?:mg|mcg|g|ml|iu)\b", cleaned, re.IGNORECASE)
            if dose_match:
                candidate = re.sub(r"^(?:rx|medicine|medication|drug)\s*:?\s*", "", cleaned, flags=re.IGNORECASE)
                candidate = candidate[:dose_match.start()].strip(" :-")
                if len(candidate) > 2 and re.search(r"[A-Za-z]", candidate):
                    medicine_name = candidate
                    break

    if not medicine_name:
        ignored_prefixes = (
            "medical prescription", "prescription", "doctor", "patient", "clinic",
            "hospital", "date", "dose", "frequency", "duration", "instruction",
            "lot", "exp", "filed by", "used", "address",
        )
        for line in text.splitlines():
            cleaned = line.strip()
            if (
                len(cleaned) > 2
                and not cleaned[0].isdigit()
                and not cleaned.lower().startswith(ignored_prefixes)
                and not re.fullmatch(r"[\W_]+", cleaned)
                and not re.search(r"\b(?:prescription|report|clinic|hospital)\b", cleaned, re.IGNORECASE)
            ):
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
