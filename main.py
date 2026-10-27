import os
import sys

from typing     import Any
from subprocess import call
from traceback  import format_exc

from src.scanner     import Scanner
from src.calc_parser import Parser
from src.interpreter import Interpreter
from src.datatypes   import Number


PRINT_TOKENS: bool = False
PRINT_AST: bool = False
PRINT_EXCEPTIONS: bool = False

LAST_ERROR: str = ""

HELP_MESSAGE: str = """
Predefined constants:
@pi  - π value
@e   - Euler value
@tau - 2π

What you can do:

1) Write some expression (for example, 5 + 2)

2) Create variables in two modes (mutable and immutable (constants))
    2.1) Mutable variables example: a = 90
    2.2) Immutable variables example: @another_pi = 14
         (P.S. '@' must be part of the identifier. It's not an operator)

3) Create functions
    For example functions:
    // Square function
    sqr(x) = x * x

    // Squared magnitude of a third dimensional vector
    vec3_len_sqr(x, y, z) = sqr(x) + sqr(y) + sqr(z)

    // Magnitude of a third dimensional vector
    vec3_len(x, y, z) = sqrt(vec3_len_sqr(x, y, z))

    // Storing result into variable
    m_vec3_length = vec3_len(1, 1, 1)
    Output: 1.732...

    // Functions have local scoping
    f(x) = (x = x + 1) 

4) Delete variables and functions
    @m_pi = 3.14
    del @m_pi

    f(x) = x**2
    del f

5) Create points in 2D or 3D
    p0_2D = (0, 1)
    p0_3D = (0, 1, 0)

    p1_2D = (1, 0)
    p1_3D = (1, 0, -1)

    p0_2D + p1_2D
    Output: (1, 1)

    p0_3D == p1_3D
    Output: false

  5.1) Indexing and attribute assignment:
      p0_2D[0]
      Output: 0

      p0_2D::x = 5
      // Updates the X coordinate of the point directly

6) Using of ternary operator
    my_value  = -0.2
    min_bound = 2
    max_bound = 4
    r_max = (my_value > min_bound) ? my_value : min_bound
    r_min = (r_max < max_bound) ? r_max : min_bound
    Output: 2

7) Using of "::" operator (Accessing fields and methods)
    p0_2D = (1, 2)
    p1_2D = (3, 4)
    p0_2D::dist(p1_2D)
    Output: 2.828...

8) Strings
    s = "Hello, " + "World"
    s::upper()
    Output: HELLO, WORLD

    s::split(", ")
    Output: ["Hello", "World"]
    
    "42"::to_number() + 8
    Output: 50

9) Hash Tables (Dictionaries)
    h = {"name": "Desmos", "ver": 1.0}
    h["name"]
    Output: "Desmos"
    
    h::keys
    Output: ["name", "ver"]

10) Booleans and Logic
    t = true
    f = false
    t & f
    Output: false
    
    (5 > 2) | false
    Output: true

11) Operators
    Comparison: ==, !=, <, <=, >, >= (return Boolean)
    Math: +, -, *, /, %, **
    Bitwise/Logic: & (AND), | (OR), ^ (XOR)
    Augmented assignment: +=, -=, *=, /=, %=, **=, &=, |=

Commands for curious people:

.tokens [-f / -t]                   - Toggles or sets tokens flag (shows scanned tokens)
.tree [-f / -t]                     - Toggles or sets tree flag (shows parsed AST)
.debug [-f / -t]                    - Toggles or sets both tokens and tree flags
.always_show_last_error [-f / -t]   - Toggles or sets PRINT_EXCEPTIONS flag. When enabled,
                                      the full traceback of the last error is printed
                                      after each failed evaluation (useful for debugging)
.defines                            - Shows defined identifiers and functions combined
.idents                             - Shows defined identifiers (variables)
.funcs                              - Shows defined functions
.last_error                         - Shows last error traceback
.restart | .reload                  - Restarts program
.clr                                - Clears terminal
.q                                  - Closes program
.help                               - Shows help message
"""


class _RestartProgram(Exception):
    """Raised to trigger a soft restart of the interpreter."""


def _parse_toggle(flag_args: list[str], current: bool) -> tuple[bool, bool]:
    """Parse the '-t' / '-f' suffix for a flag-toggling command.

    Returns (handled, new_value):
      * ([], current)     -> (True,  not current)   -- toggle
      * (['-t'], current) -> (True,  True)          -- force on
      * (['-f'], current) -> (True,  False)         -- force off
      * anything else     -> (False, current)       -- invalid flag
    """
    if not flag_args:
        return True, not current
    if flag_args == ['-t']:
        return True, True
    if flag_args == ['-f']:
        return True, False
    return False, current


def _format_functions(defined_functions: dict[str, tuple[list[str], Any]]) -> dict[str, str]:
    """Formats functions dict for pretty-printing."""
    return {
        name: f"{name}({', '.join(params)}) = {expr}"
        for name, (params, expr) in defined_functions.items()
    }


def __parse_main_input(text: str, *args: Any) -> bool:
    """Returns True if `text` was a dot-command (whether valid or not)."""
    global PRINT_TOKENS, PRINT_AST, PRINT_EXCEPTIONS, LAST_ERROR

    if text == '.clr':
        call('clear' if os.name == "posix" else 'cls', shell=True)
        return True

    flags = text.split()

    match flags[0].strip():
        case '.tokens':
            ok, value = _parse_toggle(flags[1:], PRINT_TOKENS)
            
            if not ok:
                print("Invalid flag")
                return True
            
            PRINT_TOKENS = value
            return True

        case '.tree':
            ok, value = _parse_toggle(flags[1:], PRINT_AST)
            
            if not ok:
                print("Invalid flag")
                return True
            
            PRINT_AST = value
            return True

        case '.debug':
            ok, value = _parse_toggle(flags[1:], PRINT_TOKENS)
            
            if not ok:
                print("Invalid flag")
                return True
            
            PRINT_TOKENS = value
            PRINT_AST = value
            return True

        case '.always_show_last_error':
            ok, value = _parse_toggle(flags[1:], PRINT_EXCEPTIONS)
            
            if not ok:
                print("Invalid flag")
                return True
            
            PRINT_EXCEPTIONS = value
            return True

        case '.idents':
            if len(flags) > 1:
                print("Invalid command")
                return True
            
            print(args[0] if args else {}, end='\n\n')
            return True

        case '.funcs':
            if len(flags) > 1:
                print("Invalid command")
                return True
            
            funcs = args[1] if len(args) > 1 else {}
            funcs_str = _format_functions(funcs)
            
            print(funcs_str if funcs_str else {}, end='\n\n')
            return True

        case '.defines':
            if len(flags) > 1:
                print("Invalid command")
                return True

            idents = args[0] if args else {}
            funcs  = args[1] if len(args) > 1 else {}
            
            funcs_str = _format_functions(funcs)
            
            print(f"Identifiers:\n{idents}\n\nFunctions:\n{funcs_str}", end='\n\n')
            return True

        case '.last_error':
            if len(flags) > 1:
                print("Invalid command")
                return True
            
            print(LAST_ERROR if LAST_ERROR else "(no errors yet)", end='\n\n')
            return True

        case '.help':
            print(HELP_MESSAGE)
            return True
        
        case '.reload' | '.restart':
            raise _RestartProgram()

    return False


def main():
    global LAST_ERROR

    while True:
        defined_identifiers: dict[str, Any] = {
            '@pi':  Number(3.1415926535897932384626433832795),
            '@e':   Number(2.7182818284590452353602874713527),
            '@tau': Number(6.283185307179586476925286766559),
        }
        defined_functions: dict[str, tuple[list[str], Any]] = {}
        
        call('clear' if os.name == "posix" else 'cls', shell=True)
        print("Bobfob's Math Interpreter (type .help for info, .q to quit)")

        while True:
            try:
                src = input('> Input: ')
            except EOFError:
                print()
                return

            if src.strip() == '.q':
                return

            if not src.strip():
                continue

            try:
                if __parse_main_input(src, defined_identifiers, defined_functions):
                    continue

                scanner = Scanner(src)
                scanner.scan()
                tokens = scanner.tokens

                if PRINT_TOKENS:
                    tokens_block = ',\n'.join(f"    {t}" for t in tokens)
                    print(f'\nTokens: [\n{tokens_block}\n]\n')

                parser = Parser(tokens)
                tree = parser.parse()

                if PRINT_AST:
                    print('\nTree:', tree, end='\n\n')

                interpreter = Interpreter(tree, defined_identifiers, defined_functions)
                evaluated = interpreter.eval()
                print(f'> Output: {evaluated}\n')

            except _RestartProgram:
                print("\nReloading program...")
                break
                
            except Exception as e:
                LAST_ERROR = format_exc()

                if PRINT_EXCEPTIONS:
                    print(LAST_ERROR, end='\n\n')
                else:
                    print(f"Caught exception:\n    {e}\n")


if __name__ == '__main__':
    main()
