from typing import Callable
import json

from api.endpoints.base import AbstractEndpoint
from api.models.api.messages import MessageOutput
from api.models.dtos import Message
from api.utils import deserialize


class MessageEndpoint(AbstractEndpoint):
    def send_http_message(
        self, message: Message, agent_id: str | None = None, user_id: str | None = None
    ) -> MessageOutput:
        """
        This endpoint sends a message to the agent identified by the agentId parameter. The message is sent via HTTP.
        :param message: Message object, the message to send
        :param agent_id: the agent id, if None the message is sent to the default agent
        :param user_id: the user id, if None the message is considered as sent by the default user
        """
        return self.post_json('/message', MessageOutput, message.model_dump(), agent_id, user_id)

    async def send_websocket_message(
        self,
        message: Message,
        agent_id: str | None = None,
        user_id: str | None = None,
        callback: Callable[[str], None] | None = None
    ) -> MessageOutput:
        """
        This endpoint sends a message to the agent identified by the agentId parameter. The message is sent via WebSocket.
        :param message: Message object, the message to send
        :param agent_id: the agent id, if None the message is sent to the default agent
        :param user_id: the user id, if None the message is considered as sent by the default user
        :param callback: callable, a callback function that will be called for each message received
        """
        try:
            json_data = json.dumps(message.model_dump())
        except Exception:
            raise RuntimeError("Error encoding message")

        client = await self.get_ws_client(agent_id, user_id)

        try:
            await client.send(json_data)

            while True:
                response = await client.recv()
                if not response:
                    raise RuntimeError("Error receiving message")

                if '"type":"chat"' not in response:
                    if callback:
                        callback(response)
                    continue
                break
        except Exception as e:
            await client.close()
            raise Exception(f"WebSocket error: {str(e)}")

        await client.close()
        return deserialize(json.loads(response), MessageOutput)
