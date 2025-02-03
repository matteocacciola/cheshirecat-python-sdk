from dataclasses import dataclass


@dataclass
class TokenOutput:
    access_token: str
    token_type: str | None = "bearer"
