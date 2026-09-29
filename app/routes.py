from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from .crud import delete_user
from .crud import get_all_users
from .crud import get_user
from .crud import save_user
from .crud import update_plan

from .database import get_db

from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .gemini_generator import (
    generate_workout_gemini
)

from .schemas import UserInput

from .updated_plan import (
    update_workout_plan
)


router = APIRouter()


TEMPLATE_DIR = (
    Path(__file__).resolve().parent.parent
    /
    "templates"
)


templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)


def render_error(
    request: Request,
    message: str,
    status_code: int = 400
):

    return templates.TemplateResponse(

        request=request,

        name="error.html",

        context={
            "message": message
        },

        status_code=status_code
    )


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request
):

    return templates.TemplateResponse(

        request=request,

        name="index.html"
    )


@router.get("/health")
def health():

    return {
        "status": "ok"
    }


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(

    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        data = UserInput(

            username=username.strip(),

            user_id=user_id.strip(),

            age=age,

            weight=weight,

            goal=goal,

            intensity=intensity
        )


        existing_user = get_user(
            db,
            data.user_id
        )


        if existing_user:

            return render_error(

                request,

                (
                    f"User ID '{data.user_id}' "
                    "already exists. "
                    "Use another ID or open "
                    "the existing plan."
                ),

                409
            )


        workout_plan = generate_workout_gemini(

            data.username,

            data.age,

            data.weight,

            data.goal,

            data.intensity
        )


        nutrition_tip = (
            generate_nutrition_tip_with_flash(
                data.goal
            )
        )


        user = save_user(

            db=db,

            user_id=data.user_id,

            username=data.username,

            age=data.age,

            weight=data.weight,

            goal=data.goal,

            intensity=data.intensity,

            original_plan=workout_plan,

            nutrition_tip=nutrition_tip
        )


        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": user,

                "workout_plan": workout_plan,

                "nutrition_tip": nutrition_tip,

                "message":
                    "Your 7-day plan has been generated."
            }
        )


    except ValueError as exc:

        return render_error(
            request,
            str(exc),
            400
        )


    except RuntimeError as exc:

        return render_error(
            request,
            str(exc),
            503
        )


    except IntegrityError:

        db.rollback()

        return render_error(

            request,

            "That User ID is already in use.",

            409
        )


    except Exception:

        return render_error(

            request,

            (
                "Something went wrong while "
                "generating the plan. "
                "Check the terminal and try again."
            ),

            500
        )


@router.get(
    "/user/{user_id}",
    response_class=HTMLResponse
)
def user_plan(

    request: Request,

    user_id: str,

    db: Session = Depends(get_db)
):

    user = get_user(
        db,
        user_id
    )


    if not user:

        return render_error(
            request,
            "User not found.",
            404
        )


    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "user": user,

            "workout_plan":
                user.updated_plan
                or
                user.original_plan,

            "nutrition_tip":
                user.nutrition_tip,

            "message":
                "Saved plan loaded."
        }
    )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    feedback = feedback.strip()


    if len(feedback) < 3:

        return render_error(

            request,

            "Please enter at least 3 characters of feedback.",

            400
        )


    user = get_user(
        db,
        user_id.strip()
    )


    if not user:

        return render_error(

            request,

            "User ID not found.",

            404
        )


    try:

        revised_plan = update_workout_plan(

            original_plan=
                user.updated_plan
                or
                user.original_plan,

            feedback=feedback,

            goal=user.goal,

            intensity=user.intensity
        )


        update_plan(

            db,

            user,

            revised_plan,

            feedback
        )


        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": user,

                "workout_plan":
                    revised_plan,

                "nutrition_tip":
                    user.nutrition_tip,

                "message":
                    "Plan updated using your feedback."
            }
        )


    except RuntimeError as exc:

        return render_error(

            request,

            str(exc),

            503
        )


    except Exception:

        return render_error(

            request,

            (
                "The plan could not be updated. "
                "Please try again."
            ),

            500
        )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db)
):

    users = get_all_users(db)


    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={
            "users": users
        }
    )


@router.post(
    "/admin/users/{user_id}/delete"
)
def remove_user(

    user_id: str,

    db: Session = Depends(get_db)
):

    user = get_user(
        db,
        user_id
    )


    if user:

        delete_user(
            db,
            user
        )


    return RedirectResponse(

        url="/view-all-users",

        status_code=303
    )