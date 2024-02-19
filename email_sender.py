import logging
import os
import smtplib
import uuid
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv

from utils import get_primary_language


load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def translate_msg(fullname: str, country: str) -> str:
    msg = f"""
    Dear {fullname},
    Thank you for registering with us!
    Welcome to our community. We are excited to have you on board.
    Please feel free to reach out if you have any questions or need assistance.
    """

    dest_lang = get_primary_language(country)
    if not dest_lang:
        return msg

    api_key = os.environ.get("AZURE_API_KEY")
    endpoint = "https://api.cognitive.microsofttranslator.com"
    route = f"/translate?api-version=3.0&from=en&to={dest_lang}"

    url = f"{endpoint}{route}"
    body = [{"text": msg}]
    headers = {"Content-Type": "application/json",
               "Ocp-Apim-Subscription-Key": api_key,
               "X-ClientTraceId": str(uuid.uuid4()),
               "Ocp-Apim-Subscription-Region": "eastus"}

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        return data[0]['translations'][0]['text']
    else:
        logger.error(f"Error. Status code: {response.status_code}")


def send_email(msg: str, recipient_email: str) -> None:
    sender_email = os.environ.get("SMTP_USERNAME")
    message = MIMEText(msg, "plain")

    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Successful registration"

    smtp_server = "smtp.gmail.com"
    port = 587
    username = os.environ.get("SMTP_USERNAME")
    password = os.environ.get("SMTP_PASSWORD")

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(username, password)
        try:
            server.sendmail(sender_email, recipient_email, message.as_string())
            logger.info("Email sent successfully.")
        except smtplib.SMTPConnectError as e:
            logger.error(f"SMTP connection error: {e}")
