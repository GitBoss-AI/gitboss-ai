from fastapi import WebSocket
import json
import logging
from typing import List

logger = logging.getLogger(__name__)


class ChatWebSocketHandler:
    """Handler for chat WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Connect a new WebSocket client."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client."""
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Remaining connections: {len(self.active_connections)}")

    async def handle_connection(self, websocket: WebSocket):
        """Handle a WebSocket connection."""
        await self.connect(websocket)

        try:
            # Send welcome message
            await websocket.send_json({
                "type": "system",
                "message": "Connected to GitBoss AI chat."
            })

            # Handle messages
            while True:
                data = await websocket.receive_text()

                try:
                    message = json.loads(data)

                    # Process message - for now, just echo it back
                    # In the future, this would integrate with the AI assistant
                    response = {
                        "type": "response",
                        "message": f"Echo: {message.get('message', '')}"
                    }

                    await websocket.send_json(response)

                except json.JSONDecodeError:
                    logger.error(f"Received invalid JSON: {data}")
                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid message format. Expected JSON."
                    })

        except Exception as e:
            logger.error(f"WebSocket error: {str(e)}")
        finally:
            self.disconnect(websocket)