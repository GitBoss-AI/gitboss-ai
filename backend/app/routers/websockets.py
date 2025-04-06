from fastapi import APIRouter, WebSocket
import logging

from app.websocket.chat import ChatWebSocketHandler

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])

chat_handler = ChatWebSocketHandler()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for chat"""
    await chat_handler.handle_connection(websocket)