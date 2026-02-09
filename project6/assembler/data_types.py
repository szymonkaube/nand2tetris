from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class CFields:
    dest: Optional[str]
    comp: str
    jump: Optional[str]


@dataclass
class ParsedLine:
    kind: Literal["A", "C", "L"]
    symbol: Optional[str] = None
    fields: Optional[CFields] = None
