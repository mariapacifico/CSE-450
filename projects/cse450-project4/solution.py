from rply import LexerGenerator
from rply import ParserGenerator
import json

class ParserState(object):
  def __init__(self, counter):
    self.counter = counter

# https://stackoverflow.com/questions/12472338/flattening-a-list-recursively
def flatten(S):
    """
    This function is used to flatten lists
    """
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def lex_spartytalk(program):
    """
    Function to preform lexer analysis on a program
    :param program: String of a program
    :return: token iterator
    """
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
    def program(state, p):
        #return
        return {
            "type" : 'program',
            "statements" : flatten([p[2]])
        }

    # statements
    @parsegen.production('statements : state')
    def statements_state(state, p):
        return p[0]

    @parsegen.production('statements : statements state')
    def statements_statements(state, p):
        return [p[0]] + [p[1]]

    # statement
    @parsegen.production('state : SPARTYSAYS exp SEMICOLON')
    def state_spartysays(state, p):
        state.counter += 1
        return {
            "id" : state.counter,
            "type" : "statement",
            "statement_type" : "spartysays",
            "expression" : p[1]
        }

    @parsegen.production('state : NVAR IDENTIFIER ASSIGNMENT exp SEMICOLON')
    def state_nvar(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type" : "statement",
            "statement_type" : "nvar",
            "identifier" : p[1].value,
            "expression" : p[3]
        }

    @parsegen.production('state : SVAR IDENTIFIER ASSIGNMENT exp SEMICOLON')
    def state_svar(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "svar",
            "identifier": p[1].value,
            "expression": p[3]
        }

    @parsegen.production('state : IDENTIFIER ASSIGNMENT exp SEMICOLON')
    def state_ident(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type" : "statement",
            "statement_type" : "assignment",
            "identifier" : p[0].value,
            "expression" : p[2]
        }

    # expressions
    @parsegen.production('exp : IDENTIFIER')
    def exp_identifier(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type" : "expression",
            "expression_type" : "identifier",
            "identifier" : p[0].value
        }

    @parsegen.production('exp : NUMBER')
    def exp_num(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type" : "expression",
            "expression_type" : "number",
            "value" : p[0].value
        }

    @parsegen.production('exp : STRING')
    def exp_string(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "expression",
            "expression_type": "string",
            "value": p[0].value[1:-1]
        }

    @parsegen.production('exp : OPEN_PARENS exp CLOSE_PARENS')
    def exp_paren(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            'type' : 'expression',
            'expression_type' : 'parentheses',
            'expression' : p[1]
        }

    @parsegen.production('exp : exp PLUS exp')
    def exp_plus(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type" : "expression",
            "expression_type" : "plus",
            "left" : p[0],
            "right" : p[2]
        }

    @parsegen.production('exp : exp MINUS exp')
    def exp_minus(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "expression",
            "expression_type": "minus",
            "left": p[0],
            "right": p[2]
        }

    @parsegen.production('exp : exp MUL exp')
    def exp_mul(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "expression",
            "expression_type": "mul",
            "left": p[0],
            "right": p[2]
        }

    @parsegen.production('exp : exp DIV exp')
    def exp_div(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "expression",
            "expression_type": "div",
            "left": p[0],
            "right": p[2]
        }

    # error
    @parsegen.error
    def syntax_error(state, token):
        raise Exception({
            "type" : "error",
            "tokentype" : token.gettokentype(),
            "line": token.getsourcepos().lineno,
            "column": token.getsourcepos().colno,
            "id": state.counter
        })

    parser = parsegen.build()

    final = parser.parse(token_iter, state=ParserState(0))
    return final


def interpret_spartytalk(ast):
    # Implement this function
    final = []
    for statement in ast['statements']:
        final.append(statement['id'])
    return final