from typing import Dict, List
from pydantic import BaseModel

from api.models.api.nested.memories import (
    CollectionsItem,
    ConversationHistoryItem,
    MemoryPointsDeleteByMetadataInfo,
    Record,
    MemoryRecallQuery,
    MemoryRecallVectors,
)
from api.models.dtos import MemoryPoint


class CollectionPointsDestroyOutput(BaseModel):
    deleted: Dict[str, bool]


class CollectionsOutput(BaseModel):
    collections: List[CollectionsItem]

class ConversationHistoryDeleteOutput(BaseModel):
    deleted: bool


class ConversationHistoryOutput(BaseModel):
    history: List[ConversationHistoryItem]


class MemoryPointDeleteOutput(BaseModel):
    deleted: str


class MemoryPointOutput(MemoryPoint):
    id: str
    vector: List[float]


class MemoryPointsDeleteByMetadataOutput(BaseModel):
    deleted: MemoryPointsDeleteByMetadataInfo


class MemoryPointsOutput(BaseModel):
    points: List[Record]
    next_offset: str | int | None = None


class MemoryRecallOutput(BaseModel):
    query: MemoryRecallQuery
    vectors: MemoryRecallVectors
