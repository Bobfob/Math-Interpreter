# Bobfob's Math Interpreter

## Purpose

This project was created just for fun and in order to complete the assignment in college. It is a custom interpreter for math expressions, inspired by the Desmos graphing calculator.

## Usage

To use this interpreter, you first need to copy this repository to folder that you opened in terminal. To do this, go to **powershell** or **bash** (or any other terminal) and enter the command:

``` bash
git clone "https://github.com/Bobfob/Math-Interpreter.git"
```

Next, after you have copied the repository, you need to run the file *main.py* using **Python 3.14** or higher and try to type some expressions into terminal.

## Features

1) Variables (as well constant variants)
2) Functions with local scoping
3) Data deletion
4) Ternary operator
5) Point2D and Point3D
6) Strings (with built-in methods)
7) Hash Tables (Dictionaries)
8) Boolean datatype (`true` / `false`) and logical operations
9) Attribute and Index assignment
10) Augmented assignments (`+=`, `-=`, `*=`, `/=`, `%=`, `**=`, `&=`, `|=`, `^=`)
11) Bitwise operators (`&`, `|`)
12) And others (all list you can see in help message, type *.help* while running)

## Examples

>Example №1:\
![example №1](images/image_example1.png)
\
\
Example №2:\
![example №2](images/image_example2.png)

## Supported (reserved) variables

1. **@pi**  - π variable
2. **@e**   - Euler value
3. **@tau** - 2π variable

## Supported (reserved) functions

1. **cos** - Calculates cosine with given radians
2. **sin** - Calculates sine with given radians
3. **tan** - Calculates tangent with given radians
4. **cot** - Calculates cotangent with given radians
5. **sec** - Calculates secant with given radians
6. **csc** - Calculates cosecant with given radians
7. **ln** - Calculates natural logarithm with given x
8. **log** - Calculates logarithm of base 10 with given x
9. **logn** - Calculates logarithm of base n with given x
10. **exp** - Calculates exponent with given x
11. **sqrt** - Calculates square root of given x
12. **cbrt** - Calculates cube root of given x
13. **abs** - Returns absolute value of given x
14. **floor** - Returns floored value of given x
15. **ceil** - Returns ceiled value of given x
16. **cosh** - Returns hyperbolic cosine with given x
17. **sinh** - Returns hyperbolic sine with given x
18. **tanh** - Returns hyperbolic tangent with given x
19. **coth** - Returns hyperbolic cotangent with given x
20. **sech** - Returns hyperbolic secant with given x
21. **csch** - Returns hyperbolic cosecant with given x
22. **cos_d** - Calculates cosine with given degrees
23. **sin_d** - Calculates sine with given degrees
24. **tan_d** - Calculates tangent with given degrees
25. **cot_d** - Calculates cotangent with given degrees
26. **sec_d** - Calculates secant with given degrees
27. **csc_d** - Calculates cosecant with given degrees
28. **clamp** - Returns clamped value with given value, minimal value and maximum value
29. **min** - Returns minimum value of given x, y, etc
30. **max** - Returns maximum value of given x, y, etc
31. **asin** - Returns arc sine with given value between -1 and 1
32. **acos** - Returns arc cosine with given value between -1 and 1
33. **atan** - Returns arc tangent with given x
34. **atan2** - Returns arc tangent with given values y and x (i.e. atan(y / x))
35. **asinh** - Returns arc hyperbolic sine with given x
36. **acosh** - Returns arc hyperbolic cosine with given x
37. **atanh** - Returns arc hyperbolic tangent with given x
38. **copysign** - Returns absolute value of x but with sign of y
39. **degrees** - Converts radians to degrees (x * 180 / π)
40. **radians** - Converts degrees to radians (x * π / 180)
41. **fabs** - Works exactly like abs, but always returns float value
42. **lcm** - Returns least common multiple
43. **gcd** - Returns greatest common divisor
44. **perm** - Returns number of permutations (n! / (n - k)!)

## Versions

## Patch 1.7.0.1 - Micro patch (current)

* Fixed skipped XOR augmented assign in parser

## Version 1.7 - Major update

### This release may have some bugs in it, feel free to write issues

* **Added Boolean Datatype:**
  * Introduced `true` and `false` literals.
  * All comparison operators (`>`, `<`, `==`, `!=`, `>=`, `<=`) now return a `Boolean` instead of a raw number/float/bool.
  * Boolean logic is supported using the `&` (AND) and `|` (OR) operators. For example: `true & false` results in `false`.
  * Booleans can be used as keys in Hash Tables.
* **Added Augmented Assignments:** You can now use `+=`, `-=`, `*=`, `/=`, `%=`, `**=`, `&=`, `|=`, `^=` operators. For example: `a = 5; a += 2` results in `a` becoming `7`.
* **Added Bitwise Operators:** Added `&` (bitwise AND), `|` (bitwise OR) and `^` (bitwise XOR) operators for Number datatype.
* **Fixed Local Scoping in Functions:** Variables assigned inside a function (e.g., `f(x) = (x = x + 1)`) now properly update the local frame instead of leaking to the global scope. Assignments are now allowed inside parentheses.
* **Improved Function Printing:** The `.funcs` and `.defines` commands now print functions in a clean, human-readable format (e.g., `f(x) = (x + 1)`) instead of raw AST object representations.
* **Added full support for Strings:**
  * String literals can be defined using single or double quotes: `"hello"`, `'world'`.
  * Escape sequences are supported: `\n`, `\t`, `\\`, `\"`, etc.
  * Concatenation via `+` operator.
  * Repetition via `*` operator (e.g., `"hi" * 3`).
  * Indexing to get a single character (e.g., `s[0]`).
  * Built-in string methods accessible via `::`: `upper`, `lower`, `strip`, `split`, `replace`, `find`, `contains`, `starts_with`, `ends_with`, `chars`, `to_number`.
* **Added Hash Tables (Dictionaries):**
  * Syntax: `{"key": "value", 1: 2, (3, 4): 5}`.
  * Keys can be Numbers, Strings, Point2D, Point3D, or Boolean.
  * Supported properties: `length`, `keys`, `values`.
  * Supported methods: `has_key`, `remove`, `clear`.
  * Indexing to read or write values: `h["key"] = 10`.
* **Scanner rewritten using Regular Expressions:** The scanner (`src/scanner.py`) was completely rewritten using Python's `re` module for faster and more robust tokenization.
* **Attribute Assignment:** You can now assign values to object properties directly. For example, `p::x = 5` updates the X coordinate of Point2D.
* **Fixed Data Types:** All mathematical functions now correctly return the internal `Number` datatype instead of raw Python floats. Reserved variables (`@pi`, `@e`, `@tau`) are now correctly wrapped in `Number`.
* **Added commands:** `.reload` | `.restart` for program restarting

## Version 1.2 - Minor update

* Added support for accessing some internal functions or fields in points (with **"::"** operator)
* Added some missed functions from math module: `asin`, `acos`, `atan`, `atan2`, `asinh`, `acosh`, `atanh`, `copysign`, `degrees`, `radians`, `fabs`, `lcm`, `gcd`, `perm`
* Reserved functions and factorial function has been transported to builtins module
* Added always_show_last_error flag for more information in errors
* Added last_error for showing last error

## Version 1.1 - Major update

* Added variables
* Added functions
* Added ternary operator
* Added Point2D and Point3D
* Added indexing support (currently only works on points)
* Added deletion operator
* Added help command

## Version 1.0 - Initial release

* Added basic arithmetics
* Added basic functions (reserved functions)
* Added basic variables (reserved variables)
