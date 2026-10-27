import re

from dataclasses import dataclass
from typing      import Any
from enum        import Enum, auto


class TokenType(Enum):
    Identifier = auto()
    ConstIdentifier = auto()
    Assign = auto()
    AugAssign = auto()
    NumberLit = auto()
    StringLit = auto()
    LParen = auto()
    RParen = auto()
    LBracket = auto()
    RBracket = auto()
    LBrace = auto()
    RBrace = auto()
    BinaryOp = auto()
    PostfixOp = auto()
    Comma = auto()
    Colon = auto()
    DoubleColon = auto()


@dataclass
class Token:
    type: TokenType
    value: Any | None = None


STRING_RE = re.compile(
    r'"((?:[^"\\]|\\.)*)"'
    r"|'((?:[^'\\]|\\.)*)'",
    re.DOTALL,
)

NUMBER_RE = re.compile(r'(?:\d+(?:\.\d*)?|\.\d+)(?![.\d])')

IDENT_RE = re.compile(r'[^\W\d@][\w@]*|@[\w@]*')

OPERATORS: tuple[tuple[str, TokenType], ...] = (
    ('==', TokenType.BinaryOp),
    ('!=', TokenType.BinaryOp),
    ('**=', TokenType.AugAssign),
    ('+=', TokenType.AugAssign),
    ('-=', TokenType.AugAssign),
    ('*=', TokenType.AugAssign),
    ('/=', TokenType.AugAssign),
    ('%=', TokenType.AugAssign),
    ('&=', TokenType.AugAssign),
    ('|=', TokenType.AugAssign),
    ('^=', TokenType.AugAssign),
    ('**', TokenType.BinaryOp),
    ('<=', TokenType.BinaryOp),
    ('>=', TokenType.BinaryOp),
    ('::', TokenType.DoubleColon),
    ('(',  TokenType.LParen),
    (')',  TokenType.RParen),
    ('[',  TokenType.LBracket),
    (']',  TokenType.RBracket),
    ('{',  TokenType.LBrace),
    ('}',  TokenType.RBrace),
    ('=',  TokenType.Assign),
    (',',  TokenType.Comma),
    ('+',  TokenType.BinaryOp),
    ('-',  TokenType.BinaryOp),
    ('*',  TokenType.BinaryOp),
    ('/',  TokenType.BinaryOp),
    ('&',  TokenType.BinaryOp),
    ('|',  TokenType.BinaryOp),
    ('^',  TokenType.BinaryOp),
    ('%',  TokenType.BinaryOp),
    ('|',  TokenType.BinaryOp),
    ('<',  TokenType.BinaryOp),
    ('>',  TokenType.BinaryOp),
    ('!',  TokenType.PostfixOp),
    ('?',  TokenType.PostfixOp),
    (':',  TokenType.Colon),
)

ESCAPES: dict[str, str] = {
    'n':  '\n',
    't':  '\t',
    'r':  '\r',
    '0':  '\0',
    '\\': '\\',
    '"':  '"',
    "'":  "'",
}
