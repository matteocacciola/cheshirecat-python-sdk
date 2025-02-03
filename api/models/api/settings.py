from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class SettingDeleteOutput:
    deleted: bool

@dataclass
class SettingOutput:
    name: str
    value: Dict[str, Any]
    category: str
    setting_id: str
    updated_at: int | str

@dataclass
class SettingOutputItem:
    setting: SettingOutput

@dataclass
class SettingsOutputCollection:
    settings: List[SettingOutput]
