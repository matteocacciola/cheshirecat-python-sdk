from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class AgentOutput:
    output: str | None = None
    intermediate_steps: List[Dict[str, Any]] | None = field(default_factory=list)
    return_direct: bool = False
    with_llm_error: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "output": self.output,
            "intermediate_steps": self.intermediate_steps,
            "return_direct": self.return_direct,
            "with_llm_error": self.with_llm_error,
        }

@dataclass
class Memory:
    episodic: Dict[str, Any] | None = field(default_factory=dict)
    declarative: Dict[str, Any] | None = field(default_factory=dict)
    procedural: Dict[str, Any] | None = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Dict[str, Any] | None]:
        return {
            "episodic": self.episodic,
            "declarative": self.declarative,
            "procedural": self.procedural,
        }

@dataclass
class MemoryPoint:
    content: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "metadata": self.metadata,
        }

@dataclass
class MessageBase:
    text: str
    images: List[str] | None = field(default_factory=list)
    audio: List[str] | None = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "text": self.text,
        }
        if self.images is not None:
            result["images"] = self.images
        if self.audio is not None:
            result["audio"] = self.audio
        return result

@dataclass
class Message(MessageBase):
    additional_fields: Dict[str, Any] | None = None

    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        if self.additional_fields is not None:
            result.update(self.additional_fields)
        return result

@dataclass
class SettingInput:
    name: str
    value: Dict[str, Any]
    category: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "category": self.category,
        }

@dataclass
class Why:
    input: str | None = None
    intermediate_steps: Dict[str, Any] | None = field(default_factory=dict)
    memory: Memory = field(default_factory=Memory)
    model_interactions: Dict[str, Any] | None = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input": self.input,
            "intermediate_steps": self.intermediate_steps,
            "memory": self.memory.to_dict(),
            "model_interactions": self.model_interactions,
        }
