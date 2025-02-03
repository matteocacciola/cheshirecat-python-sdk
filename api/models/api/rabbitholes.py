from dataclasses import dataclass
from typing import List, Dict


@dataclass
class AllowedMimeTypesOutput:
    allowed: List[str]

    def to_dict(self) -> Dict[str, List[str]]:
        return {
            "allowed": self.allowed,
        }
