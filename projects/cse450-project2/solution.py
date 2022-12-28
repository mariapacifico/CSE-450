from rply import LexerGenerator
from rply import ParserGenerator

def lex_spartytalk(program):
    lexgen = LexerGenerator()
    # go green token
    lexgen.add('GOGREEN', r'gogreen')
    # go white
    lexgen.add('GOWHITE', r'gowhite')
    # spartysays
    lexgen.add('SPARTYSAYS', r'spartysays')
    # semicolon
    lexgen.add("SEMICOLON", r';')
    # nvar
    lexgen.add("NVAR", r'nvar')
    # svar
    lexgen.add("SVAR", r'svar')
    # number
    lexgen.add("NUMBER", r'[+-]?[0-9]+(\.[0-9]+)?')
    # string
    lexgen.add("STRING", r'"[^"]*"')
    # plus
    lexgen.add("PLUS", r'[+]')
    # minus
    lexgen.add("MINUS", r'[-]')
    # mul
    lexgen.add("MUL", r'[\*]')
    # div
    lexgen.add("DIV", r'/')
    # assignment
    lexgen.add("ASSIGNMENT", r'=')
    # open_parens
    lexgen.add("OPEN_PARENS", r'[\(]')
    # close_parens
    lexgen.add("CLOSE_PARENS", r'[\)]')
    # identifier
    lexgen.add("IDENTIFIER", r'[a-zA-Z][a-zA-Z0-9]*')
    # ignore spaces and new lines
    lexgen.ignore(r' ')
    lexgen.ignore(r'\s')

    # TRY AND EXCEPT
    lexer = lexgen.build()
    token_iter = lexer.lex(program)
    return token_iter

def parse_spartytalk(program):
    # Implement this function
    token_iter = lex_spartytalk(program)

    parsegen = ParserGenerator(["GOGREEN", 'GOWHITE', 'SEMICOLON', 'SPARTYSAYS', 'NVAR',
                                'ASSIGNMENT', 'SVAR', 'OPEN_PARENS', 'CLOSE_PARENS',
                                'PLUS', 'MINUS', 'MUL', 'DIV', 'IDENTIFIER', 'NUMBER',
                                'STRING'],
                               precedence=[('left', ['PLUS', 'MINUS']),
                                           ('left', ['MUL', 'DIV'])])

    # program
    @parsegen.production('program : GOGREEN SEMICOLON statements GOWHITE SEMICOLON')
    def program(p):
        print(f"<program> ::= {p[0]} {p[1]} <statements> {p[3]} {p[4]}")

    # statements
    @parsegen.production('statements : state')
    def statements_state(p):
        print(f"<statements> ::= <statement>")

    @parsegen.production('statements : statements state')
    def statements_statements(p):
        print(f"<statements> ::= <statements> <statement>")

    # statement
    @parsegen.production('state : SPARTYSAYS exp SEMICOLON')
    def state_spartysays(p):
        print(f"<statement> ::= {p[0]} <expression> {p[2]}")
        return

    @parsegen.production('state : NVAR IDENTIFIER ASSIGNMENT exp SEMICOLON')
    def state_nvar(p):
        print(f"<statement> ::= {p[0]} {p[1]} {p[2]} <expression> {p[4]}")

    @parsegen.production('state : SVAR IDENTIFIER ASSIGNMENT exp SEMICOLON')
    def state_svar(p):
        print(f"<statement> ::= {p[0]} {p[1]} {p[2]} <expression> {p[4]}")

    @parsegen.production('state : IDENTIFIER ASSIGNMENT exp SEMICOLON')
    def state_ident(p):
        print(f"<statement> ::= {p[0]} {p[1]} <expression> {p[3]}")

    # expressions
    @parsegen.production('exp : IDENTIFIER')
    def exp_identifier(p):
        print(f"<expression> ::= {p[0]}")
        return

    @parsegen.production('exp : NUMBER')
    def exp_num(p):
        print(f"<expression> ::= {p[0]}")
        return

    @parsegen.production('exp : STRING')
    def exp_string(p):
        print(f"<expression> ::= {p[0]}")
        return

    @parsegen.production('exp : OPEN_PARENS exp CLOSE_PARENS')
    def exp_paren(p):
        print(f"<expression> ::= {p[0]} <expression> {p[2]}")
        return

    @parsegen.production('exp : exp PLUS exp')
    def exp_plus(p):
        print(f"<expression> ::= <expression> {p[1]} <expression>")
        return

    @parsegen.production('exp : exp MINUS exp')
    def exp_minus(p):
        print(f"<expression> ::= <expression> {p[1]} <expression>")
        return

    @parsegen.production('exp : exp MUL exp')
    def exp_mul(p):
        print(f"<expression> ::= <expression> {p[1]} <expression>")
        return

    @parsegen.production('exp : exp DIV exp')
    def exp_div(p):
        print(f"<expression> ::= <expression> {p[1]} <expression>")
        return

    parser = parsegen.build()

    # raise a value error if it doesn't parse correctly
    try:
        parser.parse(token_iter)
    except:
        raise ValueError

    return
