from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User


def get_user(
    db: Session,
    user_id: str
):

    return db.scalar(
        select(User).where(
            User.user_id == user_id
        )
    )


def get_all_users(
    db: Session
):

    return list(
        db.scalars(
            select(User).order_by(
                User.created_at.desc()
            )
        ).all()
    )


def save_user(
    db: Session,
    user_id: str,
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    original_plan: str,
    nutrition_tip: str
):

    user = User(

        user_id=user_id,

        username=username,

        age=age,

        weight=weight,

        goal=goal,

        intensity=intensity,

        original_plan=original_plan,

        nutrition_tip=nutrition_tip
    )


    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def update_plan(
    db: Session,
    user: User,
    updated_plan: str,
    feedback: str
):

    user.updated_plan = updated_plan

    user.feedback = feedback

    user.updated_at = datetime.now(
        timezone.utc
    )


    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User
):

    db.delete(user)

    db.commit()