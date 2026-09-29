from typing import Literal

from pydantic import BaseModel
from pydantic import Field


Goal = Literal[
    "weight loss",
    "muscle gain",
    "general wellness",
    "flexibility"
]


Intensity = Literal[
    "low",
    "medium",
    "high"
]


class UserInput(BaseModel):

    username: str = Field(
        min_length=2,
        max_length=100
    )

    user_id: str = Field(
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=0,
        le=500
    )

    goal: Goal

    intensity: Intensity


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=100
    )

    feedback: str = Field(
        min_length=3,
        max_length=2000
    )