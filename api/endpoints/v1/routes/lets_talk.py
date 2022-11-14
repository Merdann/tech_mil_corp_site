from core.database.repository import lets_talk
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Form
from fastapi import status
from pydantic import EmailStr

router = APIRouter()


@router.post(
    "/send-email",
    status_code=status.HTTP_202_ACCEPTED,
)
def send_email(
    background_tasks: BackgroundTasks,
    full_name: str = Form(min_length=3, max_length=50),
    phone: str = Form(min_length=12, max_length=12),
    email: EmailStr = Form(...),
    message: str = Form(min_length=10),
):
    return lets_talk.send_email(
        background_tasks=background_tasks,
        full_name=full_name,
        phone=phone,
        email=email,
        message=message,
    )
