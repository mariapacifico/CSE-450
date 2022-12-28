import re
from rply import LexerGenerator
from rply.errors import LexingError

def lex_spartytalk(program):
    # Implement this function

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
    try:
        tokens = list(lexer.lex(program))
        return (tokens, -1, -1)
    except LexingError as e:
        return (None, e.getsourcepos().lineno, e.getsourcepos().colno)
