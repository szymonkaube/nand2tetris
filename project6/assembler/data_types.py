from dataclasses import dataclass
from typing import Optional


@dataclass
class AFields:
    value: str


@dataclass
class CFields:
    dest: Optional[str]
    comp: str
    jump: Optional[str]


@dataclass
class ParsedInstruction:
    kind: str  # A or C
    fields: AFields | CFields
