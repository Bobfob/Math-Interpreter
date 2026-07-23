from subprocess      import call
from os              import name, system
from sys             import version_info

from src.lexer       import Lexer
from src.calc_parser import Parser
from src.interpreter import Interpreter


PRINT_TOKENS: bool = False
PRINT_AST: bool = False

HELP_MASSAGE: str = """
Predefined constants:

pi - PI value
e - E value
tau - 2*PI

What you can do:

1) Write some expression (for example, 5 + 2)

2) Create variables in two modes (mutable and immutable (constants))
    2.1) Mutable variables example: a = 90
    2.2) Immutable variables example: @another_pi = 14 (P.S. '@' must be part of the identifier. It's not an operator)

3) Create functions
    For example functions:
    // Square function
    sqr(x) = x * x
    
    // Squared magnitude of a third dimensional vector
    vec3_len_sqr(x, y) = sqr(x) + sqr(y)
    
    // Magnitude of a third dimensional vector
    vec3_len(x, y) = sqrt(vec3_len_sqr(x, y))
    
    // Storing result into variable
    m_vec3_length = vec3_len(1, 1)
    Output: 1.414...

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
    Output: False

  5.1) Indexing this points:
      p0_2D[0]
      Output: 0

6) Using of ternary operator
    my_value  = -0.2
    min_bound = 2
    max_bound = 4
    r_max = (my_value > a) ? my_value : a
    r_min = (r_max < b) ? r_max : b
    Output: 2

Commands for curios people:

.tokens [-f / -t] - Toggles or sets tokens flag (shows scanned tokens)
.tree [-f / -t] - Toggles or sets tree flag (shows parsed AST in human readable form)
.debug [-f / -t] - Toggles or sets tokens and tree flags
.defines - Shows defined identifiers and functions combined
.idents - Shows defined identifiers (variables)
.funcs - Shows defined functions
.clr - Clears terminal
.q - Closes program
.help - Shows help massage
"""


def __parse_main_input(text: str, *args) -> bool:
    """Returns True if """
    global PRINT_TOKENS, PRINT_AST
    
    
    if text == '.clr':
        if version_info >= (3, 14):
            call('clear' if name == "posix" else 'cls', shell=True)
        
        else:
            system('clear' if name == 'posix' else 'cls')
        
        return True

    
    flags = text.split()
    
    
    match flags[0].strip():
        case '.tokens':
            if len(flags) == 1:
                PRINT_TOKENS = not PRINT_TOKENS
                return True
            

            elif len(flags) == 2 and flags[1].strip() == '-t':
                PRINT_TOKENS = True
                return True
            

            elif len(flags) == 2 and flags[1].strip() == '-f':
                PRINT_TOKENS = False
                return True
            

            print("Invalid flag")
            return False
    

        case '.tree':
            if len(flags) == 1:
                PRINT_AST = not PRINT_AST
                return True
            

            elif len(flags) == 2 and flags[1].strip() == '-t':
                PRINT_AST = True
                return True
            

            elif len(flags) == 2 and flags[1].strip() == '-f':
                PRINT_AST = False
                return True
            

            print("Invalid flag")
            return False
    

        case '.debug':
            if len(flags) == 1:
                PRINT_TOKENS = not PRINT_TOKENS
                PRINT_AST = not PRINT_AST
                return True
            

            if len(flags) == 2 and flags[1].strip() == '-t':
                PRINT_TOKENS = True
                PRINT_AST = True
                return True
            

            elif len(flags) == 2 and flags[1].strip() == '-f':
                PRINT_TOKENS = False
                PRINT_AST = False
                return True
            

            print("Invalid flag")
            return False
    
    
        case '.idents':
            if len(flags) > 1:
                print("Invalid command")
                return True
            
            
            elif args:
                print(args[0])
                return True
    
    
        case '.funcs':
            if len(flags) > 1:
                print("Invalid command")
                return True
            
            
            elif args:
                print(args[1])
                return True
        
        
        case '.help':
            print(HELP_MASSAGE)
            return True

        
        case '.defines':
            if len(flags) > 1:
                print("Invalid command")
                return True
            
            elif args:
                print(args[0], args[1], sep='\n\n', end='\n\n')
                return True
    
    
    return False


def main():
    # desc: "name": "value"
    defined_identifiers: dict[str, float] = {
        '@pi':  3.1415926535897932384626433832795,
        '@e':   2.7182818284590452353602874713527,
        '@tau': 6.283185307179586476925286766559,
    }
    
    
    # desc: "name": ("params", "expr")
    defined_functions = {}
    
    
    while (src := input('> Input: ')) != '.q':
        try:
            if __parse_main_input(src, defined_identifiers, defined_functions):
                continue
            
    
            lexer = Lexer(src)
            tokens = lexer.tokenize()
            
    
            if PRINT_TOKENS:
                print(f'\nTokens: [\n{',\n'.join([f"    {token}" for token in tokens])}\n]\n')

    
            parser = Parser(tokens)
            tree = parser.parse()
            
    
            if PRINT_AST:
                print('\nTree:', tree, end='\n\n')

    
            interpreter = Interpreter(tree, defined_identifiers, defined_functions)
            evaluated = interpreter.eval()
            print(f"> Output: {evaluated}\n")
            
    
            # Updating identifiers
            if interpreter.defined_identifiers != defined_identifiers:
                defined_identifiers = interpreter.defined_identifiers
            
    
            # Updating functions
            if interpreter.defined_functions != defined_functions:
                defined_functions = interpreter.defined_functions
        
        
        except Exception as e:
            print(e, end="\n\n")


if __name__ == '__main__':
    main()
    print('\n[Program finished]')
