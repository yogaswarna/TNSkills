import os

from .gemini_client import generate_text


WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.8-flash"
)


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
):

    prompt = f"""
You are FitBuddy, a careful fitness-planning assistant.

Create a practical 7-day fitness plan.

User information:

Name: {username}

Age: {age}

Weight: {weight} kg

Fitness Goal: {goal}

Workout Intensity: {intensity}


Create exactly seven sections:

Day 1
Day 2
Day 3
Day 4
Day 5
Day 6
Day 7


For every day include:

1. Focus
2. Warm-up
3. Main workout
4. Sets and repetitions or duration
5. Rest/recovery
6. Cool-down


The plan should be practical and easy to understand.

Safety requirements:

- Do not diagnose medical conditions.
- Do not recommend starvation.
- Do not recommend extreme dieting.
- Do not recommend dehydration.
- Do not recommend unsafe exercise.
- Include adequate rest and recovery.
- Keep the requested intensity in mind.
- Do not make appearance-based judgments.
- Tell the user to stop if they experience pain,
  dizziness, faintness, or other concerning symptoms.

This is general wellness information,
not medical advice.

Return only the workout plan.
"""


    return generate_text(
        prompt,
        WORKOUT_MODEL
    )