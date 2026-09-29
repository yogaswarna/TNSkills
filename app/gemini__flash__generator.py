import os

from .gemini_client import generate_text


TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-3.5-flash-lite"
)


def generate_nutrition_tip_with_flash(
    goal: str
):

    prompt = f"""
You are FitBuddy.

Provide one concise nutrition or recovery tip
for someone whose fitness goal is:

{goal}


Requirements:

- Maximum 2 to 4 sentences.
- Give practical advice.
- Encourage balanced meals.
- Encourage hydration.
- Encourage adequate recovery.
- Avoid extreme dieting.
- Avoid calorie prescriptions.
- Avoid supplements.
- Avoid medical claims.
- Do not judge body size or appearance.

The response should be general wellness information,
not medical advice.

Return only the tip.
"""


    return generate_text(
        prompt,
        TIP_MODEL
    )