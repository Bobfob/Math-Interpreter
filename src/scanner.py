from src.tokens import *


class _ScannerError(Exception): ...


# Helper function for string decoding
def _decode_string(body: str) -> str:
    out: list[str] = []
    i, n = 0, len(body)

    while i < n:
        c = body[i]
        
        if c != '\\':
            out.append(c)
            i += 1
            continue
        
        if i + 1 >= n:
            raise _ScannerError("Unterminated escape sequence")
        
        esc = body[i + 1]
        
        if esc not in ESCAPES:
            raise _ScannerError(f"Unknown escape sequence: '\\{esc}'")
        
        out.append(ESCAPES[esc])
        
        i += 2
    
    return "".join(out)


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []


    def _scan_string(self, pos: int) -> tuple[Token, int]:
        m = STRING_RE.match(self.source, pos)

        if m is None:
            raise _ScannerError("Unterminated string literal")
        
        body = m.group(1) if m.group(1) is not None else m.group(2)
        
        return Token(TokenType.StringLit, _decode_string(body)), m.end()


    def _scan_number(self, pos: int) -> tuple[Token, int]:
        m = NUMBER_RE.match(self.source, pos)
        
        if m is None:
            raise _ScannerError("Invalid number")
        
        raw = m.group(0)
        value: int | float = float(raw) if '.' in raw else int(raw)
        
        return Token(TokenType.NumberLit, value), m.end()


    def _scan_identifier(self, pos: int) -> tuple[Token, int]:
        m = IDENT_RE.match(self.source, pos)
        
        if m is None:
            raise _ScannerError("Invalid identifier")

        raw = m.group(0)
        at_count = raw.count('@')
        
        if at_count > 1:
            raise _ScannerError("Expected only one '@' symbol for constant identifier")
        
        if at_count == 1 and not raw.startswith('@'):
            raise _ScannerError("Expected '@' symbol in identifier at the start")

        tt = TokenType.ConstIdentifier if raw.startswith('@') else TokenType.Identifier
        
        return Token(tt, raw), m.end()


    def _scan_operator(self, pos: int) -> tuple[Token, int]:
        src = self.source

        for op, tt in OPERATORS:
            if src.startswith(op, pos):
                return Token(tt, op), pos + len(op)
        
        raise _ScannerError(f"Invalid symbol: '{src[pos]}'")


    def scan(self) -> None:
        src = self.source
        n = len(src)
        pos = 0

        while pos < n:
            ch = src[pos]

            if ch.isspace():
                pos += 1

            elif ch in ('"', "'"):
                tok, pos = self._scan_string(pos)
                self.tokens.append(tok)

            elif ch.isdigit() or (ch == '.' and pos + 1 < n and src[pos + 1].isdigit()):
                tok, pos = self._scan_number(pos)
                self.tokens.append(tok)

            elif ch.isalpha() or ch in ('_', '@'):
                tok, pos = self._scan_identifier(pos)
                self.tokens.append(tok)

            else:
                tok, pos = self._scan_operator(pos)
                self.tokens.append(tok)
