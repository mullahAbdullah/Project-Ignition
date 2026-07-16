LEAD_WEIGHTS = {
    "budget": 25,
    "decision_maker": 20,
    "timeline": 20,
    "company": 10,
    "employees": 10,
    "goal": 10,
    "industry": 5,
}


def analyze_lead(profile):
    score = 0

    missing = []
    collected = []

    for field, weight in LEAD_WEIGHTS.items():

        value = profile.get(field)

        if value:
            score += weight
            collected.append(field)
        else:
            missing.append(field)

    if score >= 80:
        quality = "High"

    elif score >= 50:
        quality = "Medium"

    else:
        quality = "Low"

    return {
        "score": score,
        "quality": quality,
        "missing": missing,
        "collected": collected,
    }