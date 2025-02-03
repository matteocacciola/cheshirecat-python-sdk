from typing import Dict, List, Any
from pydantic import BaseModel

from api.models.dtos import MessageBase, Why


class CollectionsItem(BaseModel):
    name: str
    vectors_count: int


class ConversationHistoryItemContent(MessageBase):
    why: Why | None = None


class ConversationHistoryItem(BaseModel):
    who: str
    when: float
    content: ConversationHistoryItemContent


class MemoryPointsDeleteByMetadataInfo(BaseModel):
    operation_id: int
    status: str


class MemoryRecallQuery(BaseModel):
    text: str
    vector: List[float]


class MemoryRecallVectors(BaseModel):
    embedder: str
    collections: Dict[str, List[Dict[str, Any]]]


class Record(BaseModel):
    id: str
    payload: Dict[str, Any] | None = None
    vector: List[float] | None = None
    shard_key: str | None = None
    order_value: float | None = None
