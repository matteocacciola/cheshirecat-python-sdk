from dataclasses import dataclass, field
from typing import Dict, Any

from api.models.dtos import MessageBase, Why


@dataclass
class MessageOutput(MessageBase):
    why: Why = field(default_factory=Why)  # Assuming Why has a no-args constructor
    type: str | None = "chat"  # Default argument
    error: bool | None = False  # Default argument
    content: str = field(init=False)  # Field without a default value

    def __post_init__(self):
        self.content = self.text

    def get_content(self) -> str:
        return self.text

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "type": self.type,
            "why": self.why.to_dict(),
            "content": self.text,
            "error": self.error,
        })
        return data
