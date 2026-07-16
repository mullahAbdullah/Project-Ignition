from app.prompts import SYSTEM_PROMPTS


def get_system_prompt(mode):

    return SYSTEM_PROMPTS.get(
        mode,
        SYSTEM_PROMPTS["Lead Qualification"],
    )