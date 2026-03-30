from dataclasses import dataclass
from typing import Literal, Union


Segment = Literal["local", "argument", "this", "that",
                  "constant", "static", "temp", "pointer"]

ArithmeticOp = Literal["add", "sub", "neg",
                       "eq", "gt", "lt",
                       "and", "or", "not"]


@dataclass
class PushCommand:
    segment: Segment
    i: int


@dataclass
class PopCommand:
    segment: Segment
    i: int


@dataclass
class ArithmeticCommand:
    op: ArithmeticOp


Command = Union[PushCommand, PopCommand, ArithmeticCommand]
