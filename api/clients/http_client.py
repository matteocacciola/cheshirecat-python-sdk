from abc import ABC, abstractmethod

import aiohttp
import requests
from urllib.parse import urlunparse
from typing import Callable, Dict, Any
from requests.adapters import BaseAdapter


class MiddlewareAdapter(BaseAdapter):
    def __init__(self, middleware: Callable):
        super().__init__()
        self.middleware = middleware

    def send(self, request, **kwargs):
        request = self.middleware(request, **kwargs)
        return super().send(request, **kwargs)


class HttpClientMixin(ABC):
    def __init__(
        self,
        host: str,
        port: int | None = None,
        apikey: str | None = None,
        is_https: bool = False
    ):
        self.apikey = apikey
        self.token = None
        self.user_id = None
        self.agent_id = None

        self.middlewares: Dict[str, Callable] = {
            "before_secure_request": self.before_secure_request(),
            "before_jwt_request": self.before_jwt_request(),
        }

        scheme = "https" if is_https else "http"
        netloc = f"{host}:{port}" if port else host
        self.http_uri = urlunparse((scheme, netloc, "", "", "", ""))

        self.http_client = self.create_http_client()

    def set_token(self, token: str):
        self.token = token
        return self

    def get_http_uri(self) -> str:
        return self.http_uri

    def before_secure_request(self) -> Callable:
        def middleware(request: requests.PreparedRequest, **kwargs):
            if self.apikey:
                request.headers["Authorization"] = f"Bearer {self.apikey}"
            if self.user_id:
                request.headers["user_id"] = self.user_id
            if self.agent_id:
                request.headers["agent_id"] = self.agent_id
            return request

        return middleware

    def before_jwt_request(self) -> Callable:
        def middleware(request: requests.PreparedRequest, **kwargs):
            if self.token:
                request.headers["Authorization"] = f"Bearer {self.token}"
            if self.agent_id:
                request.headers["agent_id"] = self.agent_id
            return request

        return middleware

    @abstractmethod
    def create_http_client(self) -> Any:
        pass

    @abstractmethod
    def get_client(self, agent_id: str | None = None, user_id: str | None = None) -> Any:
        pass


class HttpClient(HttpClientMixin):
    def create_http_client(self) -> requests.Session:
        session = requests.Session()
        for middleware in self.middlewares.values():
            adapter = MiddlewareAdapter(middleware)
            session.mount(self.http_uri, adapter)
        return session

    def get_client(self, agent_id: str | None = None, user_id: str | None = None) -> requests.Session:
        if not self.apikey and not self.token:
            raise ValueError("You must provide an apikey or a token")

        self.agent_id = agent_id or "agent"
        self.user_id = user_id

        return self.http_client


class AsyncHttpClient(HttpClientMixin):
    def create_http_client(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(base_url=self.http_uri)

    def get_client(self, agent_id: str | None = None, user_id: str | None = None) -> aiohttp.ClientSession:
        if not self.apikey and not self.token:
            raise ValueError("You must provide an apikey or a token")

        self.agent_id = agent_id or "agent"
        self.user_id = user_id

        headers = {}
        for middleware in self.middlewares.values():
            headers.update(middleware())
        return aiohttp.ClientSession(base_url=self.http_uri, headers=headers)
