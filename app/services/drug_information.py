from datetime import datetime

LOCAL_DRUG_DATABASE = {
    "amoxicillin": {
        "name": "Amoxicillin",
        "purpose": "Commonly used to treat bacterial infections as directed by a healthcare professional.",
        "precautions": "Use only as prescribed. Tell your doctor or pharmacist about allergies or kidney disease.",
        "side_effects": "Nausea, diarrhea, rash, or an allergic reaction may occur in some people.",
        "storage": "Store in a cool, dry place away from direct sunlight and out of reach of children.",
        "source": "Demo medication information",
        "last_updated": "2026-08-18",
    },
    "paracetamol": {
        "name": "Paracetamol",
        "purpose": "Used to relieve pain and reduce fever as directed by a healthcare professional.",
        "precautions": "Do not exceed the labelled dose; inform your doctor if you have liver disease.",
        "side_effects": "Usually well tolerated, but some people may feel nausea or stomach discomfort.",
        "storage": "Store below 25°C in a cool, dry place away from moisture.",
        "source": "Demo medication information",
        "last_updated": "2026-08-18",
    },
    "cetirizine": {
        "name": "Cetirizine",
        "purpose": "Commonly used to help relieve allergy symptoms such as sneezing or itching.",
        "precautions": "Follow the product label and seek help if you feel unusually drowsy.",
        "side_effects": "Drowsiness, dry mouth, or tiredness may occur.",
        "storage": "Store in a closed container away from heat and sunlight.",
        "source": "Demo medication information",
        "last_updated": "2026-08-18",
    },
    "interactions": {
        ("amoxicillin", "paracetamol"): {
            "severity": "LOW",
            "explanation": "This combination is often used together, but dose and timing should be reviewed with a healthcare professional.",
            "source": "Demo medication information",
        },
        ("amoxicillin", "cetirizine"): {
            "severity": "LOW",
            "explanation": "No major interaction is commonly expected, but medical advice is still recommended for complex regimens.",
            "source": "Demo medication information",
        },
        ("paracetamol", "cetirizine"): {
            "severity": "LOW",
            "explanation": "No major interaction is commonly expected, but dose and timing should be reviewed if other medicines are being taken.",
            "source": "Demo medication information",
        },
    },
}


def get_medicine_info(name: str) -> dict:
    key = (name or "").strip().lower()
    if not key:
        return {
            "medicine_name": "",
            "purpose": "Information unavailable — consult a pharmacist or trusted medical source.",
            "precautions": "Information unavailable — consult a pharmacist or trusted medical source.",
            "side_effects": "Information unavailable — consult a pharmacist or trusted medical source.",
            "storage": "Information unavailable — consult a pharmacist or trusted medical source.",
            "source": "Demo medication information",
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d"),
        }

    record = LOCAL_DRUG_DATABASE.get(key)
    if record:
        return {
            "medicine_name": record["name"],
            "purpose": record["purpose"],
            "precautions": record["precautions"],
            "side_effects": record["side_effects"],
            "storage": record["storage"],
            "source": record.get("source", "Demo medication information"),
            "last_updated": record.get("last_updated", datetime.utcnow().strftime("%Y-%m-%d")),
        }

    return {
        "medicine_name": name,
        "purpose": "Information unavailable — consult a pharmacist or trusted medical source.",
        "precautions": "Information unavailable — consult a pharmacist or trusted medical source.",
        "side_effects": "Information unavailable — consult a pharmacist or trusted medical source.",
        "storage": "Information unavailable — consult a pharmacist or trusted medical source.",
        "source": "Demo medication information",
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d"),
    }
