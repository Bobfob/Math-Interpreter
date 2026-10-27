from src.builtins    import *
from src.datatypes   import *
from src.calc_parser import *


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


    # ------------------------------------------------------------------ #
    #                       ARITHMETIC / LOGIC                           #
    # ------------------------------------------------------------------ #

    def visit_PlusNode(self, tree: PlusNode):
        return self.visit(tree.lhs) + self.visit(tree.rhs)


    def visit_MinusNode(self, tree: MinusNode):
        return self.visit(tree.lhs) - self.visit(tree.rhs)


    def visit_MulNode(self, tree: MulNode):
        return self.visit(tree.lhs) * self.visit(tree.rhs)


    def visit_DivNode(self, tree: DivNode):
        return self.visit(tree.lhs) / self.visit(tree.rhs)


    def visit_PowerNode(self, tree: PowerNode):
        return self.visit(tree.lhs) ** self.visit(tree.rhs)


    def visit_ModNode(self, tree: ModNode):
        return self.visit(tree.lhs) % self.visit(tree.rhs)


    def visit_UnaryPlusNode(self, tree: UnaryPlusNode):
        return +self.visit(tree.value)


    def visit_UnaryMinusNode(self, tree: UnaryMinusNode):
        return -self.visit(tree.value)


    def visit_GTNode(self, tree: GTNode):
        return Boolean(self.visit(tree.lhs) > self.visit(tree.rhs))

    
    def visit_GTENode(self, tree: GTENode):
        return Boolean(self.visit(tree.lhs) >= self.visit(tree.rhs))

    
    def visit_LTNode(self, tree: LTNode):
        return Boolean(self.visit(tree.lhs) < self.visit(tree.rhs))

    
    def visit_LTENode(self, tree: LTENode):
        return Boolean(self.visit(tree.lhs) <= self.visit(tree.rhs))

    
    def visit_EQNode(self, tree: EQNode):
        return Boolean(self.visit(tree.lhs) == self.visit(tree.rhs))

    
    def visit_NEQNode(self, tree: NEQNode):
        return Boolean(self.visit(tree.lhs) != self.visit(tree.rhs))
    
    
    def visit_BitwiseAndNode(self, tree: BitwiseAndNode):
        return self.visit(tree.lhs) & self.visit(tree.rhs)


    def visit_BitwiseOrNode(self, tree: BitwiseOrNode):
        return self.visit(tree.lhs) | self.visit(tree.rhs)
    
    
    def visit_BitwiseXorNode(self, tree: BitwiseXorNode):
        return self.visit(tree.lhs) ^ self.visit(tree.rhs)


    def visit_NumberNode(self, tree: NumberNode):
        return Number(tree.value)


    def visit_StringNode(self, tree: StringNode):
        return String(tree.value)
    
    
    def visit_BoolNode(self, tree: BoolNode):
        return Boolean(tree.value)


    def visit_FactorialNode(self, tree: FactorialNode):
        return Number(factorial(int(self.visit(tree.value))))


    def visit_TernaryOpNode(self, tree: TernaryOpNode):
        test_result: bool = bool(self.visit(tree.test_expr))

        if test_result:
            return self.visit(tree.success_expr)

        return self.visit(tree.failed_expr)


    def visit_ModuleExpr(self, tree: ModuleExpr):
        return abs(self.visit(tree.expr))


    # ------------------------------------------------------------------ #
    #                       FUNCTIONS / IDENTIFIERS                      #
    # ------------------------------------------------------------------ #

    def evaluate_function_arguments(self, args: list[ExprBase]) -> list[Any]:
        return [self.visit(arg) for arg in args]


    def visit_FunctionCall(self, tree: FunctionCall) -> Any:
        if tree.name in RESERVED_FUNCTIONS_NAMES:
            func_args = self.evaluate_function_arguments(tree.args)
            cur_method = getattr(ReservedFunctions, tree.name)
            result = cur_method(*func_args)

            # Wrap native scalars in Number so they can participate in
            # operations with interpreter datatypes (Number arithmetic,
            # hash table keys, etc.)
            if isinstance(result, (int, float)) and not isinstance(result, bool):
                return Number(result)

            return result

        elif tree.name in self.defined_functions:
            params, body = self.defined_functions[tree.name]

            if len(tree.args) != len(params):
                f_name: str = (
                    f"\"{tree.name}\"" if len(tree.name) > 1
                    else f"'{tree.name}'" if len(tree.name) == 1
                    else f"\"{tree.name}\""
                )
                raise _InterpreterError(f"Expected {len(params)} arguments in {f_name} function call")

            self._current_function = tree.name
            locals_dict: dict[str, Any] = {}

            args = [self.visit(arg) for arg in tree.args]

            for param_name, arg_value in zip(params, args):
                locals_dict[param_name] = arg_value

            self._call_stack.append(locals_dict)

            try:
                result = self.visit(body)
            finally:
                self._call_stack.pop()

            return result

        raise _InterpreterError(f"Undefined function: \"{tree.name}\"")


    def visit_IdentNode(self, tree: IdentNode):
        for locals_dict in reversed(self._call_stack):
            if tree.ident in locals_dict:
                return locals_dict[tree.ident]

        if tree.ident in self.defined_identifiers:
            return self.defined_identifiers[tree.ident]

        raise _InterpreterError(f'Undefined identifier: "{tree.ident}"')


    def visit_FuncDeclaration(self, tree: FuncDeclaration):
        if tree.name in self.defined_functions:
            raise _InterpreterError(f"Function '{tree.name}' already defined")

        elif tree.name in RESERVED_FUNCTIONS_NAMES:
            raise _InterpreterError("Cannot override reserved function")

        self.defined_functions[tree.name] = (
            [param.ident for param in tree.params],  # type: ignore
            tree.expr
        )


    def visit_DeleteExpr(self, tree: DeleteExpr):
        if tree.ident in self.defined_identifiers:
            if tree.ident in ("@pi", "@e", "@tau"):
                raise _InterpreterError("Cannot delete predefined constants")

            del self.defined_identifiers[tree.ident]
            return

        elif tree.ident in self.defined_functions:
            del self.defined_functions[tree.ident]
            return

        elif tree.ident in RESERVED_FUNCTIONS_NAMES:
            raise _InterpreterError("Cannot delete reserved function")

        raise _InterpreterError(f"Cannot delete undefined name: {tree.ident}")


    # ------------------------------------------------------------------ #
    #                            ASSIGNMENT                              #
    # ------------------------------------------------------------------ #

    def visit_AssignmentExpr(self, tree: AssignmentExpr):
        # ---- Plain identifier:  x = E -------------------------------- #
        if isinstance(tree.assign_to, IdentNode):
            name = tree.assign_to.ident

            if name in self.defined_identifiers and name[0] == '@':
                raise _InterpreterError(f"Variable '{name}' is readonly")

            value = self.visit(tree.expr)

            # If the name exists in any active call frame, write into the
            # innermost one (this fixes the "parameter overwritten globally"
            # bug for x = x + 1 inside f(x) = ...).
            for locals_dict in reversed(self._call_stack):
                if name in locals_dict:
                    locals_dict[name] = value
                    return value

            # Otherwise fall back to global scope
            self.defined_identifiers[name] = value
            return value

        # ---- Index:  parent[E] = E ----------------------------------- #
        elif isinstance(tree.assign_to, IndexNode):
            parent = self.visit(tree.assign_to.parent)

            if isinstance(parent, String):
                raise _InterpreterError("String is immutable and does not support item assignment")

            key = self.visit(tree.assign_to.value)
            value = self.visit(tree.expr)

            if not isinstance(parent, (Point2D, Point3D, Array, HashTable)):
                raise _InterpreterError(f"{type(parent).__name__} is not subscriptable")

            try:
                parent[key] = value
            except (KeyError, IndexError, TypeError, AttributeError) as e:
                raise _InterpreterError(str(e))

            return value

        # ---- Attribute:  parent::ident = E --------------------------- #
        elif isinstance(tree.assign_to, AccessNode):
            parent = self.visit(tree.assign_to.parent)
            child = tree.assign_to.child

            if not isinstance(child, IdentNode):
                raise _InterpreterError(
                    "Left-hand side of attribute assignment must be an identifier, "
                    f"got {type(child).__name__}"
                )

            value = self.visit(tree.expr)

            try:
                parent.set_property(child.ident, value)
            except (AttributeError, TypeError) as e:
                raise _InterpreterError(str(e))

            return value

        raise _InterpreterError("Unexpected value to assign")


    # ------------------------------------------------------------------ #
    #                        COMPOSITE DATATYPES                         #
    # ------------------------------------------------------------------ #

    def visit_Point2DNode(self, tree: Point2DNode):
        x = self.visit(tree.value[0])
        y = self.visit(tree.value[1])

        if not isinstance(x, Number) or not isinstance(y, Number):
            raise _InterpreterError("Expected number as value of Point2D")

        return Point2D(x, y)


    def visit_Point3DNode(self, tree: Point3DNode):
        x = self.visit(tree.value[0])
        y = self.visit(tree.value[1])
        z = self.visit(tree.value[2])

        if not isinstance(x, Number) or not isinstance(y, Number) or not isinstance(z, Number):
            raise _InterpreterError("Expected number as value of Point3D")

        return Point3D(x, y, z)


    def visit_IndexNode(self, tree: IndexNode):
        subscriptable = self.visit(tree.parent)

        if not isinstance(subscriptable, (Point2D, Point3D, Array, HashTable, String)):
            raise _InterpreterError(f"{type(subscriptable).__name__} is not subscriptable")

        key = self.visit(tree.value)

        try:
            return subscriptable[key]
        except (KeyError, IndexError, TypeError, AttributeError) as e:
            raise _InterpreterError(str(e))


    def visit_AccessNode(self, tree: AccessNode):
        parent = self.visit(tree.parent)
        child = tree.child

        if isinstance(child, IdentNode):
            try:
                return parent.get_property(child.ident)
            except AttributeError as e:
                raise _InterpreterError(str(e))

        if isinstance(child, FunctionCall):
            args = self.evaluate_function_arguments(child.args)
            try:
                return parent.call_method(child.name, args)
            except AttributeError as e:
                raise _InterpreterError(str(e))
            except TypeError as e:
                raise _InterpreterError(str(e))

        raise _InterpreterError(f"Invalid member access: {type(child).__name__}")


    def visit_ArrayNode(self, tree: ArrayNode):
        return Array([self.visit(v) for v in tree.value])


    def visit_HashTableNode(self, tree: HashTableNode):
        result: dict[BaseDatatype, BaseDatatype] = {}

        for field in tree.value:
            key = self.visit(field.key)
            value = self.visit(field.value)

            if not isinstance(key, HASHABLE_KEY_TYPES):
                raise _InterpreterError(
                    f"Unsupported hash table key type: {type(key).__name__}"
                )

            if key in result:
                raise _InterpreterError(f"Duplicate hash table key: {key}")

            result[key] = value

        return HashTable(result)
