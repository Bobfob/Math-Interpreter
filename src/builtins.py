import math
import inspect


class ReservedFunctions:
    @staticmethod
    def cos(x): return math.cos(x)
    @staticmethod
    def sin(x): return math.sin(x)
    @staticmethod
    def tan(x): return math.tan(x)
    @staticmethod
    def cot(x): return 1 / math.tan(x)
    @staticmethod
    def sec(x): return 1 / math.cos(x)
    @staticmethod
    def csc(x): return 1 / math.sin(x)
    @staticmethod
    def ln(x): return math.log(x)
    @staticmethod
    def log(x): return math.log10(x)
    @staticmethod
    def logn(x, base): return math.log(x, base)
    @staticmethod
    def exp(x): return math.exp(x)
    @staticmethod
    def sqrt(x): return math.sqrt(x)
    @staticmethod
    def cbrt(x): return math.cbrt(x)
    @staticmethod
    def abs(x): return abs(x)
    @staticmethod
    def ceil(x): return math.ceil(x)
    @staticmethod
    def floor(x): return math.floor(x)
    @staticmethod
    def cosh(x): return math.cosh(x)
    @staticmethod
    def sinh(x): return math.sinh(x)
    @staticmethod
    def tanh(x): return math.tanh(x)
    @staticmethod
    def coth(x): return 1 / math.tanh(x)
    @staticmethod
    def sech(x): return 1 / math.cosh(x)
    @staticmethod
    def csch(x): return 1 / math.sinh(x)
    @staticmethod
    def cos_d(x): return math.cos(math.radians(x))
    @staticmethod
    def sin_d(x): return math.sin(math.radians(x))
    @staticmethod
    def tan_d(x): return math.tan(math.radians(x))
    @staticmethod
    def cot_d(x): return 1 / math.tan(math.radians(x))
    @staticmethod
    def sec_d(x): return 1 / math.cos(math.radians(x))
    @staticmethod
    def csc_d(x): return 1 / math.sin(math.radians(x))
    @staticmethod
    def clamp(x, min_x, max_x): return min(max(x, min_x), max_x)
    @staticmethod
    def min(x, y, *args): return min(x, y, *args)
    @staticmethod
    def max(x, y, *args): return max(x, y, *args)
    @staticmethod
    def asin(x): return math.asin(x)
    @staticmethod
    def acos(x): return math.acos(x)
    @staticmethod
    def atan(x): return math.atan(x)
    @staticmethod
    def atan2(y, x): return math.atan2(y, x)
    @staticmethod
    def asinh(x): return math.asinh(x)
    @staticmethod
    def acosh(x): return math.acosh(x)
    @staticmethod
    def atanh(x): return math.atanh(x)
    @staticmethod
    def copysign(x, y): return math.copysign(x, y)
    @staticmethod
    def degrees(x): return math.degrees(float(x))
    @staticmethod
    def radians(x): return math.radians(float(x))
    @staticmethod
    def fabs(x): return math.fabs(x)
    @staticmethod
    def lcm(*args): return math.lcm(*map(int, args))
    @staticmethod
    def gcd(*args): return math.gcd(*map(int, args))
    @staticmethod
    def perm(n, k): return math.perm(int(n), int(k))


def factorial(n: int) -> int:
    if not isinstance(n, int): raise TypeError(f'Expected type \'int\', but got \'{type(n).__name__}\'')
    elif n < 0: raise ValueError("Expected n >= 0")
    elif n == 0: return 1
    else: return factorial(n - 1) * n


RESERVED_FUNCTIONS_NAMES = tuple(
    name for name, _
        in inspect.getmembers(ReservedFunctions, predicate=inspect.isfunction)
)
