from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PropertySettingsOutput:
    default: Any
    title: str
    type: str
    extra: Dict[str, Any] | None = None

@dataclass
class PluginSchemaSettings:
    title: str
    type: str
    properties: Dict[str, PropertySettingsOutput]

@dataclass
class PluginSettingsOutput:
    name: str
    value: Dict[str, Any]
    scheme: PluginSchemaSettings | None = None
