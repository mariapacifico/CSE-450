def question01(text):
    # Implement this function that takes a string and checks that the three sets of braces "()<>{}" are all matched properly.
    # Any characters other than the 6 characters for braces should raise an Exception exception.
    # Any mismatched braces should raise an Exception exception.
    # If the string is fine, nothing need be done.
    # You must use rply's LexerGenerator and ParserGenerator to solve this problem.

    from rply import LexerGenerator
    from rply import ParserGenerator

    lexgen = LexerGenerator()

    lexgen.add('OPEN_PARAENTHESIS', r'\(')
    lexgen.add('CLOSE_PARAENTHESIS', r'\)')
    lexgen.add('OPEN_ARROW', r'\<')
    lexgen.add('CLOSE_ARROW', r'\>')
    lexgen.add('OPEN_CURL', r'\{')
    lexgen.add('CLOSE_CURL', r'\}')

    lexer = lexgen.build()

    token_iter = lexer.lex(text)

    parsegen = ParserGenerator(['OPEN_PARAENTHESIS', 'CLOSE_PARAENTHESIS', 'OPEN_ARROW', 'CLOSE_ARROW',
                                'OPEN_CURL', 'CLOSE_CURL'])

    # <expression> ::= <expression> { <expression> } |  <expression> ( <expression> )
    #               | <expression> < <expression> >
    @parsegen.production('exp : exp OPEN_PARAENTHESIS exp CLOSE_PARAENTHESIS')
    def expression1(p):
        return "expression1"
    @parsegen.production('exp : exp OPEN_ARROW exp CLOSE_ARROW')
    def expression2(p):
        return "expression2"
    @parsegen.production('exp : exp OPEN_CURL exp CLOSE_CURL')
    def sexpression3(p):
        return "expression3"

    # <expression> ::= { <expression> } |  ( <expression> ) | < <expression> >
    @parsegen.production('exp : OPEN_PARAENTHESIS exp CLOSE_PARAENTHESIS')
    def expression4(p):
        return "expression4"
    @parsegen.production('exp : OPEN_ARROW exp CLOSE_ARROW')
    def expression5(p):
        return "expression5"
    @parsegen.production('exp : OPEN_CURL exp CLOSE_CURL')
    def expression6(p):
        return "expression6"

    # <expression> ::= <expression> <expression>
    @parsegen.production('exp : exp exp')
    def expression7(p):
        return "expression7"

    # expression ::= () | <> | {}
    @parsegen.production('exp : OPEN_PARAENTHESIS CLOSE_PARAENTHESIS')
    def expression8(p):
        return "expression8"
    @parsegen.production('exp : OPEN_ARROW CLOSE_ARROW')
    def expression9(p):
        return "expression9"
    @parsegen.production('exp : OPEN_CURL CLOSE_CURL')
    def expression10(p):
        return "expression10"


    # @parsegen.error
    # def error(token):
    #     print('error')
    #     raise Exception()

    parser = parsegen.build()
    # parser.parse(token_iter)
    try:
        parser.parse(token_iter)
    except:
        # ignore empty text
        if text != "":
            raise Exception()