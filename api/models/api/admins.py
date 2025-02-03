from dataclasses import dataclass
from typing import Dict, List, Any
from plugins import PluginToggleOutput


@dataclass
class AdminOutput:
    username: str
    permissions: Dict[str, List[str]]
    id: str

@dataclass
class CreatedOutput:
    created: bool

@dataclass
class PluginDeleteOutput:
    deleted: str

@dataclass
class PluginDetailsOutput:
    data: Dict[str, Any]

@dataclass
class PluginInstallFromRegistryOutput(PluginToggleOutput):
    url: str
    info: str

@dataclass
class PluginInstallOutput(PluginToggleOutput):
    filename: str
    content_type: str

@dataclass
class ResetOutput:
    deleted_settings: bool
    deleted_memories: bool
    deleted_plugin_folders: bool
