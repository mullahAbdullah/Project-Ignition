QUESTION_MAP = {
    "budget": {
        "priority": 100,
        "question": "May I ask what budget you've allocated for implementing this solution?",
        "reason": "Budget helps determine the most suitable solution and proposal.",
    },
    "timeline": {
        "priority": 90,
        "question": "When are you planning to implement this project?",
        "reason": "Understanding the timeline helps prioritize urgency and planning.",
    },
    "decision_maker": {
        "priority": 95,
        "question": "Will you be the final decision maker for this project?",
        "reason": "Knowing who makes the final decision helps determine the sales process.",
    },
    "employees": {
        "priority": 70,
        "question": "Approximately how many employees will be using this solution?",
        "reason": "Company size influences deployment and pricing recommendations.",
    },
    "goal": {
        "priority": 85,
        "question": "What is the primary business goal you'd like this AI assistant to achieve?",
        "reason": "Understanding the business objective allows us to recommend the right solution.",
    },
    "industry": {
        "priority": 60,
        "question": "Which industry does your business operate in?",
        "reason": "Industry-specific knowledge improves recommendations.",
    },
    "company": {
        "priority": 50,
        "question": "Could you tell me the name of your company?",
        "reason": "Company information is required for CRM records and proposals.",
    },
}


def get_next_step(analysis):

    missing = analysis["missing"]

    if not missing:
        return {
            "next_question": None,
            "reason": "All essential lead information has been collected.",
            "next_action": "Prepare proposal or schedule a discovery call.",
        }

    highest_priority = max(
        missing,
        key=lambda field: QUESTION_MAP[field]["priority"]
    )

    data = QUESTION_MAP[highest_priority]

    return {
        "next_question": data["question"],
        "reason": data["reason"],
        "next_action": "Continue qualifying the lead.",
    }