# PROJECT 7
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

    # while token
    lexgen.add('WHILE', r'while')

    # function tokens
    lexgen.add('FUNCTION', r'function')
    lexgen.add('RETURN', r'return')
    lexgen.add('CALL', r'call')

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
    # comma
    lexgen.add('COMMA', r',')

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

    @parsegen.production('state : WHILE boolexp scope')
    def statement_while(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "while",
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

    @parsegen.production('state : FUNCTION IDENTIFIER OPEN_PARENS parameters CLOSE_PARENS scope')
    def statement_function(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "function",
            "name": p[1].value,
            "parameters": p[3],
            "scope": p[5]
        }

    @parsegen.production('state : FUNCTION IDENTIFIER OPEN_PARENS CLOSE_PARENS scope')
    def statement_function_empty(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "function",
            "name": p[1].value,
            "parameters": [],
            "scope": p[4]
        }

    @parsegen.production('state : CALL IDENTIFIER OPEN_PARENS arguments CLOSE_PARENS SEMICOLON')
    def statement_call(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "call",
            "name": p[1].value,
            "arguments": p[3]
        }

    @parsegen.production('state : CALL IDENTIFIER OPEN_PARENS CLOSE_PARENS SEMICOLON')
    def statement_call_empty(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "call",
            "name": p[1].value,
            "arguments": []
        }

    @parsegen.production('arguments : argument')
    def arguments_argument(state, p):
        return [p[0]]

    @parsegen.production('arguments : arguments COMMA argument')
    def arguments_arguments_argument(state, p):
        pp = p[0].copy()
        pp.append(p[2])
        return pp

    @parsegen.production('argument : exp')
    def arguemnt_expression(state, p):
        return p[0]

    @parsegen.production('state : RETURN exp SEMICOLON')
    def statement_return(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "statement",
            "statement_type": "return",
            "expression": p[1]
        }

    @parsegen.production('parameters : parameter')
    def parameters_parameter(state, p):
        return [p[0]]

    @parsegen.production('parameters : parameters COMMA parameter')
    def parameters_parameters_parameter(state, p):
        p[0].append(p[2])
        return p[0]

    # what about numbers?
    @parsegen.production('parameter : IDENTIFIER')
    def parameter_variable(state, p):
        return p[0].value

    # boolexp
    @parsegen.production('boolexp : boolexp AND boolexp')
    @parsegen.production('boolexp : boolexp OR boolexp')
    def boolexp_boolexp_andor_boolexp(state, p):
        state.counter += 1
        return_dict = {
                "id": state.counter,
                "type": "boolexp",
                "left": p[0],
                "right": p[2]
            }
        if p[1].name == "AND":
            return_dict['expression_type'] = 'and'
        elif p[1].name == "OR":
            return_dict['expression_type'] = 'or'
        else:
            return None
        return return_dict

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
        return_dict = {
                "id": state.counter,
                "type": "boolexp",
                "left": p[0],
                "right": p[2]
            }

        if p[1].name == "GREATER":
            return_dict['expression_type'] = 'greater'
        elif p[1].name == "GREATER_EQ":
            return_dict['expression_type'] = 'greater_eq'
        elif p[1].name == "LESS":
            return_dict['expression_type'] = 'less'
        elif p[1].name == "LESS_EQ":
            return_dict['expression_type'] = 'less_eq'
        elif p[1].name == "EQ":
            return_dict['expression_type'] = 'eq'
        elif p[1].name == "NOTEQ":
            return_dict['expression_type'] = 'noteq'
        else:
            return None
        return return_dict

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
    @parsegen.production('exp : exp MINUS exp')
    @parsegen.production('exp : exp DIV exp')
    @parsegen.production('exp : exp MUL exp')
    def exp_div(state, p):
        state.counter += 1
        return_dict = {
            "id": state.counter,
            "type": "expression",
            "left": p[0],
            "right": p[2]
        }
        if p[1].name == 'PLUS':
            return_dict['expression_type'] = 'plus'
        elif p[1].name == 'MINUS':
            return_dict['expression_type'] = 'minus'
        elif p[1].name == 'MUL':
            return_dict['expression_type'] = 'mul'
        elif p[1].name == 'DIV':
            return_dict['expression_type'] = 'div'
        else:
            return None
        return return_dict

    @parsegen.production('exp : CALL IDENTIFIER OPEN_PARENS arguments CLOSE_PARENS')
    def expression_call(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "expression",
            "expression_type": "call",
            "name": p[1].value,
            "arguments": p[3]
        }

    @parsegen.production('exp : CALL IDENTIFIER OPEN_PARENS CLOSE_PARENS')
    def expression_call_empty(state, p):
        state.counter += 1
        return {
            "id": state.counter,
            "type": "expression",
            "expression_type": "call",
            "name": p[1].value,
            "arguments": []
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

    elif expression["expression_type"] == "call":
        scoperts = RunTimeState()

        params = rts.symtable[expression["name"]]["parameters"]

        for k in rts.symtable.keys():
            try:
                if rts.symtable[k]["type"] == "function":
                    scoperts.symtable[k] = rts.symtable[k]
            except:
                continue

        for i in range(len(expression["arguments"])):
            argexpr = expression["arguments"][i]

            scoperts.symtable[params[i]] = {
                "type": "variable",
                "value": evaluate_expression(argexpr, rts)
            }

        return interpret_scope(rts.symtable[expression["name"]]["scope"], scoperts)

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

        if statement["statement_type"] == "while":
            scoperts = RunTimeState()
            scoperts.symtable = rts.symtable

            while evaluate_boolean_expression(statement["boolexp"], rts):
                scoperts.sso = []
                scoperts.pc = 0
                scoperts.scache = {}
                scoperts.som = {}
                scoperts.symtable = rts.symtable

                interpret_scope(statement["scope"], scoperts)

        if statement["statement_type"] == "function":
            rts.symtable[statement["name"]] = {
                "type": "function",
                "scope": statement["scope"],
                "parameters": statement["parameters"]
            }

        if statement["statement_type"] == "call":
            scoperts = RunTimeState()

            params = rts.symtable[statement["name"]]["parameters"]

            #print('DELETE LATER1:', rts.symtable)

            for k in rts.symtable.keys():
                try:
                    if rts.symtable[k]["type"] == "function":
                        scoperts.symtable[k] = rts.symtable[k]
                except:
                    continue

            for i in range(len(statement["arguments"])):
                argexpr = statement["arguments"][i]

                scoperts.symtable[params[i]] = {
                    "type": "variable",
                    "value": evaluate_expression(argexpr, rts)
                }

            interpret_scope(rts.symtable[statement["name"]]["scope"], scoperts)

        if statement["statement_type"] == "return":
            return evaluate_expression(statement["expression"], rts)

        if rts.pc == len(rts.sso) - 1:
            break

        rts.pc = rts.som[rts.sso[rts.pc]] + 1

def interpret_spartytalk(program):
    # get the intermediate representation
    ir = parse_spartytalk(program)

    rts = RunTimeState()

    # run the program
    interpret_scope(ir['scope'], rts)