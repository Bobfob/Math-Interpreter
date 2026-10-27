from src.tokens   import *
from src.nodes    import *


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
        expr = self.parse_statement()
        
        if self.cur_token is not None:
            raise _ParserError(f"Unexpected token: '{self.cur_token.value}'")
            
        return expr
    
    
    def parse_statement(self) -> ExprBase:
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
                    
                    # Assignment expression
                    else:
                        return self.try_parse_assignment_expr()
                
                # Else it's just an expression
                case _:
                    return self.try_parse_assignment_expr()
        
        raise _ParserError("Expected token")


    def try_parse_assignment_expr(self) -> ExprBase:
        lvalue: ExprBase = self.parse_expr()

        if self.cur_token is not None and self.cur_token.type in (TokenType.Assign, TokenType.AugAssign):
            op = self.cur_token.value
            self.advance()
            
            rvalue: ExprBase = self.try_parse_assignment_expr()

            if isinstance(lvalue, FunctionCall):
                if op != '=':
                    raise _ParserError("Augmented assignment is not allowed in function declaration")
                for arg in lvalue.args:
                    if not isinstance(arg, IdentNode):
                        raise _ParserError("Expected parameters not arguments in function declaration")
                return FuncDeclaration(lvalue.name, lvalue.args, rvalue)

            else:
                if op == '=':
                    return AssignmentExpr(lvalue, rvalue)
                elif op == '+=':
                    return AssignmentExpr(lvalue, PlusNode(lvalue, rvalue))
                elif op == '-=':
                    return AssignmentExpr(lvalue, MinusNode(lvalue, rvalue))
                elif op == '*=':
                    return AssignmentExpr(lvalue, MulNode(lvalue, rvalue))
                elif op == '/=':
                    return AssignmentExpr(lvalue, DivNode(lvalue, rvalue))
                elif op == '%=':
                    return AssignmentExpr(lvalue, ModNode(lvalue, rvalue))
                elif op == '**=':
                    return AssignmentExpr(lvalue, PowerNode(lvalue, rvalue))
                elif op == '&=':
                    return AssignmentExpr(lvalue, BitwiseAndNode(lvalue, rvalue))
                elif op == '|=':
                    return AssignmentExpr(lvalue, BitwiseOrNode(lvalue, rvalue))
                elif op == '^=':
                    return AssignmentExpr(lvalue, BitwiseXorNode(lvalue, rvalue))

        return lvalue
    
    
    def parse_func_params_or_args(self) -> list[ExprBase]:
        params: list[ExprBase] = []
        
        while self.cur_token != None and self.cur_token.type != TokenType.RParen:
            expr: ExprBase = self.try_parse_assignment_expr()
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
        lhs = self.parse_expr_bitwise()
        
        while self.cur_token is not None and self.cur_token.value in ('<', '<=', '>', '>=', '==', '!='):
            match self.cur_token.value:
                case '<':
                    self.advance()
                    lhs = LTNode(lhs, self.parse_expr_bitwise())
                
                case '<=':
                    self.advance()
                    lhs = LTENode(lhs, self.parse_expr_bitwise())
                
                case '==':
                    self.advance()
                    lhs = EQNode(lhs, self.parse_expr_bitwise())
                
                case '!=':
                    self.advance()
                    lhs = NEQNode(lhs, self.parse_expr_bitwise())
                
                case '>':
                    self.advance()
                    lhs = GTNode(lhs, self.parse_expr_bitwise())
                
                case '>=':
                    self.advance()
                    lhs = GTENode(lhs, self.parse_expr_bitwise())
        
        return lhs

    def parse_expr_bitwise(self) -> ExprBase:
        lhs = self.parse_expr_tail()

        while self.cur_token is not None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value in ('&', '|', '^'):
            match self.cur_token.value:
                case '&':
                    self.advance()
                    lhs = BitwiseAndNode(lhs, self.parse_expr_tail())
                
                case '|':
                    self.advance()
                    lhs = BitwiseOrNode(lhs, self.parse_expr_tail())
                
                case '^':
                    self.advance()
                    lhs = BitwiseXorNode(lhs, self.parse_expr_tail())
        
        return lhs
    
    
    def parse_expr_tail(self) -> ExprBase:
        lhs = self.parse_term()

        while self.cur_token != None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value in ('+', '-'):
            match self.cur_token.value:
                case '+':
                    self.advance()
                    lhs = PlusNode(lhs, self.parse_term())
            
                case '-':
                    self.advance()
                    lhs = MinusNode(lhs, self.parse_term())
        
        return lhs


    def parse_term(self) -> ExprBase:
        lhs = self.parse_power()
        
        while self.cur_token != None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value in ('*', '/', '%'):
            match self.cur_token.value:
                case '*':
                    self.advance()
                    lhs = MulNode(lhs, self.parse_power())
                
                case '/':
                    self.advance()
                    lhs = DivNode(lhs, self.parse_power())
                
                case '%':
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
        
        while self.cur_token != None and self.cur_token.value in ('!', '[', '::'):
            match self.cur_token.value:
                case '!':
                    self.advance()
                    lhs = FactorialNode(lhs)
                
                case '[':
                    self.advance()
                    value: ExprBase = self.parse_expr()
                    self.expected(TokenType.RBracket, ']')
                    
                    lhs = IndexNode(lhs, value)

                case '::':
                    self.advance()
                    node = self.parse_primary()

                    if not isinstance(node, (IdentNode, FunctionCall)):
                        raise _ParserError("Expected identifier or function call after ::")

                    lhs = AccessNode(lhs, node)
        
        return lhs
    
    
    def parse_primary(self) -> ExprBase:
        tok = self.cur_token

        if tok == None:
            raise _ParserError('Invalid expression')

        elif tok.type == TokenType.LBrace:
            self.advance()
            parsed_hash_table = self.parse_primary_hash_table()
            self.expected(TokenType.RBrace, '}')

            return parsed_hash_table

        elif tok.type == TokenType.LBracket:
            self.advance()
            parsed_array = self.parse_primary_array()
            self.expected(TokenType.RBracket, ']')

            return parsed_array
        
        elif tok.type == TokenType.LParen:
            self.advance()
            result = self.try_parse_assignment_expr()
            
            if self.cur_token is not None and self.cur_token.type == TokenType.Comma:
                self.advance()
                
                if isinstance(result, (Point2DNode, Point3DNode)):
                    raise _ParserError("Point literal cannot contain other point literal")
                
                point = [result]
                
                while self.cur_token is not None and self.cur_token.type != TokenType.RParen:
                    expr = self.try_parse_assignment_expr()
                    
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
            return NumberNode(tok.value)

        elif tok.type == TokenType.StringLit:
            self.advance()
            return StringNode(tok.value)
        
        elif tok.type == TokenType.Identifier or tok.type == TokenType.ConstIdentifier:
            name: str = tok.value
            self.advance()
            
            if name == "true" and (self.cur_token is None or self.cur_token.type != TokenType.LParen):
                return BoolNode(True)
            elif name == "false" and (self.cur_token is None or self.cur_token.type != TokenType.LParen):
                return BoolNode(False)
            
            if self.cur_token is not None and self.cur_token.type == TokenType.LParen:
                self.advance()
                call_args = self.parse_func_params_or_args()
                self.expected(TokenType.RParen, ')')
                
                return FunctionCall(name, call_args)
            
            return IdentNode(name)

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


    def parse_primary_array(self) -> ArrayNode:
        result: list[ExprBase] = []

        while self.cur_token is not None and self.cur_token.type != TokenType.RBracket:
            result.append(self.parse_primary())

            if self.cur_token is not None and self.cur_token.type != TokenType.RBracket:
                self.expected(TokenType.Comma, ',')

        return ArrayNode(result)


    def parse_primary_hash_table(self) -> HashTableNode:
        fields: list[HashTableFieldNode] = []
        seen_keys: set[str] = set()

        while self.cur_token is not None and self.cur_token.type != TokenType.RBrace:
            field = self.parse_primary_hash_table_field()

            key_repr = str(field.key)
            if key_repr in seen_keys:
                raise _ParserError(f"Key ({field.key}) is duplicated")
            seen_keys.add(key_repr)

            fields.append(field)

            if self.cur_token is not None and self.cur_token.type != TokenType.RBrace:
                self.expected(TokenType.Comma, ',')

            elif self.cur_token is None:
                raise _ParserError("Expected '}'")

        return HashTableNode(fields)


    def parse_primary_hash_table_field(self) -> HashTableFieldNode:
        key = self.parse_primary()
        self.expected(TokenType.Colon, ":")
        value = self.parse_expr()

        return HashTableFieldNode(key, value)
