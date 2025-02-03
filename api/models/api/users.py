from dataclasses import dataclass
from typing import Dict, List


@dataclass
class UserOutput:
    username: str
    permissions: Dict[str, List[str]]
    id: str
