from dataclasses import dataclass, field
from typing import List                              # <1>

@dataclass
class ClubMember:

    name: str
    guests: List[str] = field(default_factory=list)  # <2>
