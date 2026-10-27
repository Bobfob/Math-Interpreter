import math

from typing      import Any
from dataclasses import dataclass
from abc         import abstractmethod


def _as_number(x) -> Number:
    if isinstance(x, Number):
        return x
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return Number(x)
    raise TypeError("Expected Number, int or float")


class BaseDatatype:
    @abstractmethod
    def __str__(self) -> str: ...


    def __repr__(self) -> str:
        return self.__str__()


    @abstractmethod
    def get_property(self, name: str) -> Any: ...


    @abstractmethod
    def set_property(self, name: str, value: Any) -> None: ...


    @abstractmethod
    def call_method(self, name: str, args: list[Any]) -> Any: ...


@dataclass(repr=False)
class Number(BaseDatatype):
    value: float

    def __str__(self):
        return f"{self.value}"

    def __float__(self) -> float:
        return float(self.value)

    def __int__(self) -> int:
        return int(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __index__(self) -> int:
        return int(self.value)

    def __add__(self, other: Number) -> Number:
        other = _as_number(other)
        return Number(self.value + other.value)

    def __radd__(self, other: Number) -> Number:
        return self.__add__(other)

    def __iadd__(self, other: Number) -> Number:
        other = _as_number(other)
        self.value += other.value
        return self

    def __sub__(self, other: Number) -> Number:
        other = _as_number(other)
        return Number(self.value - other.value)

    def __rsub__(self, other: Number) -> Number:
        other = _as_number(other)
        return Number(other.value - self.value)

    def __isub__(self, other: Number) -> Number:
        other = _as_number(other)
        self.value -= other.value
        return self

    def __mul__(self, other) -> Number:
        other = _as_number(other)
        return Number(self.value * other.value)

    def __rmul__(self, other) -> Number:
        other = _as_number(other)
        return Number(self.value * other.value)

    def __imul__(self, other: Number) -> Number:
        other = _as_number(other)
        self.value *= other.value
        return self

    def __truediv__(self, other: Number) -> Number:
        other = _as_number(other)
        return Number(self.value / other.value)

    def __rtruediv__(self, other: Number) -> Number:
        other = _as_number(other)
        return Number(other.value / self.value)

    def __itruediv__(self, other: Number) -> Number:
        other = _as_number(other)
        self.value /= other.value
        return self

    def __floordiv__(self, other: Number) -> Number:
        other = _as_number(other)
        return Number(self.value // other.value)

    def __rfloordiv__(self, other: Number) -> Number:
        other = _as_number(other)
        return Number(other.value // self.value)

    def __ifloordiv__(self, other: Number) -> Number:
        other = _as_number(other)
        self.value //= other.value
        return self

    def __mod__(self, other) -> Number:
        other = _as_number(other)
        return Number(self.value % other.value)

    def __rmod__(self, other) -> Number:
        other = _as_number(other)
        return Number(other.value % self.value)

    def __imod__(self, other: Number) -> Number:
        other = _as_number(other)
        self.value %= other.value
        return self

    def __pow__(self, other) -> Number:
        other = _as_number(other)
        return Number(self.value ** other.value)

    def __rpow__(self, other) -> Number:
        other = _as_number(other)
        return Number(other.value ** self.value)

    def __ipow__(self, other: Number) -> Number:
        other = _as_number(other)
        self.value **= other.value
        return self

    def __neg__(self) -> Number:
        return Number(-self.value)

    def __pos__(self) -> Number:
        return Number(+self.value)

    def __abs__(self) -> Number:
        return Number(abs(self.value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return self.value != other.value

    def __lt__(self, other: Number) -> bool:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return self.value < other.value

    def __le__(self, other: Number) -> bool:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return self.value <= other.value

    def __gt__(self, other: Number) -> bool:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return self.value > other.value

    def __ge__(self, other: Number) -> bool:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return self.value >= other.value
    
    def __and__(self, other: Number) -> Number:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return Number(int(self.value) & int(other.value))

    def __rand__(self, other: Number) -> Number:
        return self.__and__(other)

    def __or__(self, other: Number) -> Number:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return Number(int(self.value) | int(other.value))

    def __ror__(self, other: Number) -> Number:
        return self.__or__(other)
    
    def __xor__(self, other: Number) -> Number:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return Number(int(self.value) ^ int(other.value))
    
    def __rxor__(self, other: Number) -> Number:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return Number(int(other.value) ^ int(self.value))

    def __hash__(self) -> int:
        return hash(self.value)

    def __format__(self, format_spec) -> str:
        return format(self.value, format_spec)

    def __round__(self, ndigits=None) -> Number:
        return Number(round(self.value, ndigits))

    def __floor__(self) -> Number:
        return Number(math.floor(self.value))

    def __ceil__(self) -> Number:
        return Number(math.ceil(self.value))

    def get_property(self, name: str) -> Any:
        raise AttributeError(f"{type(self).__name__} has no property named: {name}")

    def set_property(self, name: str, value: Any) -> None:
        raise AttributeError(f"{type(self).__name__} has no settable property named: {name}")

    def call_method(self, name: str, args: list[Any]) -> Any:
        match name:
            case "as_ratio":
                if len(args) != 0:
                    raise TypeError(f"as_ratio takes 0 positional arguments, but got {len(args)}")
                r = self.value.as_integer_ratio()
                return Point2D(Number(r[0]), Number(r[1]))
            case _:
                raise AttributeError(f"{type(self).__name__} has no method with name: {name}")


@dataclass(repr=False)
class Point2D(BaseDatatype):
    x: Number
    y: Number

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __getitem__(self, key: int) -> Number:
        return (self.x, self.y)[key]

    def __setitem__(self, key, value):
        match key.value:
            case 0: self.x = value
            case 1: self.y = value
            case _: raise AttributeError("Unexpected key to assign")

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

    def __mul__(self, other) -> Point2D:
        other = _as_number(other)
        return Point2D(self.x * other, self.y * other)

    def __rmul__(self, other) -> Point2D:
        return self.__mul__(other)

    def __truediv__(self, other) -> Point2D:
        other = _as_number(other)
        return Point2D(self.x / other, self.y / other)

    def __pow__(self, other) -> Point2D:
        other = _as_number(other)
        return Point2D(self.x ** other, self.y ** other)

    def get_property(self, name: str) -> Any:
        match name:
            case 'x': return self.x
            case 'y': return self.y
            case "length": return (self.x*self.x + self.y*self.y) ** 0.5
            
            case "angle":
                length = (self.x*self.x + self.y*self.y) ** 0.5
                if float(length) <= 1e-14:
                    return Point2D(Number(0), Number(0))
                normalized = self / length
                
                return Number(math.atan2(normalized.y, normalized.x))
            
            case "normalized":
                length = (self.x*self.x + self.y*self.y) ** 0.5
                if float(length) <= 1e-14:
                    return Point2D(Number(0), Number(0))
                return self / length
            
            case _:
                raise AttributeError(f"{type(self).__name__} has no property named: {name}")

    def set_property(self, name: str, value: Any) -> None:
        if not isinstance(value, Number):
            raise TypeError("Expected datatype Number")
        match name:
            case 'x': self.x = value
            case 'y': self.y = value
            case _:
                raise AttributeError(f"{type(self).__name__} has no settable property named: {name}")

    def call_method(self, name: str, args: list[Any]) -> Any:
        def _check_arity(expected: int) -> None:
            if len(args) != expected:
                raise TypeError(
                    f"{name} takes {expected} positional argument(s), but got {len(args)}"
                )
        
        def _is_type(arg: Any, _type) -> None:
            if not isinstance(arg, _type):
                raise TypeError(f"argument must be {type(_type).__name__}")
            return arg
        
        match name:
            case "dot":
                _check_arity(1)
                other = _is_type(args[0], Point2D)
                return self.x * other.x + self.y * other.y

            case "cross":
                _check_arity(1)
                other = _is_type(args[0], Point2D)
                return self.x * other.y - self.y * other.x

            case "dist":
                _check_arity(1)
                d = _is_type(args[0], Point2D) - self
                return (d.x*d.x + d.y*d.y) ** 0.5

            case _:
                raise AttributeError(f"{type(self).__name__} has no method with name: {name}")


@dataclass(repr=False)
class Point3D(BaseDatatype):
    x: Number
    y: Number
    z: Number

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __getitem__(self, key: int) -> Number:
        return (self.x, self.y, self.z)[key]

    def __setitem__(self, key, value):
        match key.value:
            case 0: self.x = value
            case 1: self.y = value
            case 2: self.z = value
            case _: raise AttributeError("Unexpected key to assign")

    def __abs__(self) -> Point3D:
        return Point3D(abs(self.x), abs(self.y), abs(self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Point3D):
            raise TypeError("Expected Point3D")
        return self.x == value.x and self.y == value.y and self.z == value.z

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

    def __mul__(self, other) -> Point3D:
        other = _as_number(other)
        return Point3D(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other) -> Point3D:
        return self.__mul__(other)

    def __truediv__(self, other) -> Point3D:
        other = _as_number(other)
        return Point3D(self.x / other, self.y / other, self.z / other)

    def __pow__(self, other) -> Point3D:
        other = _as_number(other)
        return Point3D(self.x ** other, self.y ** other, self.z ** other)

    def get_property(self, name: str) -> Any:
        match name:
            case 'x': return self.x
            case 'y': return self.y
            case 'z': return self.z
            case "length": return (self.x*self.x + self.y*self.y + self.z*self.z) ** 0.5
            
            case "normalized":
                length = (self.x*self.x + self.y*self.y + self.z*self.z) ** 0.5
                if float(length) <= 1e-14:
                    return Point3D(Number(0), Number(0), Number(0))
                return self / length
            
            case _:
                raise AttributeError(f"{type(self).__name__} has no property named: {name}")

    def set_property(self, name: str, value: Any) -> None:
        if not isinstance(value, Number):
            raise TypeError("Expected datatype Number")
        match name:
            case 'x': self.x = value
            case 'y': self.y = value
            case 'z': self.z = value
            case _:
                raise AttributeError(f"{type(self).__name__} has no settable property named: {name}")

    def call_method(self, name: str, args: list[Any]) -> Any:
        def _check_arity(expected: int) -> None:
            if len(args) != expected:
                raise TypeError(
                    f"{name} takes {expected} positional argument(s), but got {len(args)}"
                )
        
        def _is_type(arg: Any, _type) -> None:
            if not isinstance(arg, _type):
                raise TypeError(f"argument must be {type(_type).__name__}")
            return arg
        
        match name:
            case "dot":
                _check_arity(1)
                other = _is_type(args[0], Point3D)
                return self.x * other.x + self.y * other.y + self.z * other.z
            
            case "cross":
                _check_arity(1)
                other = _is_type(args[0], Point3D)
                return Point3D(
                    self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x
                )

            case "dist":
                _check_arity(1)
                d = _is_type(args[0], Point3D) - self
                return (d.x*d.x + d.y*d.y + d.z*d.z) ** 0.5
            
            case "lerp":
                _check_arity(2)
                other, t = _is_type(args[0], Point3D), _is_type(args[1], Number)
                return Point3D(
                    self.x + (other.x - self.x) * t,
                    self.y + (other.y - self.y) * t,
                    self.z + (other.z - self.z) * t
                )

            case _:
                raise AttributeError(f"{type(self).__name__} has no method with name: {name}")


@dataclass(repr=False)
class Array(BaseDatatype):
    value: list[BaseDatatype]

    def __str__(self) -> str:
        return f"[{', '.join(map(repr, self.value))}]"

    def __add__(self, other: Array) -> Array:
        if not isinstance(other, Array):
            raise TypeError("Expected datatype Array")
        return self._join(other)

    def __getitem__(self, key: Number) -> BaseDatatype:
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def _join(self, other: Array) -> Array:
        new_list = list(self.value)
        new_list.extend(other.value)
        return Array(new_list)

    def get_property(self, name: str) -> Any:
        match name:
            case "length": return Number(len(self.value))
            case _:
                raise AttributeError(f"{type(self).__name__} has no property named: {name}")

    def set_property(self, name: str, value: Any) -> None:
        raise AttributeError(f"{type(self).__name__} has no settable property named: {name}")

    def call_method(self, name: str, args: list[Any]) -> Any:
        def _check_arity(expected: int) -> None:
            if len(args) != expected:
                raise TypeError(
                    f"{name} takes {expected} positional argument(s), but got {len(args)}"
                )
        
        def _is_type(arg: Any, _type) -> None:
            if not isinstance(arg, _type):
                raise TypeError(f"argument must be {type(_type).__name__}")
            return arg
        
        match name:
            case "add":
                _check_arity(1)
                self.value.append(args[0])

            case "extend":
                _check_arity(1)
                arg = _is_type(args[0], Array)
                self.value.extend(arg.value)

            case "pop":
                _check_arity(0)
                return self.value.pop()

            case _:
                raise AttributeError(f"{type(self).__name__} has no method with name: {name}")


@dataclass(repr=False)
class String(BaseDatatype):
    value: str

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        escaped = (
            self.value
            .replace('\\', '\\\\')
            .replace('"', '\\"')
            .replace('\n', '\\n')
            .replace('\t', '\\t')
            .replace('\r', '\\r')
        )

        return f'"{escaped}"'

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, String):
            raise TypeError("Expected datatype String")
        return self.value == other.value

    def __ne__(self, other) -> bool:
        if not isinstance(other, String):
            raise TypeError("Expected datatype String")
        return self.value != other.value

    def __lt__(self, other) -> bool:
        if not isinstance(other, String):
            raise TypeError("Expected datatype String")
        return self.value < other.value

    def __le__(self, other) -> bool:
        if not isinstance(other, String):
            raise TypeError("Expected datatype String")
        return self.value <= other.value

    def __gt__(self, other) -> bool:
        if not isinstance(other, String):
            raise TypeError("Expected datatype String")
        return self.value > other.value

    def __ge__(self, other) -> bool:
        if not isinstance(other, String):
            raise TypeError("Expected datatype String")
        return self.value >= other.value

    def __add__(self, other: String) -> String:
        if not isinstance(other, String):
            raise TypeError("Expected datatype String")
        return String(self.value + other.value)

    def __radd__(self, other: String) -> String:
        return self.__add__(other)

    def __mul__(self, other) -> String:
        if not isinstance(other, Number):
            raise TypeError("Expected datatype Number")
        return String(self.value * int(other))

    def __rmul__(self, other) -> String:
        return self.__mul__(other)

    def __getitem__(self, key) -> String:
        if not isinstance(key, Number):
            raise TypeError("Expected datatype Number")
        try:
            return String(self.value[int(key)])
        except IndexError:
            raise IndexError(f"String index out of range: {int(key)}")

    def __len__(self) -> int:
        return len(self.value)

    def get_property(self, name: str) -> Any:
        match name:
            case "length": return Number(len(self.value))
            case _:
                raise AttributeError(f"{type(self).__name__} has no property named: {name}")

    def set_property(self, name: str, value: Any) -> None:
        raise AttributeError(
            f"{type(self).__name__} is immutable and has no settable property named: {name}"
        )

    def call_method(self, name: str, args: list[Any]) -> Any:
        def _check_arity(expected: int) -> None:
            if len(args) != expected:
                raise TypeError(
                    f"{name} takes {expected} positional argument(s), but got {len(args)}"
                )

        def _as_string(arg: Any) -> str:
            if not isinstance(arg, String):
                raise TypeError("argument must be String")
            return arg.value

        match name:
            case "upper":
                _check_arity(0)
                return String(self.value.upper())

            case "lower":
                _check_arity(0)
                return String(self.value.lower())

            case "strip":
                _check_arity(0)
                return String(self.value.strip())

            case "split":
                if len(args) > 1:
                    raise TypeError(f"split takes 0 or 1 positional argument(s), but got {len(args)}")
                sep = None if not args else _as_string(args[0])
                if sep == "":
                    raise ValueError("split separator must not be empty")
                return Array([String(p) for p in self.value.split(sep)])

            case "replace":
                _check_arity(2)
                return String(self.value.replace(_as_string(args[0]), _as_string(args[1])))

            case "find":
                _check_arity(1)
                return Number(self.value.find(_as_string(args[0])))

            case "contains":
                _check_arity(1)
                return Number(1 if _as_string(args[0]) in self.value else 0)

            case "starts_with":
                _check_arity(1)
                return Number(1 if self.value.startswith(_as_string(args[0])) else 0)

            case "ends_with":
                _check_arity(1)
                return Number(1 if self.value.endswith(_as_string(args[0])) else 0)

            case "chars":
                _check_arity(0)
                return Array([String(c) for c in self.value])

            case "to_number":
                _check_arity(0)
                try:
                    return Number(float(self.value))
                except ValueError:
                    raise ValueError(f"Cannot convert '{self.value}' to Number")

            case _:
                raise AttributeError(f"{type(self).__name__} has no method with name: {name}")


@dataclass(repr=False)
class Boolean(BaseDatatype):
    value: bool

    def __str__(self) -> str:
        return "true" if self.value else "false"

    def __repr__(self) -> str:
        return str(self)

    def __bool__(self) -> bool:
        return self.value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Boolean):
            raise TypeError("Expected datatype Boolean")
        return self.value == other.value

    def __ne__(self, other) -> bool:
        if not isinstance(other, Boolean):
            raise TypeError("Expected datatype Boolean")
        return self.value != other.value

    def __and__(self, other: Boolean) -> Boolean:
        if not isinstance(other, Boolean):
            raise TypeError("Expected datatype Boolean")
        return Boolean(self.value and other.value)

    def __rand__(self, other: Boolean) -> Boolean:
        return self.__and__(other)

    def __or__(self, other: Boolean) -> Boolean:
        if not isinstance(other, Boolean):
            raise TypeError("Expected datatype Boolean")
        return Boolean(self.value or other.value)

    def __ror__(self, other: Boolean) -> Boolean:
        return self.__or__(other)

    def get_property(self, name: str) -> Any:
        raise AttributeError(f"{type(self).__name__} has no property named: {name}")

    def set_property(self, name: str, value: Any) -> None:
        raise AttributeError(f"{type(self).__name__} has no settable property named: {name}")

    def call_method(self, name: str, args: list[Any]) -> Any:
        raise AttributeError(f"{type(self).__name__} has no method with name: {name}")


HASHABLE_KEY_TYPES = (Number, Point2D, Point3D, String, Boolean)


@dataclass
class HashTable(BaseDatatype):
    value: dict[BaseDatatype, BaseDatatype]

    def __str__(self) -> str:
        return "{" + ", ".join(f"{repr(k)}: {repr(v)}" for k, v in self.value.items()) + "}"

    def __getitem__(self, key: BaseDatatype) -> BaseDatatype:
        if not isinstance(key, HASHABLE_KEY_TYPES):
            raise TypeError(f"Unsupported hash table key type: {type(key).__name__}")
        try:
            return self.value[key]
        except KeyError:
            raise KeyError(f"Key not found: {key}")

    def __setitem__(self, key: BaseDatatype, value: BaseDatatype) -> None:
        if not isinstance(key, HASHABLE_KEY_TYPES):
            raise TypeError(f"Unsupported hash table key type: {type(key).__name__}")
        self.value[key] = value

    def __contains__(self, key: BaseDatatype) -> bool:
        return key in self.value

    def __len__(self) -> int:
        return len(self.value)

    def get_property(self, name: str) -> Any:
        match name:
            case "length": return Number(len(self.value))
            case "keys":   return Array(list(self.value.keys()))
            case "values": return Array(list(self.value.values()))
            case _:
                raise AttributeError(f"{type(self).__name__} has no property named: {name}")

    def set_property(self, name: str, value: Any) -> None:
        raise AttributeError(f"{type(self).__name__} has no settable property named: {name}")

    def call_method(self, name: str, args: list[Any]) -> Any:
        def _check_arity(expected: int) -> None:
            if len(args) != expected:
                raise TypeError(
                    f"{name} takes {expected} positional argument(s), but got {len(args)}"
                )

        match name:
            case "has_key":
                _check_arity(1)
                return Boolean(True if args[0] in self.value else False)

            case "remove":
                _check_arity(1)
                if args[0] in self.value:
                    del self.value[args[0]]

            case "clear":
                _check_arity(0)
                self.value.clear()

            case _:
                raise AttributeError(f"{type(self).__name__} has no method with name: {name}")
