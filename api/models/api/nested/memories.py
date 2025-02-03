from dataclasses import dataclass
from typing import Dict, List, Any
from api.models.dtos import MessageBase, Why


@dataclass
class CollectionsItem:
    name: str
    vectors_count: int

@dataclass
class ConversationHistoryItemContent(MessageBase):
    why: Why | None = None

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        if self.why is not None:
            data["why"] = self.why.to_dict()
        return data

@dataclass
class ConversationHistoryItem:
    who: str
    when: float
    content: ConversationHistoryItemContent

    def to_dict(self) -> Dict[str, Any]:
        return {
            "who": self.who,
            "content": self.content.to_dict(),
            "when": self.when,
        }

@dataclass
class MemoryPointsDeleteByMetadataInfo:
    operation_id: int
    status: str

@dataclass
class MemoryRecallQuery:
    text: str
    vector: List[float]

@dataclass
class MemoryRecallVectors:
    embedder: str
    collections: Dict[str, List[Dict[str, Any]]]

@dataclass
class Record:
    id: str
    payload: Dict[str, Any] | None = None
    vector: List[float] | None = None
    shard_key: str | None = None
    order_value: float | None = None
