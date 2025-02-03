from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class FactoryObjectSettingOutput:
    name: str
    value: Dict[str, Any]
    scheme: Dict[str, Any] | None = None

@dataclass
class FactoryObjectSettingsOutput:
    settings: List[FactoryObjectSettingOutput]
    selected_configuration: str