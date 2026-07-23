from dataclasses import dataclass
from typing import Any
from enum import Enum, auto


class TokenType(Enum):
    Identifier = auto()
    ConstIdentifier = auto()
    Assign = auto()
    NumberLit = auto()
    LParen = auto()
    RParen = auto()
    LBracket = auto()
    RBracket = auto()
    BinaryOp = auto()
    PostfixOp = auto()
    Comma = auto()
    Colon = auto()


@dataclass
class Token:
    type: TokenType
    value: Any | None = None
