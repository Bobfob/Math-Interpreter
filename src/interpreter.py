import math

from src.calc_parser import *


def factorial(n: int) -> int:
    if not isinstance(n, int): raise TypeError(f'Expected type \'int\', but got \'{type(n).__name__}\'')
    
    elif n < 0: raise ValueError("Expected n >= 0")
    
    elif n == 0: return 1
    
    else: return factorial(n - 1) * n


class ReservedFunctions:
    @staticmethod
    def cos(x) -> float: return math.cos(x)
    @staticmethod
    def sin(x) -> float: return math.sin(x)
    @staticmethod
    def tan(x) -> float: return math.tan(x)
    @staticmethod
    def cot(x) -> float: return 1 / math.tan(x)
    @staticmethod
    def sec(x) -> float: return 1 / math.cos(x)
    @staticmethod
    def csc(x) -> float: return 1 / math.sin(x)
    @staticmethod
    def ln(x) -> float: return math.log(x)
    @staticmethod
    def log(x) -> float: return math.log10(x)
    @staticmethod
    def logn(x, base) -> float: return math.log(x, base)
    @staticmethod
    def exp(x) -> float: return math.exp(x)
    @staticmethod
    def sqrt(x) -> float: return math.sqrt(x)
    @staticmethod
    def cbrt(x) -> float: return math.cbrt(x)
    @staticmethod
    def abs(x) -> float: return abs(x)
    @staticmethod
    def ceil(x) -> float: return math.ceil(x)
    @staticmethod
    def floor(x) -> float: return math.floor(x)
    @staticmethod
    def cosh(x) -> float: return math.cosh(x)
    @staticmethod
    def sinh(x) -> float: return math.sinh(x)
    @staticmethod
    def tanh(x) -> float: return math.tanh(x)
    @staticmethod
    def coth(x) -> float: return 1 / math.tanh(x)
    @staticmethod
    def sech(x) -> float: return 1 / math.cosh(x)
    @staticmethod
    def csch(x) -> float: return 1 / math.sinh(x)
    @staticmethod
    def cos_d(x) -> float: return math.cos(math.radians(x))
    @staticmethod
    def sin_d(x) -> float: return math.sin(math.radians(x))
    @staticmethod
    def tan_d(x) -> float: return math.tan(math.radians(x))
    @staticmethod
    def cot_d(x) -> float: return 1 / math.tan(math.radians(x))
    @staticmethod
    def sec_d(x) -> float: return 1 / math.cos(math.radians(x))
    @staticmethod
    def csc_d(x) -> float: return 1 / math.sin(math.radians(x))
    @staticmethod
    def clamp(x, min_x, max_x) -> int | float: return min(max(x, min_x), max_x)
    @staticmethod
    def min(x, y, *args) -> int | float: return min(x, y, *args)
    @staticmethod
    def max(x, y, *args) -> int | float: return max(x, y, *args)


class _InterpreterError(Exception): ...


class Interpreter:
    def __init__(self, tree: ExprBase, defined_idents: dict[str, int | float], defined_funcs: dict[str, tuple[list[str], ExprBase]]):
        self.tree = tree
        self.defined_identifiers = defined_idents
        self.defined_functions = defined_funcs
        
        self._current_function: str | None = None
        self._call_stack: list[dict[str, Any]] = []
    
    
    def eval(self):
        return self.visit(self.tree)
    
    
    def visit(self, tree: ExprBase):
        visit_method_name = f'visit_{type(tree).__name__}'
        visit_method = getattr(self, visit_method_name)
        
        return visit_method(tree)
    
    
    def visit_PlusNode(self, tree: PlusNode):
        return self.visit(tree.lhs) + self.visit(tree.rhs)
    
    
    def visit_MinusNode(self, tree: MinusNode):
        return self.visit(tree.lhs) - self.visit(tree.rhs)
    
    
    def visit_MulNode(self, tree: MulNode):
        return self.visit(tree.lhs) * self.visit(tree.rhs)
    
    
    def visit_DivNode(self, tree: DivNode):
        return self.visit(tree.lhs) / self.visit(tree.rhs)
    
    
    def visit_PowerNode(self, tree: PowerNode):
        return self.visit(tree.lhs)**self.visit(tree.rhs)
    
    
    def visit_ModNode(self, tree: ModNode):
        return self.visit(tree.lhs) % self.visit(tree.rhs)
    
    
    def visit_UnaryPlusNode(self, tree: UnaryPlusNode):
        return  self.visit(tree.value)
    
    
    def visit_UnaryMinusNode(self, tree: UnaryMinusNode):
        return -self.visit(tree.value)
    
    
    def visit_GTNode(self, tree: GTNode):
        return self.visit(tree.lhs) > self.visit(tree.rhs)
    
    
    def visit_GTENode(self, tree: GTENode):
        return self.visit(tree.lhs) >= self.visit(tree.rhs)
    
    
    def visit_LTNode(self, tree: LTNode):
        return self.visit(tree.lhs) < self.visit(tree.rhs)
    
    
    def visit_LTENode(self, tree: LTENode):
        return self.visit(tree.lhs) <= self.visit(tree.rhs)
    
    
    def visit_EQNode(self, tree: EQNode):
        return self.visit(tree.lhs) == self.visit(tree.rhs)
    
    
    def visit_NEQNode(self, tree: NEQNode):
        return self.visit(tree.lhs) != self.visit(tree.rhs)
    
    
    def visit_NumberNode(self, tree: NumberNode):
        return tree.value
    
    
    def visit_FactorialNode(self, tree: FactorialNode):
        return factorial(self.visit(tree.value))
    
    
    def visit_TernaryOpNode(self, tree: TernaryOpNode):
        test_result: bool = bool(self.visit(tree.test_expr))
        
        if test_result:
            return self.visit(tree.success_expr)
        
        return self.visit(tree.failed_expr)
    
    
    def evaluate_function_arguments(self, args: list[ExprBase]) -> list[Any]:
        return [self.visit(arg) for arg in args]
    
    
    def visit_FunctionCall(self, tree: FunctionCall) -> Any:
        if tree.name in RESERVED_FUNCTIONS:
            func_args = self.evaluate_function_arguments(tree.args)
            cur_method = getattr(ReservedFunctions, tree.name)
            
            return cur_method(*func_args)
        
        
        elif tree.name in self.defined_functions:
            params, body = self.defined_functions[tree.name]
            
            
            # If length of passed arguments miss match with number of defined parameters
            # then we're rasing _InterpreterError
            if len(tree.args) != len(params):
                f_name: str = f"\"{tree.name}\"" if len(tree.name) > 1 else f"'{tree.name}'" if len(tree.name) == 1 else f"\"{tree.name}\""
                raise _InterpreterError(f"Expected {len(params)} arguments in {f_name} function call")
            
            
            # Creating new local context
            self._current_function = tree.name
            locals_dict: dict[str, Any] = {}
            
            
            # Evaluating arguments and passing them to the function
            args = [self.visit(arg) for arg in tree.args]
            
            for param_name, arg_value in zip(params, args):
                locals_dict[param_name] = arg_value
            
            
            # Pushing locals to the stack
            self._call_stack.append(locals_dict)
            
            
            # Evaluating function body
            try:
                result = self.visit(body)
            
            finally:
                self._call_stack.pop()
            
            
            # Returning result
            return result
        
        
        raise _InterpreterError(f"Undefined function: \"{tree.name}\"")
    
    
    def visit_IdentNode(self, tree: IdentNode):
        for locals_dict in reversed(self._call_stack):
            if tree.ident in locals_dict:
                return locals_dict[tree.ident]
        
        
        if tree.ident in self.defined_identifiers:
            return self.defined_identifiers[tree.ident]
        
        
        raise _InterpreterError(f'Undefined identifier: "{tree.ident}"')
    
    
    def visit_AssignmentExpr(self, tree: AssignmentExpr):
        if tree.assign_to in self.defined_identifiers and tree.assign_to[0] == '@':
            raise _InterpreterError(f"Variable '{tree.assign_to}' is readonly")
        
        
        value = self.visit(tree.expr)
        self.defined_identifiers[tree.assign_to] = value
        return value
    
    
    def visit_FuncDeclaration(self, tree: FuncDeclaration):
        if tree.name in self.defined_functions:
            raise _InterpreterError(f"Function '{tree.name}' already defined")
        
        
        elif tree.name in RESERVED_FUNCTIONS:
            raise _InterpreterError("Cannot override reserved function")
        
        
        self.defined_functions[tree.name] = ([param.ident for param in tree.params], tree.expr) # type: ignore
    
    
    def visit_DeleteExpr(self, tree: DeleteExpr):
        if tree.ident in self.defined_identifiers:
            if tree.ident in ("@pi", "@e", "@tau"):
                raise _InterpreterError("Cannot delete predefined constants")
            
            del self.defined_identifiers[tree.ident]
            return
        
        
        elif tree.ident in self.defined_functions:
            del self.defined_functions[tree.ident]
            return
        
        
        elif tree.ident in RESERVED_FUNCTIONS:
            raise _InterpreterError("Cannot delete reserved function")
        
        
        raise _InterpreterError(f"Cannot delete undefined name: {tree.ident}") # UNREACHABLE
    
    
    def visit_ModuleExpr(self, tree: ModuleExpr):
        return abs(self.visit(tree.expr))
    
    
    def visit_Point2DNode(self, tree: Point2DNode):
        return Point2D(self.visit(tree.value[0]), self.visit(tree.value[1]))
    
    
    def visit_Point3DNode(self, tree: Point3DNode):
        return Point3D(self.visit(tree.value[0]), self.visit(tree.value[1]), self.visit(tree.value[2]))
    
    
    def visit_IndexNode(self, tree: IndexNode):
        subscriptable = self.visit(tree.parent)
        
        if not isinstance(subscriptable, (Point2D, Point3D)):
            raise _InterpreterError("You can only subscript points (Point2D and Point3D)")
        
        return subscriptable[self.visit(tree.value)]
