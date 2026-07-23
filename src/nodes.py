from dataclasses import dataclass

### BASES


@dataclass
class ExprBase: ...


### EXPRESSIONS


@dataclass
class ModuleExpr(ExprBase): # |E|
    expr: ExprBase
    
    def __str__(self) -> str: return f"|{self.expr}|"
    __repr__ = __str__


@dataclass
class DeleteExpr(ExprBase): # del E
    ident: str
    
    def __str__(self) -> str: return f"del {self.ident}"
    __repr__ = __str__


@dataclass
class FuncDeclaration(ExprBase): # E(...) = E
    name: str
    params: list[ExprBase]
    expr: ExprBase
    
    def __str__(self) -> str: return f"{self.name}({', '.join(map(str, self.params))}) = {self.expr}"
    __repr__ = __str__


@dataclass
class AssignmentExpr(ExprBase): # P = E
    assign_to: str
    expr: ExprBase
    
    def __str__(self) -> str: return f"{self.assign_to} = {self.expr}"
    __repr__ = __str__


@dataclass
class PlusNode(ExprBase): # E + E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} + {self.rhs})"
    __repr__ = __str__


@dataclass
class MinusNode(ExprBase): # E - E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self): return f"({self.lhs} - {self.rhs})"
    __repr__ = __str__


@dataclass
class MulNode(ExprBase): # E * E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} * {self.rhs})"
    __repr__ = __str__


@dataclass
class PowerNode(ExprBase): # E ** E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} ** {self.rhs})"
    __repr__ = __str__


@dataclass
class DivNode(ExprBase): # E / E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} / {self.rhs})"
    __repr__ = __str__


@dataclass
class ModNode(ExprBase): # E % E
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} % {self.rhs})"
    __repr__ = __str__


@dataclass
class NumberNode(ExprBase): # P
    value: int | float

    def __str__(self): return f"{self.value}"
    __repr__ = __str__


@dataclass
class IdentNode(ExprBase): # P
    ident: str
    
    def __str__(self) -> str: return f"{self.ident}"
    __repr__ = __str__


@dataclass
class Point2DNode(ExprBase): # P
    value: tuple[ExprBase, ExprBase]
    
    def __str__(self) -> str: return f"{self.value}"
    __repr__ = __str__


@dataclass
class Point3DNode(ExprBase): # P
    value: tuple[ExprBase, ExprBase, ExprBase]
    
    def __str__(self) -> str: return f"{self.value}"
    __repr__ = __str__


@dataclass
class UnaryPlusNode(ExprBase): # +E
    value: ExprBase

    def __str__(self): return f"+{self.value}"
    __repr__ = __str__


@dataclass
class UnaryMinusNode(ExprBase): # -E
    value: ExprBase

    def __str__(self): return f"-{self.value}"
    __repr__ = __str__


@dataclass
class FactorialNode(ExprBase): # E!
    value: ExprBase
    
    def __str__(self) -> str: return f"{self.value}!"
    __repr__ = __str__


@dataclass
class FunctionCall(ExprBase): # E(...)
    name: str
    args: list[ExprBase]

    def __str__(self): return f"{self.name}({', '.join(map(str, self.args))})"
    __repr__ = __str__


@dataclass
class GTNode(ExprBase): # E > E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str: return f"({self.lhs} > {self.rhs})"
    __repr__ = __str__


@dataclass
class GTENode(ExprBase): # E >= E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str: return f"({self.lhs} >= {self.rhs})"
    __repr__ = __str__


@dataclass
class LTNode(ExprBase): # E < E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str: return f"({self.lhs} < {self.rhs})"
    __repr__ = __str__


@dataclass
class LTENode(ExprBase): # E <= E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str: return f"({self.lhs} <= {self.rhs})"
    __repr__ = __str__


@dataclass
class EQNode(ExprBase): # E == E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str: return f"({self.lhs} == {self.rhs})"
    __repr__ = __str__


@dataclass
class NEQNode(ExprBase): # E != E
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self) -> str: return f"({self.lhs} != {self.rhs})"
    __repr__ = __str__


@dataclass
class IndexNode(ExprBase): # E[E]
    parent: ExprBase
    value: ExprBase
    
    
    def __str__(self) -> str: return f"{self.parent}[{self.value}]"
    __repr__ = __str__


@dataclass
class TernaryOpNode(ExprBase): # (E) ? E : E
    test_expr: ExprBase
    success_expr: ExprBase
    failed_expr: ExprBase
    
    
    def __str__(self) -> str: return f"({self.test_expr}) ? {self.success_expr} : {self.failed_expr}"
    __repr__ = __str__


# Interpreter datatypes


@dataclass
class Point2D:
    x: float
    y: float
    
    
    def __str__(self) -> str: return f"({self.x}, {self.y})"
    __repr__ = __str__
    
    
    def __getitem__(self, key: int) -> float:
        return [self.x, self.y][key]
    
    
    def __abs__(self) -> Point2D:
        return Point2D(abs(self.x), abs(self.y))
    
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Point2D):
            raise TypeError("Expected Point2D")
        
        return self.x == value.x and self.y == value.y
    
    
    def __neq__(self, value: object) -> bool:
        return not (self == value)
    
    
    def __lt__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            raise TypeError("Expected Point2D")
        
        return self.x < other.x and self.y < other.y
    
    
    def __le__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            raise TypeError("Expected Point2D")
        
        return self.x <= other.x and self.y <= other.y
    
    
    def __gt__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            raise TypeError("Expected Point2D")
        
        return self.x > other.x and self.y > other.y
    
    
    def __ge__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            raise TypeError("Expected Point2D")
        
        return self.x >= other.x and self.y >= other.y
    
    
    def __neg__(self) -> Point2D:
        return Point2D(-self.x, -self.y)
    
    
    def __add__(self, other: Point2D) -> Point2D:
        if not isinstance(other, Point2D):
            raise TypeError("Expected Point2D")
        
        return Point2D(self.x + other.x, self.y + other.y)
    
    
    def __radd__(self, other: Point2D) -> Point2D:
        return self.__add__(other)
    
    
    def __sub__(self, other: Point2D) -> Point2D:
        if not isinstance(other, Point2D):
            raise TypeError("Expected Point2D")
        
        return Point2D(self.x - other.x, self.y - other.y)
    
    
    def __rsub__(self, other: Point2D) -> Point2D:
        return self.__sub__(other)
    
    
    def __mul__(self, other: int | float) -> Point2D:
        if not isinstance(other, (int, float)):
            raise TypeError("Expected int or float")
        
        return Point2D(self.x * other, self.y * other)
    
    
    def __rmul__(self, other: int | float) -> Point2D:
        return self.__mul__(other)
    
    
    def __truediv__(self, other: int | float) -> Point2D:
        if not isinstance(other, (int, float)):
            raise TypeError("Expected int or float")
        
        return Point2D(self.x / other, self.y / other)
    
    
    def __pow__(self, other: int | float) -> Point2D:
        if not isinstance(other, (int, float)):
            raise TypeError("Expected int or float")
        
        return Point2D(self.x ** other, self.y ** other)


@dataclass
class Point3D:
    x: float
    y: float
    z: float
    
    
    def __str__(self) -> str: return f"({self.x}, {self.y}, {self.z})"
    __repr__ = __str__
    
    
    def __getitem__(self, key: int) -> float:
        return [self.x, self.y, self.z][key]
    
    
    def __abs__(self) -> Point3D:
        return Point3D(abs(self.x), abs(self.y), abs(self.z))
    
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Point3D):
            raise TypeError("Expected Point3D")
        
        return self.x == value.x and self.y == value.y
    
    
    def __neq__(self, value: object) -> bool:
        return not (self == value)
    
    
    def __lt__(self, other: Point3D) -> bool:
        if not isinstance(other, Point3D):
            raise TypeError("Expected Point3D")
        
        return self.x < other.x and self.y < other.y and self.z < other.z
    
    
    def __le__(self, other: Point3D) -> bool:
        if not isinstance(other, Point3D):
            raise TypeError("Expected Point3D")
        
        return self.x <= other.x and self.y <= other.y and self.z <= other.z
    
    
    def __gt__(self, other: Point3D) -> bool:
        if not isinstance(other, Point3D):
            raise TypeError("Expected Point3D")
        
        return self.x > other.x and self.y > other.y and self.z > other.z
    
    
    def __ge__(self, other: Point3D) -> bool:
        if not isinstance(other, Point3D):
            raise TypeError("Expected Point3D")
        
        return self.x >= other.x and self.y >= other.y and self.z >= other.z
    
    
    def __neg__(self) -> Point3D:
        return Point3D(-self.x, -self.y, -self.z)
    
    
    def __add__(self, other: Point3D) -> Point3D:
        if not isinstance(other, Point3D):
            raise TypeError("Expected Point3D")
        
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    
    def __radd__(self, other: Point3D) -> Point3D:
        return self.__add__(other)
    
    
    def __sub__(self, other: Point3D) -> Point3D:
        if not isinstance(other, Point3D):
            raise TypeError("Expected Point3D")
        
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    
    def __rsub__(self, other: Point3D) -> Point3D:
        return self.__sub__(other)
    
    
    def __mul__(self, other: int | float) -> Point3D:
        if not isinstance(other, (int, float)):
            raise TypeError("Expected int or float")
        
        return Point3D(self.x * other, self.y * other, self.z * other)
    
    
    def __rmul__(self, other: int | float) -> Point3D:
        return self.__mul__(other)
    
    
    def __truediv__(self, other: int | float) -> Point3D:
        if not isinstance(other, (int, float)):
            raise TypeError("Expected int or float")
        
        return Point3D(self.x / other, self.y / other, self.z / other)
    
    
    def __pow__(self, other: int | float) -> Point3D:
        if not isinstance(other, (int, float)):
            raise TypeError("Expected int or float")
        
        return Point3D(self.x ** other, self.y ** other, self.z ** other)
