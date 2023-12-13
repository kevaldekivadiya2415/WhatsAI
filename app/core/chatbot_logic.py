from loguru import logger
import json
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from dotenv import load_dotenv
from app.utils.whatsapp_helpers import WhatsAppHandler


# Load environment variables
load_dotenv()

WHATSAPP_HANDLER = WhatsAppHandler()


class ChatbotLogic:
    def __init__(self) -> None:
        pass

    async def handle_whatsapp_webhook_post(self, message_body: dict):
        try:
            # Check if it's a WhatsApp status update
            if (
                message_body.get("entry", [{}])[0]
                .get("changes", [{}])[0]
                .get("value", {})
                .get("statuses")
            ):
                return JSONResponse(
                    content=json.dumps({"status": "ok"}), status_code=200
                )

            if WHATSAPP_HANDLER.is_valid_whatsapp_message(message_body=message_body):
                # Extract necessary information from the message body
                changes = message_body["entry"][0]["changes"][0]["value"]
                recipient_info = changes["contacts"][0]
                recipient_number = recipient_info["wa_id"]
                recipient_name = recipient_info["profile"]["name"]
                messages = changes["messages"]

                await WHATSAPP_HANDLER.process_whatsapp_message(
                    messages=messages, recipient_number=recipient_number
                )
            else:
                # If the request is not a WhatsApp API event, return an error
                raise HTTPException(status_code=404, detail="Not a WhatsApp API event")
        except json.JSONDecodeError as exc:
            logger.exception(exc)
            raise HTTPException(status_code=400, detail="Invalid JSON provided")
        except Exception as exc:
            logger.exception(exc)
