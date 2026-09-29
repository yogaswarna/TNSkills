import os

from .gemini_client import generate_text


WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.8-flash"
)


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str
):

    prompt = f"""
You are FitBuddy.

You are updating an existing 7-day fitness plan.

Fitness goal:

{goal}


Preferred intensity:

{intensity}


Original workout plan:

--------------------
{original_plan}
--------------------


User feedback:

--------------------
{feedback}
--------------------


Create a revised 7-day workout plan.

The revised plan must:

- Address the user's feedback.
- Maintain the original fitness goal.
- Maintain the requested intensity.
- Include Day 1 through Day 7.
- Include warm-up.
- Include main workout.
- Include rest/recovery.
- Include cool-down.
- Avoid unsafe exercise.
- Avoid extreme dieting.
- Avoid medical diagnosis.
- Encourage stopping if pain, dizziness,
  faintness, or other concerning symptoms occur.

Return only the revised workout plan.

This is general wellness information,
not medical advice.
"""


    return generate_text(
        prompt,
        WORKOUT_MODEL
    )