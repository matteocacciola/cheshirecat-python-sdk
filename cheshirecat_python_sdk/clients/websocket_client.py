from urllib.parse import urlencode
from websockets import connect, ClientConnection
from websockets.exceptions import InvalidURI


class WSClient:
    def __init__(
        self,
        host: str,
        port: int | None = None,
        apikey: str | None = None,
        is_wss: bool | None = False,
    ):
        self.host = host
        self.port = port
        self.apikey = apikey
        self.token = None
        self.is_wss = is_wss

    def set_token(self, token: str) -> "WSClient":
        self.token = token
        return self

    def get_ws_uri(self, agent_id: str | None = None, user_id: str | None = None) -> str:
        query = {}
        if self.token:
            query["token"] = self.token
        elif self.apikey:
            query["apikey"] = self.apikey
        else:
            raise ValueError("You must provide an apikey or a token")

        if user_id:
            query["user_id"] = user_id

        scheme = "wss" if self.is_wss else "ws"
        path = f"ws/{agent_id}" if agent_id else "ws"
        query_string = urlencode(query)
        port_suffix = f":{self.port}" if self.port else ""

        return f"{scheme}://{self.host}{port_suffix}/{path}?{query_string}"

    async def get_client(self, agent_id: str | None = None, user_id: str | None = None) -> ClientConnection:
        uri = self.get_ws_uri(agent_id, user_id)
        try:
            # Create a WebSocket connection
            websocket = await connect(uri, ping_interval=100000, ping_timeout=100000)
            return websocket
        except InvalidURI as e:
            raise ValueError(f"Invalid WebSocket URI: {uri}") from e
