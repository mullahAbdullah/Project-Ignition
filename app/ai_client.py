import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = os.getenv("OPENROUTER_MODEL")


def generate_response(
    system_prompt,
    conversation,
    temperature=0.7,
    closing_stage=False,
):

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    if closing_stage:
        messages.append(
            {
                "role": "system",
                "content": (
                    "The lead is now fully qualified. "
                    "Do NOT ask any more qualification questions. "
                    "Transition into a professional closing conversation. "
                    "Explain that your company now has a clear understanding of the customer's requirements. "
                    "Request their contact information if it has not already been provided. "
                    "Once contact information has been collected, thank them professionally and explain that one of your specialists will review their requirements and prepare a tailored solution. "
                    "Tell them that your team will contact them using their preferred contact method with the next steps. "
                    "Never say 'I will contact you', 'I'll prepare your solution', or similar first-person phrasing. "
                    "Always speak as a representative of the business using 'we', 'our team', or 'our specialists'. "
                    "request their contact information if it has not already been provided, "
                    "answer any additional business questions they ask, "
                    "and end the conversation naturally once they are finished."
                ),
            }
        )

    messages.extend(conversation)

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=500,
            temperature=temperature,
            stream=True,
        )

        for chunk in response:

            if (
                chunk.choices
                and chunk.choices[0].delta
                and chunk.choices[0].delta.content
            ):
                yield chunk.choices[0].delta.content

    except Exception as e:

        yield (
            "⚠️ Unable to contact the AI service.\n\n"
            f"Error: {str(e)}"
        )
        
EMPTY_PROFILE = {
    "company": None,
    "industry": None,
    "budget": None,
    "timeline": None,
    "employees": None,
    "decision_maker": None,
    "goal": None,

    # Contact Information
    "email": None,
    "phone": None,
    "whatsapp": None,
    "preferred_contact": None,
}

def extract_lead_info_ai(conversation):
    user_messages = [
        msg for msg in conversation
        if msg["role"] == "user"
    ]

    if not user_messages:
        return EMPTY_PROFILE.copy()
        
    messages = [
        {
            "role": "system",
            "content": """
You are an information extraction engine.

Extract lead information.

Return ONLY valid JSON.

Schema:

{
  "company": null,
  "industry": null,
  "budget": null,
  "timeline": null,
  "employees": null,
  "decision_maker": null,
  "goal": null,
  "email": null,
  "phone": null,
  "whatsapp": null,
  "preferred_contact": null
}

Rules:
- Never invent information.
- Extract contact information only if the customer explicitly provides it.
- If the same phone number is also used for WhatsApp, use that value for both fields.
- "preferred_contact" should contain values such as "Email", "Phone", or "WhatsApp" only if the customer explicitly states a preference.
- Use null when unknown.
- Return JSON only.
"""
        }
    ]

    messages.extend(conversation)
    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0,
            max_tokens=250,
        )

        content = response.choices[0].message.content.strip()

        data = json.loads(content)

    except Exception:

        return EMPTY_PROFILE.copy()

    if not isinstance(data, dict):
        return EMPTY_PROFILE.copy()

    profile = EMPTY_PROFILE.copy()

    for key in profile:
        profile[key] = data.get(key)

    return profile