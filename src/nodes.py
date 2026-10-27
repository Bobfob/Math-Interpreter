from dataclasses import dataclass
from abc         import abstractmethod


### BASES


@dataclass
class ExprBase:
    @abstractmethod
    def __str__(self) -> str: ...
    __repr__ = __str__


### EXPRESSIONS


@dataclass
class ModuleExpr(ExprBase): # |E|
    expr: ExprBase

    def __str__(self) -> str:
        return f"|{self.expr}|"


@dataclass
class DeleteExpr(ExprBase): # del E
    ident: str
    
    def __str__(self) -> str:
        return f"del {self.ident}"


@dataclass
class FuncDeclaration(ExprBase): # E(...) = E
    name: str
    params: list[ExprBase]
    expr: ExprBase
    
    def __str__(self) -> str:
        return f"{self.name}({', '.join(map(str, self.params))}) = {self.expr}"


@dataclass
class AssignmentExpr(ExprBase): # E = E
    assign_to: ExprBase
    expr: ExprBase
    
    def __str__(self) -> str:
        return f"{self.assign_to} = {self.expr}"


@dataclass
class PlusNode(ExprBase): # E + E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self) -> str:
        return f"({self.lhs} + {self.rhs})"


@dataclass
class MinusNode(ExprBase): # E - E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str:
        return f"({self.lhs} - {self.rhs})"


@dataclass
class MulNode(ExprBase): # E * E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self) -> str:
        return f"({self.lhs} * {self.rhs})"


@dataclass
class PowerNode(ExprBase): # E ** E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self) -> str:
        return f"({self.lhs} ** {self.rhs})"


@dataclass
class DivNode(ExprBase): # E / E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self) -> str:
        return f"({self.lhs} / {self.rhs})"


@dataclass
class ModNode(ExprBase): # E % E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self) -> str:
        return f"({self.lhs} % {self.rhs})"


@dataclass
class BitwiseAndNode(ExprBase): # E & E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self) -> str:
        return f"({self.lhs} & {self.rhs})"


@dataclass
class BitwiseOrNode(ExprBase): # E | E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self) -> str:
        return f"({self.lhs} | {self.rhs})"


@dataclass
class BitwiseXorNode(ExprBase): # E ^ E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str:
        return f"({self.lhs} ^ {self.rhs})"


@dataclass
class NumberNode(ExprBase): # P
    value: int | float

    def __str__(self) -> str:
        return f"{self.value}"

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class IdentNode(ExprBase): # P
    ident: str
    
    def __str__(self) -> str:
        return f"{self.ident}"

    def __hash__(self) -> int:
        return hash(self.ident)


@dataclass
class Point2DNode(ExprBase): # P
    value: tuple[ExprBase, ExprBase]
    
    def __str__(self) -> str:
        return f"{self.value}"

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class Point3DNode(ExprBase): # P
    value: tuple[ExprBase, ExprBase, ExprBase]
    
    def __str__(self) -> str:
        return f"{self.value}"

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class UnaryPlusNode(ExprBase): # +E
    value: ExprBase

    def __str__(self) -> str:
        return f"+{self.value}"


@dataclass
class UnaryMinusNode(ExprBase): # -E
    value: ExprBase

    def __str__(self) -> str:
        return f"-{self.value}"


@dataclass
class FactorialNode(ExprBase): # E!
    value: ExprBase
    
    def __str__(self) -> str:
        return f"{self.value}!"


@dataclass
class FunctionCall(ExprBase): # E(...)
    name: str
    args: list[ExprBase]

    def __str__(self) -> str:
        return f"{self.name}({', '.join(map(str, self.args))})"


@dataclass
class GTNode(ExprBase): # E > E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str:
        return f"({self.lhs} > {self.rhs})"


@dataclass
class GTENode(ExprBase): # E >= E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str:
        return f"({self.lhs} >= {self.rhs})"


@dataclass
class LTNode(ExprBase): # E < E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str:
        return f"({self.lhs} < {self.rhs})"


@dataclass
class LTENode(ExprBase): # E <= E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str:
        return f"({self.lhs} <= {self.rhs})"


@dataclass
class EQNode(ExprBase): # E == E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str:
        return f"({self.lhs} == {self.rhs})"


@dataclass
class NEQNode(ExprBase): # E != E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str:
        return f"({self.lhs} != {self.rhs})"


@dataclass
class IndexNode(ExprBase): # E[E]
    parent: ExprBase
    value: ExprBase
    
    def __str__(self) -> str:
        return f"{self.parent}[{self.value}]"


@dataclass
class TernaryOpNode(ExprBase): # (E) ? E : E
    test_expr: ExprBase
    success_expr: ExprBase
    failed_expr: ExprBase
    
    def __str__(self) -> str:
        return f"({self.test_expr}) ? {self.success_expr} : {self.failed_expr}"


@dataclass
class AccessNode(ExprBase): # P::P
    parent: ExprBase
    child: ExprBase

    def __str__(self) -> str:
        return f"{self.parent}::{self.child}"


@dataclass
class ArrayNode(ExprBase): # [E, ...]
    value: list[ExprBase]

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass
class HashTableFieldNode(ExprBase): # P: E
    key: ExprBase
    value: ExprBase

    def __str__(self) -> str:
        return f"{self.key}: {self.value}"


@dataclass
class HashTableNode(ExprBase): # {P: E, ...}
    value: list[HashTableFieldNode]

    def __str__(self) -> str:
        return f"\x7B{", ".join(map(str, self.value))}\x7D"


@dataclass
class StringNode(ExprBase):  # P
    value: str

    def __str__(self) -> str:
        return repr(self.value)
    
    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class BoolNode(ExprBase):  # P
    value: bool

    def __str__(self) -> str:
        return "true" if self.value else "false"

    def __hash__(self) -> int:
        return hash(self.value)
