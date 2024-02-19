import logging
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic_settings import BaseSettings

from email_sender import send_email, translate_msg


load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    BASE_URL: str = "http://localhost:8000"
    USE_NGROK: str = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()
app = FastAPI()


if settings.USE_NGROK and os.environ.get("NGROK_AUTHTOKEN"):

    from pyngrok import ngrok

    port = (sys.argv[sys.argv.index("--port") + 1]
            if "--port" in sys.argv else "8000")
    public_url = ngrok.connect(port).public_url
    settings.BASE_URL = public_url
    logger.info(f"Public URL: {public_url}")


@app.post("/webhook")
async def webhook(request: Request) -> None:
    payload = await request.json()
    fullname = payload["current"]["name"]
    country = payload["current"]["org_name"]
    email = payload["current"]["email"][0]["value"]
    logger.info(f"fullname {fullname}, country {country}, email {email}")
    if country:
        body = translate_msg(fullname, country)
        send_email(body, email)
        logger.info("Webhook processed successfully "
                    f"for {fullname} with: email {email}, country: {country}")
