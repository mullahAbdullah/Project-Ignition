import re
from app.ai_client import extract_lead_info_ai

FIELDS = {
    "company": None,
    "industry": None,
    "budget": None,
    "timeline": None,
    "employees": None,
    "decision_maker": None,
    "goal": None,
}


def extract_lead_info(messages):
    try:
        profile = extract_lead_info_ai(messages)

        return profile
    except Exception as e:
        raise e

    profile = FIELDS.copy()

    user_messages = [
        message["content"]
        for message in messages
        if message["role"] == "user"
    ]

    text = " ".join(user_messages)

    # -----------------------------
    # Company
    # -----------------------------

    company_patterns = [
        r"(?:company|business|organization|organisation)\s+(?:is\s+)?([A-Za-z0-9&.,' -]+)",
        r"(?:from|at)\s+([A-Za-z0-9&.,' -]+)",
        r"(?:ceo|founder|owner|director|manager)\s+of\s+([A-Za-z0-9&.,' -]+)",
    ]

    for pattern in company_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            profile["company"] = match.group(1).strip()
            break

    # -----------------------------
    # Industry
    # -----------------------------

    industries = [
        "software",
        "saas",
        "real estate",
        "healthcare",
        "finance",
        "marketing",
        "construction",
        "education",
        "retail",
        "manufacturing",
        "consulting",
        "ecommerce",
        "technology",
    ]

    for industry in industries:
        if industry.lower() in text.lower():
            profile["industry"] = industry.title()
            break

    # -----------------------------
    # Budget
    # -----------------------------

    budget = re.search(
        r"\$[\d,]+|[\d,]+\s*(?:usd|dollars)",
        text,
        re.IGNORECASE,
    )

    if budget:
        profile["budget"] = budget.group(0)

    # -----------------------------
    # Employees
    # -----------------------------

    employees = re.search(
        r"(\d+)\s+(?:employees|staff|workers|people)",
        text,
        re.IGNORECASE,
    )

    if employees:
        profile["employees"] = employees.group(1)

    # -----------------------------
    # Timeline
    # -----------------------------

    timeline = re.search(
        r"(next month|this month|next week|immediately|asap|within \d+ months?)",
        text,
        re.IGNORECASE,
    )

    if timeline:
        profile["timeline"] = timeline.group(1)

    # -----------------------------
    # Goals
    # -----------------------------

    goal_patterns = [
        ("customer support", "Automate Customer Support"),
        ("support", "Automate Customer Support"),
        ("ai assistant", "Deploy AI Assistant"),
        ("automation", "Business Automation"),
        ("generate more leads", "Lead Generation"),
        ("increase sales", "Increase Sales"),
        ("book appointments", "Appointment Booking"),
        ("reduce costs", "Reduce Costs"),
        ("grow business", "Business Growth"),
        ("follow up", "Lead Follow-up"),
    ]
    for keyword, label in goal_patterns:
        if keyword.lower() in text.lower():
            profile["goal"] = label
            break

    # -----------------------------
    # Decision Maker
    # -----------------------------

    decision_patterns = [
        "ceo",
        "chief executive",
        "founder",
        "co-founder",
        "owner",
        "director",
        "president",
        "partner",
        "manager",
    ]

    for role in decision_patterns:
        if role.lower() in text.lower():
            profile["decision_maker"] = role.title()
            break

    return profile


def lead_score(profile):

    filled = sum(
        value is not None
        for value in profile.values()
    )

    return round((filled / len(profile)) * 100)