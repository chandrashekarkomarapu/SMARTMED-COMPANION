from app.services.drug_information import LOCAL_DRUG_DATABASE


def detect_duplicate_medicines(medicine_names: list[str]) -> list[str]:
    seen = set()
    duplicates = set()
    for name in medicine_names:
        normalized = (name or "").strip().lower()
        if not normalized:
            continue
        if normalized in seen:
            duplicates.add(name.strip())
        else:
            seen.add(normalized)
    return sorted(duplicates, key=str.lower)


def classify_severity(level: str) -> str:
    value = (level or "LOW").upper()
    if value in {"HIGH", "CRITICAL"}:
        return "HIGH"
    if value == "MODERATE":
        return "MODERATE"
    return "LOW"


def check_interactions(medicine_names: list[str]) -> dict:
    unique_names = [name.strip() for name in medicine_names if name and name.strip()]
    if len(unique_names) < 2:
        return {"alerts": [], "status": "ok", "message": "No potential interaction check needed for a single medicine."}

    alerts = []
    for index, first in enumerate(unique_names):
        for second in unique_names[index + 1:]:
            pair = tuple(sorted((first.lower(), second.lower())))
            interaction = LOCAL_DRUG_DATABASE.get("interactions", {}).get(pair)
            if interaction:
                alerts.append({
                    "severity": classify_severity(interaction.get("severity", "LOW")),
                    "medicines": [first, second],
                    "explanation": interaction.get("explanation", "Interaction information could not be verified. Please consult a pharmacist."),
                    "source": interaction.get("source", "Demo medication information"),
                    "recommendation": "Please contact your doctor or pharmacist before making changes to your medicines.",
                })

    if alerts:
        return {"alerts": alerts, "status": "warning", "message": "Medication safety checks completed."}

    return {
        "alerts": [{
            "severity": "LOW",
            "medicines": unique_names,
            "explanation": "Interaction information could not be verified. Please consult a pharmacist.",
            "source": "Demo medication information",
            "recommendation": "Please contact your doctor or pharmacist before making changes to your medicines.",
        }],
        "status": "warning",
        "message": "Interaction information could not be verified. Please consult a pharmacist.",
    }


def build_safety_report(medicine_names: list[str]) -> dict:
    duplicates = detect_duplicate_medicines(medicine_names)
    interaction_result = check_interactions(medicine_names)
    alerts = interaction_result.get("alerts", [])

    if duplicates:
        alerts.insert(0, {
            "severity": "MODERATE",
            "medicines": duplicates,
            "explanation": "Possible duplicate medicine detected.",
            "source": "Demo medication information",
            "recommendation": "Please contact your doctor or pharmacist before making changes to your medicines.",
        })

    return {
        "duplicate_names": duplicates,
        "interaction_alerts": alerts,
        "status": "warning" if alerts else "ok",
        "message": "Safety review completed.",
    }
