from dataclasses import dataclass
from typing import Dict, List, Any

from api.models.api.nested.memories import (
    CollectionsItem,
    ConversationHistoryItem,
    MemoryPointsDeleteByMetadataInfo,
    Record,
    MemoryRecallQuery,
    MemoryRecallVectors,
)
from api.models.dtos import MemoryPoint


@dataclass
class CollectionPointsDestroyOutput:
    deleted: Dict[str, bool]

@dataclass
class CollectionsOutput:
    collections: List[CollectionsItem]

@dataclass
class ConversationHistoryDeleteOutput:
    deleted: bool

@dataclass
class ConversationHistoryOutput:
    history: List[ConversationHistoryItem]

    def to_dict(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "history": [item.to_dict() for item in self.history]
        }

@dataclass
class MemoryPointDeleteOutput:
    deleted: str

@dataclass
class MemoryPointOutput(MemoryPoint):
    id: str
    vector: List[float]

@dataclass
class MemoryPointsDeleteByMetadataOutput:
    deleted: MemoryPointsDeleteByMetadataInfo

@dataclass
class MemoryPointsOutput:
    points: List[Record]
    next_offset: str | int | None = None

@dataclass
class MemoryRecallOutput:
    query: MemoryRecallQuery
    vectors: MemoryRecallVectors
