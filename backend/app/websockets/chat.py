from fastapi import WebSocket, WebSocketDisconnect
import json
import logging

logger = logging.getLogger(__name__)


class ChatWebSocketHandler:
    """Handler for WebSocket chat connections."""

    async def handle_connection(self, websocket: WebSocket):
        """Handle a WebSocket connection for the chat interface."""
        await websocket.accept()
        logger.info("WebSocket connection established")

        try:
            while True:
                data = await websocket.receive_text()
                logger.info(f"Received message: {data}")

                try:
                    message_data = json.loads(data)

                    if "message" not in message_data:
                        await websocket.send_json({
                            "type": "error",
                            "content": "Message field is required"
                        })
                        continue

                    await websocket.send_json({
                        "type": "message",
                        "content": f"Socket working! You sent: {message_data['message']}"
                    })
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "content": "Invalid JSON format"
                    })
        except WebSocketDisconnect:
            logger.info("WebSocket disconnected")
        except Exception as e:
            logger.error(f"WebSocket error: {str(e)}")
            try:
                await websocket.send_json({
                    "type": "error",
                    "content": "An internal error occurred"
                })
            except:
                pass