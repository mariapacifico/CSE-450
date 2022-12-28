# PROJECT 6
# NETID: pacific3
# NAME: Maria Pacifico

from rply import LexerGenerator
from rply import ParserGenerator

class ParserState(object):
  def __init__(self, counter):
    self.counter = counter

class RunTimeState:
  def __init__(self):
    self.sso = [] # relative order of the statements
    self.pc = 0
    self.scache = {} # describing the statement
    self.som = {} # LOOK AT SLIDES; order of execution
    self.symtable = {}

# https://stackoverflow.com/questions/12472338/flattening-a-list-recursively
def flatten(S):
    """
    Function that flattens a list
    :param S: list that needs to be flattened
    :return: Flattened list
    """
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def parse_spartytalk(program):
    """
    Function that parses a program
    :param program: The program needed to parse
    :return: The intermediate representation
    """

    # LEXICAL ANALYSIS
    lexgen = LexerGenerator()

    # comparison tokens
    lexgen.add('EQ', r'==')
    lexgen.add('NOTEQ', r'!=')
    lexgen.add('LESS_EQ', r'<=')
    lexgen.add('GREATER_EQ', r'>=')
    lexgen.add('LESS', r'<')
    lexgen.add('GREATER', r'>')
    lexgen.add('AND', r'and')
    lexgen.add('OR', r'or')
    lexgen.add('NOT', r'not')

    # if else tokens
    lexgen.add('IF', r'if')
    lexgen.add('ELSE', r'else')

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
    lexgen.ignore(r'[ \t\s]+')

    lexer = lexgen.build()
    token_iter = lexer.lex(program)

    # PARSER
    possible_tokens = [rule.name for rule in lexer.rules]

    parsegen = ParserGenerator(possible_tokens,
                               precedence=[('left', ['PLUS', 'MINUS']),
                                           ('left', ['MUL', 'DIV'])])

    # program
    @parsegen.production('program : scope')
    def program_scope(state, p):
        return {
            "type": "program",
            "scope": p[0]
        }

    # scope
    @parsegen.production('scope : GOGREEN SEMICOLON statements GOWHITE SEMICOLON')
    def program(state, p):
        return {
            "type" : 'scope',
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

    @parsegen.production('state : IF boolexp scope')
    def statement_if(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "if",
            "boolexp": p[1],
            "scope": p[2]
        }

    @parsegen.production('state : IF boolexp scope ELSE scope')
    def statement_if_else(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "ifelse",
            "boolexp": p[1],
            "truescope": p[2],
            "falsescope": p[4]
        }

    # boolexp
    @parsegen.production('boolexp : boolexp AND boolexp')
    @parsegen.production('boolexp : boolexp OR boolexp')
    def boolexp_boolexp_andor_boolexp(state, p):
        state.counter += 1

        if p[1].name == "AND":
            return {
                "id": state.counter,
                "type": "boolexp",
                "expression_type": "and",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "OR":
            return {
                "id": state.counter,
                "type": "boolexp",
                "expression_type": "or",
                "left": p[0],
                "right": p[2]
            }
        else:
            return None

    @parsegen.production('boolexp : NOT boolexp')
    def boolexp_not_boolexp(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "boolexp",
            "expression_type": "not",
            "boolexp": p[1]
        }

    @parsegen.production('boolexp : exp GREATER exp')
    @parsegen.production('boolexp : exp LESS exp')
    @parsegen.production('boolexp : exp GREATER_EQ exp')
    @parsegen.production('boolexp : exp LESS_EQ exp')
    @parsegen.production('boolexp : exp EQ exp')
    @parsegen.production('boolexp : exp NOTEQ exp')
    def boolexp_exp_op_exp(state, p):
        state.counter += 1

        if p[1].name == "GREATER":
            return {
                "id": state.counter,
                "type": "boolexp",
                "expression_type": "greater",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "GREATER_EQ":
            return {
                "id": state.counter,
                "type": "boolexp",
                "expression_type": "greater_eq",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "LESS":
            return {
                "id": state.counter,
                "type": "boolexp",
                "expression_type": "less",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "LESS_EQ":
            return {
                "id": state.counter,
                "type": "boolexp",
                "expression_type": "less_eq",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "EQ":
            return {
                "id": state.counter,
                "type": "boolexp",
                "expression_type": "eq",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "NOTEQ":
            return {
                "id": state.counter,
                "type": "boolexp",
                "expression_type": "noteq",
                "left": p[0],
                "right": p[2]
            }
        else:
            return None

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

def evaluate_expression(expression, rts):
    '''
    Function that evaluates expressions
    :param expression: Expression needed to be interpreted
    :param rts: run time state
    :return: value of the expression
    '''

    # identifier
    if expression['expression_type'] == 'identifier':
        # value of the state of the variable
        return rts.symtable[expression["identifier"]]['value']

    # number
    elif expression['expression_type'] == 'number':
        # can be an int or a float
        try:
            return int(expression['value'])
        except ValueError:
            return float(expression['value'])

    # string
    elif expression['expression_type'] == 'string':
        return expression['value']

    # parentheses
    elif expression['expression_type'] == 'parentheses':
        return evaluate_expression(expression['expression'], rts)

    # plus or concat
    elif expression['expression_type'] == "plus":
        # string + string or number + number
        try:
            return evaluate_expression(expression['left'], rts) + evaluate_expression(expression['right'], rts)
        # string + number
        except:
            # only one side will end up being a number
            # check is left side is a string, the other side is a number
            if type(evaluate_expression(expression['left'], rts)) == str:
                return evaluate_expression(expression['left'], rts) + str(evaluate_expression(expression['right'], rts))
            else:
                return str(evaluate_expression(expression['left'], rts)) + evaluate_expression(expression['right'], rts)

    # minus
    elif expression['expression_type'] == "minus":
        return evaluate_expression(expression['left'], rts) - evaluate_expression(expression['right'], rts)

    # division
    elif expression['expression_type'] == "div":
        return evaluate_expression(expression['left'], rts) / evaluate_expression(expression['right'], rts)

    # multiplication
    elif expression['expression_type'] == "mul":
        return evaluate_expression(expression['left'], rts) * evaluate_expression(expression['right'], rts)

def evaluate_boolean_expression(boolexp, rts):
    '''
    Function that evaluates a boolean expression
    :param boolexp: Boolean expression that needs to be interpreted
    :param rts: Run time state
    :return: True or False
    '''
    if boolexp["expression_type"] == "and":
        return evaluate_boolean_expression(boolexp["left"] and boolexp["right"], rts)

    elif boolexp["expression_type"] == "or":
        return evaluate_boolean_expression(boolexp["left"] or boolexp["right"], rts)

    elif boolexp["expression_type"] == "eq":
        return evaluate_expression(boolexp["left"], rts) == evaluate_expression(boolexp["right"], rts)

    elif boolexp["expression_type"] == "noteq":
        return evaluate_expression(boolexp["left"], rts) != evaluate_expression(boolexp["right"], rts)

    elif boolexp["expression_type"] == "less":
        return evaluate_expression(boolexp["left"], rts) < evaluate_expression(boolexp["right"], rts)

    elif boolexp["expression_type"] == "greater":
        return evaluate_expression(boolexp["left"], rts) > evaluate_expression(boolexp["right"], rts)

    elif boolexp["expression_type"] == "less_eq":
        return evaluate_expression(boolexp["left"], rts) <= evaluate_expression(boolexp["right"], rts)

    elif boolexp["expression_type"] == "greater_eq":
        return evaluate_expression(boolexp["left"], rts) >= evaluate_expression(boolexp["right"], rts)

    elif boolexp["expression_type"] == "not":
        return not evaluate_boolean_expression(boolexp["boolexp"], rts)

    else:
        print("Boolean expression evaluation error: unknown expression type.")
        return None

def interpret_scope(scope, rts):
    count = 0
    for statement in scope["statements"]:
        rts.sso.append(statement["id"])
        rts.som[statement["id"]] = count
        rts.scache[statement["id"]] = statement
        count += 1

    # execute program
    while True:
        # get the statement
        statement = rts.scache[rts.sso[rts.pc]]

        # what statement is it
        # spartysays --> printing
        if statement['statement_type'] == 'spartysays':
            #print('STATEMENT', statement)
            print(evaluate_expression(statement['expression'], rts))

        # some sort of assignment --> just need to update symbol table
        if statement['statement_type'] == 'nvar' or statement['statement_type'] == 'svar' or \
                statement['statement_type'] == 'assignment':
            rts.symtable[statement['identifier']] = {
                'value': evaluate_expression(statement['expression'], rts)
            }

        # print boolean
        if statement["statement_type"] == "printbool":
            print(evaluate_boolean_expression(statement["boolexp"], rts))

        # if statement
        if statement["statement_type"] == "if":
            scoperts = RunTimeState()
            scoperts.symtable = rts.symtable
            if evaluate_boolean_expression(statement["boolexp"], rts):
                interpret_scope(statement["scope"], scoperts)

        # if else statement
        if statement["statement_type"] == "ifelse":
            scoperts = RunTimeState()
            scoperts.symtable = rts.symtable
            if evaluate_boolean_expression(statement["boolexp"], rts):
                interpret_scope(statement["truescope"], scoperts)
            else:
                interpret_scope(statement["falsescope"], scoperts)

        if rts.pc == len(rts.sso) - 1:
            break

        rts.pc = rts.som[rts.sso[rts.pc]] + 1

def interpret_spartytalk(program):
    # get the intermediate representation
    ir = parse_spartytalk(program)

    rts = RunTimeState()

    # run the program
    interpret_scope(ir['scope'], rts)