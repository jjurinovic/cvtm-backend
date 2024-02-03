import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import ssl
from fastapi import HTTPException

ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
SENDER_EMAIL = os.environ["MAIL_USERNAME"]
SENDER_EMAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
PORT = os.environ["MAIL_PORT"]
MAIL_SERVER = os.environ["MAIL_SERVER"]
MAIL_FROM = os.environ["MAIL_FROM"]
MAIL_FROM_NAME = os.environ["MAIL_FROM_NAME"]
dirname = os.path.dirname(__file__)
templates_folder = os.path.join(dirname, './templates')


conf = ConnectionConfig(
    MAIL_USERNAME=SENDER_EMAIL,
    MAIL_PASSWORD=SENDER_EMAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=templates_folder,
)


async def send_registration_email(password, recipient_email):
    template_body = {
        "email": recipient_email,
        "password": password
    }

    try:
        message = MessageSchema(
            subject="CVTM Registration - Your Credentials",
            recipients=[recipient_email],
            template_body=template_body,
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="registration.html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
