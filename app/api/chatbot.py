import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from loguru import logger
from app.core.chatbot_logic import ChatbotLogic

# Load environment variables
load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# Add router
router = APIRouter()

#
CHATBOT_LOGIC = ChatbotLogic()


@router.get(
    path="/webhook",
    tags=["WhatsApp Webhook"],
    summary="Handle WhatsApp Webhook (GET)",
    description="This endpoint handles WhatsApp webhook for GET requests.",
    responses={
        200: {"description": "Webhook response successfully received."},
        400: {"description": "Bad Request: Invalid parameters."},
        401: {"description": "Unauthorized: Authentication failed."},
        500: {"description": "Internal Server Error: Something went wrong."},
    },
)
async def whatsapp_webhook_get(request: Request):
    """
    WhatsApp Webhook (GET)

    Handles incoming GET requests from WhatsApp webhook.

    Args:
        request (Request): FastAPI Request object.

    Returns:
        JSONResponse: Webhook response.
    """
    try:
        verify_token = request.query_params.get("hub.verify_token")

        if verify_token == VERIFY_TOKEN:
            logger.info("Successfully verify the token.")
            return PlainTextResponse(request.query_params.get("hub.challenge"))
        else:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized: Invalid verify_token.",
            )
    except HTTPException as http_exc:
        logger.warning(f"HTTP Exception: {http_exc}")
        return JSONResponse(
            content={"status": "error", "message": "Webhook response failed."},
            status_code=http_exc.status_code,
        )
    except Exception as exc:
        logger.exception(f"Internal Server Error: {exc}")
        return JSONResponse(
            content={"status": "error", "message": "Internal Server Error."},
            status_code=500,
        )


@router.post(
    path="/webhook",
    tags=["WhatsApp Webhook"],
    summary="Handle WhatsApp Webhook (POST)",
    description="This endpoint handles WhatsApp webhook for POST requests.",
)
async def whatsapp_webhook_post(request: Request):
    try:
        request_data = await request.json()
        logger.info(f"Request Data:- {request_data}")
        await CHATBOT_LOGIC.handle_whatsapp_webhook_post(message_body=request_data)
    except Exception as exc:
        logger.exception(exc)
