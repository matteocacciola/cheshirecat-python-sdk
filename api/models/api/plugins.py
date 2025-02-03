from dataclasses import dataclass, field
from typing import List, Dict, Any

from api.models.api.nested.plugins import PluginSettingsOutput


@dataclass
class FilterOutput:
    query: str | None = None

    def to_dict(self) -> Dict[str, str | None]:
        return {
            "query": self.query,
        }

@dataclass
class HookOutput:
    name: str
    priority: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "priority": self.priority,
        }

@dataclass
class ToolOutput:
    name: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
        }

@dataclass
class PluginItemOutput:
    id: str
    name: str
    description: str
    author_name: str
    author_url: str
    plugin_url: str
    tags: str
    thumb: str
    version: str
    active: bool
    hooks: List[HookOutput]
    tools: List[ToolOutput]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "author_name": self.author_name,
            "author_url": self.author_url,
            "plugin_url": self.plugin_url,
            "tags": self.tags,
            "thumb": self.thumb,
            "version": self.version,
            "active": self.active,
            "hooks": [hook.to_dict() for hook in self.hooks],
            "tools": [tool.to_dict() for tool in self.tools],
        }

@dataclass
class PluginCollectionOutput:
    filters: FilterOutput
    installed: List[PluginItemOutput] = field(default_factory=list)
    registry: List["PluginItemRegistryOutput"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filters": self.filters.to_dict(),
            "installed": [item.to_dict() for item in self.installed],
            "registry": [item.to_dict() for item in self.registry],
        }

@dataclass
class PluginItemRegistryOutput:
    id: str
    name: str
    description: str
    author_name: str
    author_url: str
    plugin_url: str
    tags: str
    thumb: str
    version: str
    url: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "author_name": self.author_name,
            "author_url": self.author_url,
            "plugin_url": self.plugin_url,
            "tags": self.tags,
            "thumb": self.thumb,
            "version": self.version,
            "url": self.url,
        }

@dataclass
class PluginsSettingsOutput:
    settings: List[PluginSettingsOutput]

@dataclass
class PluginToggleOutput:
    info: str
