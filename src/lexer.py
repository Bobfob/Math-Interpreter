from src.tokens import *


class _LexerError(Exception): ...


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = iter(source)
        self.source_lit = source
        self.index = -1

        self.advance()
    
    
    def advance(self, n: int = 1) -> None:
        for _ in range(n):
            try:
                self.cur_char = next(self.source)
                self.index += 1
            
            except StopIteration:
                self.cur_char = None
    
    
    def peek(self, offset: int = 0) -> str:
        return self.source_lit[max(0, min(self.index + offset, len(self.source_lit) - 1))]
    
    
    def is_eof(self, offset: int = 0) -> bool:
        return self.index + offset >= len(self.source_lit)
    
    
    def eat(self) -> str:
        prev = self.peek()
        self.advance()
        return prev

    
    def tokenize(self) -> list[Token]:
        result: list[Token] = []
        
        
        while self.cur_char is not None:
            # Skipping whitespaces
            while self.cur_char is not None and self.cur_char.isspace():
                self.advance()
            
            
            # Checking if is's the end
            if self.cur_char is None:
                break
            
            
            # Numbers
            if self.cur_char.isdigit() or (self.cur_char == '.' and self.peek(offset = 1).isdigit()):
                number = ''
                points = 0

                
                if self.cur_char == '.':
                    points += 1
                    number += self.eat()
                
                
                while self.cur_char != None and (self.cur_char.isdigit() or self.cur_char == '.'):
                    if points > 1:
                        raise _LexerError('Invalid number')

                    
                    number += self.eat()
                    
                    
                    if self.cur_char == '.':
                        points += 1
                        number += self.eat()
                
                
                result.append(Token(TokenType.NumberLit, int(number) if points == 0 else float(number)))
            
            
            # Identifiers
            elif self.cur_char.isalnum() or self.cur_char in '@_':
                ident: str = ""
                is_const: bool = False
                
                
                while self.cur_char != None and (self.cur_char.isalnum() or self.cur_char in '@_'):
                    if ident.count('@') >= 1 and ident[0] != '@':
                        raise _LexerError("Expected '@' symbol in identifier at the start")
                    
                
                    if self.cur_char == '@':
                        is_const = True
                    
                
                    ident += self.eat()
                
                
                    if ident.count('@') > 1:
                        raise _LexerError("Expected only one '@' symbol for constant identifier")
                
                
                result.append(Token(TokenType.ConstIdentifier if is_const else TokenType.Identifier, ident))
            
            
            # Other symbols
            else:
                match self.cur_char:
                    case '(': result.append(Token(TokenType.LParen, self.eat()))
                    case ')': result.append(Token(TokenType.RParen, self.eat()))
                    case '[': result.append(Token(TokenType.LBracket, self.eat()))
                    case ']': result.append(Token(TokenType.RBracket, self.eat()))
                    case '=':
                        if not self.is_eof(1) and self.peek(1) == '=':
                            self.advance(2)
                            result.append(Token(TokenType.BinaryOp, '=='))
                        else:
                            result.append(Token(TokenType.Assign, self.eat()))
                    case '!':
                        if self.peek(1) == '=':
                            self.advance(2)
                            result.append(Token(TokenType.BinaryOp, '!='))
                        else:
                            result.append(Token(TokenType.PostfixOp, self.eat()))
                    case ',': result.append(Token(TokenType.Comma, self.eat()))
                    case '+': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '-': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '*':
                        if self.peek(offset = 1) == '*':
                            self.advance(2)
                            result.append(Token(TokenType.BinaryOp, '**'))
                        else:
                            result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '/': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '%': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '|': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '<':
                        if self.peek(1) == '=':
                            self.advance(2)
                            result.append(Token(TokenType.BinaryOp, '<='))
                        else:
                            result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '>':
                        if self.peek(1) == '=':
                            self.advance(2)
                            result.append(Token(TokenType.BinaryOp, '>='))
                        else:
                            result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '?': result.append(Token(TokenType.PostfixOp, self.eat()))
                    case ':': result.append(Token(TokenType.Colon, self.eat()))
                    case _  : raise _LexerError(f'Invalid symbol: {self.cur_char}')
        
        
        return result
