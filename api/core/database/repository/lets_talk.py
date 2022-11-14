from core.config import settings
from core.exceptions import exceptions
from core.security import FieldsValidations
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig
from fastapi_mail import FastMail
from fastapi_mail import MessageSchema
from fastapi_mail import MessageType

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


def send_email(
    background_tasks: BackgroundTasks,
    full_name: str,
    phone: str,
    email: str,
    message: str,
):
    if not FieldsValidations.correct_email(email):
        raise exceptions.exception_incorrect_email()
    if not FieldsValidations.correct_phone(phone):
        raise exceptions.exception_incorrect_phone_number()
    html = f"""
    <p>
    <b>Name:</b> {full_name}</br>
    <b>Phone:</b> {phone}</br>
    <b>Email:</b> {email}</br>
    <b>Message:</b></br>
    {message}
    </p>
    """
    message = MessageSchema(
        subject=f"Message from {full_name}",
        recipients=[i for i in settings.MAIL_TO.split(",")],
        body=html,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return {"detail": "Your email has been sent"}
