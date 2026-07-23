from src.lexer import *
from src.nodes import *


RESERVED_FUNCTIONS = (
    "cos",   "sin",   "tan",
    "cot",   "sec",   "csc",
    "ln",    "log",   "logn",
    "exp",   "sqrt",  "cbrt",
    "abs",   "floor", "ceil",
    "cosh",  "sinh",  "tanh",
    "coth",  "sech",  "csch",
    "cos_d", "sin_d", "tan_d",
    "cot_d", "sec_d", "csc_d",
    "clamp", "min",   "max",
)


class _ParserError(Exception): ...


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = iter(tokens)
        self.tokens_lit = tokens
        self.index = -1

        self.advance()
    
    
    def advance(self) -> None:
        try:
            self.cur_token = next(self.tokens)
            self.index += 1
        
        except StopIteration:
            self.cur_token = None
    
    
    def peek(self, offset = 0) -> Token:
        return self.tokens_lit[max(0, min(self.index + offset, len(self.tokens_lit) - 1))]

    
    def eat(self) -> Token:
        prev = self.peek()
        self.advance()
        return prev

    
    def expected(self, check: TokenType, explanation: str, expected_value: str | None = None, use_quotes: bool = True) -> None:
        if self.cur_token == None or self.cur_token.type != check or (expected_value is not None and self.cur_token.value != expected_value):
            raise _ParserError(f"Expected \"{explanation}\"" if use_quotes else f"Expected {explanation}")
        
        self.advance()
    
    
    def eat_expected(self, check: TokenType, explanation: str) -> Token:
        prev = self.peek()
        self.expected(check, explanation)
        return prev


    def parse(self) -> ExprBase:
        return self.parse_statements()
    
    
    def parse_statements(self) -> ExprBase:
        while self.cur_token != None:
            match self.cur_token.type:
                case TokenType.Identifier | TokenType.ConstIdentifier:
                    # Delete expression
                    if self.cur_token.value == "del":
                        self.advance()
                        ident = self.parse_expr()
                        
                        
                        if not isinstance(ident, IdentNode):
                            raise _ParserError("Expected identifier to delete")
                        
                        
                        return DeleteExpr(ident.ident)
                    
                    
                    # Variable reassignment: "IDENT '=' EXPR"
                    elif self.peek(offset = 1).type == TokenType.Assign:
                        return self.parse_assignment_expr()
                    
                    
                    # Function declaration/call:
                    #   - "IDENT '(' ARGS ')' '=' EXPR"
                    #   - "IDENT '(' ARGS ')'"
                    elif self.peek(offset = 1).type == TokenType.LParen:
                        if self.cur_token.type == TokenType.ConstIdentifier:
                            raise _ParserError("Function cannot be constants")
                        
                        
                        # Parsing function only when '=' sign is in expression
                        if any([t.type == TokenType.Assign for t in self.tokens_lit]):
                            return self.parse_func()
                    
                    
                    # Else we just found some identifier in some expression
                    return self.parse_expr()
                
                
                # Else it's just an expression
                case _:
                    return self.parse_expr()
        
        
        raise _ParserError("Expected token")
    
    
    def parse_assignment_expr(self) -> ExprBase:
        # if we have situation like this: "(x + 1) = expr" we have to check the
        # type of lhs of assignment expression, because it's must be an identifier
        # and neither of BinaryExpr
        assign_to = self.parse_expr()
        
        
        if not isinstance(assign_to, IdentNode):
            raise _ParserError("Expected identifier, but got expression")
        
        
        # overriding variable to string
        assign_to = assign_to.ident
        
        
        # expecting next token is equals sign
        self.expected(TokenType.Assign, '=')
        
        
        # catching expression
        expr = self.parse_expr()
        
        
        return AssignmentExpr(assign_to, expr)
        
    
    def parse_func(self, ) -> ExprBase:
        name: str = self.eat_expected(TokenType.Identifier, 'identifier').value # type: ignore
        
        
        self.expected(TokenType.LParen, '(')
        params = self.parse_func_params_or_args(True)
        self.expected(TokenType.RParen, ')')
        
        
        if self.cur_token is not None and self.cur_token.type == TokenType.Assign:
            self.advance()
            expr = self.parse_expr()
            return FuncDeclaration(name, params, expr)
        
        
        raise _ParserError("Invalid function expression")
    
    
    def parse_func_params_or_args(self, is_params: bool) -> list[IdentNode | ExprBase]:
        params: list[IdentNode | ExprBase] = []
        
        
        while self.cur_token != None and self.cur_token.type != TokenType.RParen:
            if is_params:
                ident: ExprBase = self.parse_expr()
                
                
                if not isinstance(ident, IdentNode):
                    raise _ParserError("Expected identifier as parameter")
                
                
                elif ident.ident[0] == '@':
                    raise _ParserError("Function parameters cannot be constant")
            
            
                params.append(ident)
            
            
            else:
                expr: ExprBase = self.parse_expr()
                params.append(expr)
            
        
            if self.cur_token.type != TokenType.RParen:
                self.expected(TokenType.Comma, ',')
        
        
        return params


    def parse_expr(self) -> ExprBase:
        return self.parse_expr_ternary()
    
    
    def parse_expr_ternary(self) -> ExprBase:
        expr = self.parse_expr_comparison()
        
        
        if self.cur_token is not None and self.cur_token.value == '?':
            self.advance()
            success_expr = self.parse_expr_ternary()
            
            self.expected(TokenType.Colon, ':')
            failed_expr = self.parse_expr_ternary()
            
            return TernaryOpNode(expr, success_expr, failed_expr)
        
        
        return expr
    
    
    def parse_expr_comparison(self) -> ExprBase:
        lhs = self.parse_expr_tail()
        
        
        while self.cur_token is not None and self.cur_token.value in ('<', '<=', '>', '>=', '==', '!='):
            match self.cur_token.value:
                case '<':
                    self.advance()
                    lhs = LTNode(lhs, self.parse_expr_tail())
                
                case '<=':
                    self.advance()
                    lhs = LTENode(lhs, self.parse_expr_tail())
                
                case '==':
                    self.advance()
                    lhs = EQNode(lhs, self.parse_expr_tail())
                
                case '!=':
                    self.advance()
                    lhs = NEQNode(lhs, self.parse_expr_tail())
                
                case '>':
                    self.advance()
                    lhs = GTNode(lhs, self.parse_expr_tail())
                
                case '>=':
                    self.advance()
                    lhs = GTENode(lhs, self.parse_expr_tail())
        
        
        return lhs
    
    
    def parse_expr_tail(self) -> ExprBase:
        lhs = self.parse_term()

        
        while self.cur_token != None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value in ('+', '-'):
            if self.cur_token.value == '+':
                self.advance()
                lhs = PlusNode(lhs, self.parse_term())
            
        
            elif self.cur_token.value == '-':
                self.advance()
                lhs = MinusNode(lhs, self.parse_term())
        
        
        return lhs


    def parse_term(self) -> ExprBase:
        lhs = self.parse_power()

        
        while self.cur_token != None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value in ('*', '/', '%'):
            if self.cur_token.value == '*':
                self.advance()
                lhs = MulNode(lhs, self.parse_power())
            
        
            elif self.cur_token.value == '/':
                self.advance()
                lhs = DivNode(lhs, self.parse_power())
            
        
            elif self.cur_token.value == '%':
                self.advance()
                lhs = ModNode(lhs, self.parse_power())
        
        
        return lhs

    
    def parse_power(self) -> ExprBase:
        lhs = self.parse_postfix()

        
        while self.cur_token != None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value == '**':
            self.advance()
            lhs = PowerNode(lhs, self.parse_postfix())
        
        
        return lhs
    
    
    def parse_postfix(self) -> ExprBase:
        lhs = self.parse_primary()
        
        
        while self.cur_token != None and self.cur_token.value in ('!', '['):
            if self.cur_token.value == '!':
                self.advance()
                lhs = FactorialNode(lhs)
            
            
            elif self.cur_token.value == '[':
                self.advance()
                value: ExprBase = self.parse_expr()
                self.expected(TokenType.RBracket, ']')
                
                lhs = IndexNode(lhs, value)
        
        
        return lhs
    
    
    def parse_primary(self) -> ExprBase:
        tok = self.cur_token

        
        if tok == None:
            raise _ParserError('Invalid expression')
        
        
        elif tok.type == TokenType.LParen:
            self.advance()
            result = self.parse_expr()
            
            
            if self.cur_token is not None and self.cur_token.type == TokenType.Comma:
                self.advance()
                
                
                if isinstance(result, (Point2DNode, Point3DNode)):
                    raise _ParserError("Point literal cannot contain other point literal")
                
                
                point = [result]
                
                
                while self.cur_token is not None and self.cur_token.type != TokenType.RParen:
                    expr = self.parse_expr()
                    
                    if isinstance(expr, (Point2DNode, Point3DNode)):
                        raise _ParserError("Point literal cannot contain other point literal")
                    
                    point.append(expr)
                    
                    
                    if self.cur_token is not None and self.cur_token.type == TokenType.Comma:
                        self.advance()
                        
                        if self.cur_token is not None and self.cur_token.type == TokenType.Comma:
                            raise _ParserError("Trailing comma in point literal")
                
                
                if len(point) == 2:
                    self.advance()
                    return Point2DNode((point[0], point[1]))
                
                
                elif len(point) == 3:
                    self.advance()
                    return Point3DNode((point[0], point[1], point[2]))
                
                
                raise _ParserError("Expected 2 or 3 values (expressions) for point literal")
            
            
            self.expected(TokenType.RParen, ')')
            
            
            return result
        
        
        elif tok.type == TokenType.NumberLit:
            self.advance()
            
            return NumberNode(tok.value) # type: ignore

        
        elif tok.type == TokenType.Identifier or tok.type == TokenType.ConstIdentifier:
            name: str = tok.value # type: ignore
            self.advance()
            
            
            if self.cur_token is not None and self.cur_token.type == TokenType.LParen:
                self.advance()
                call_args = self.parse_func_params_or_args(False)
                self.expected(TokenType.RParen, ')')
            
                
                return FunctionCall(name, call_args)
            
            
            return IdentNode(name) # type: ignore

        
        elif tok.type == TokenType.BinaryOp:
            match tok.value:
                case '+':
                    self.advance()
                    return UnaryPlusNode(self.parse_primary())
                
        
                case '-':
                    self.advance()
                    return UnaryMinusNode(self.parse_primary())
                
                
                case '|':
                    self.advance()
                    expr: ExprBase = self.parse_expr()
                    self.expected(TokenType.BinaryOp, '|', expected_value='|')
                    
                    return ModuleExpr(expr)
                
                
                case _:
                    raise _ParserError(f"Unexpected operator '{tok.value}'")
        
        
        raise _ParserError("Invalid expression")
