# netid: pacific3
# name: Maria Pacifico

from rply import LexerGenerator
from rply import ParserGenerator

def question01(text):
    # Use RPLY to write a compiler for a simple markup language.
    # In this language, any text between double parentheses
    # must be capitalized. For example, the following input text:
    # 
    # Hello ((world))!
    #
    # should compile into the following output:
    #
    # Hello WORLD!
    #
    # Remember, you should use RPLY lexing and parsing for that.
    # Bypassing this requirement will result in 0 points for the
    # assignment, even if all tests pass.
    #
    # As always, see the unit tests to better understand the 
    # assignment.
    # 
    # Tip 1: Parse the surrounding text symbol by symbol. Attempting
    # to capture large blocks may result in the parser never finishing.
    # Tip 2: The regular expression [\w\W\n] effectively captures 
    # what we usually refer to as "any character".

    lexgen = LexerGenerator()

    lexgen.add('OPEN_PAREN', r'[\(][\(]')
    lexgen.add('CLOSE_PAREN', r'[\)][\)]')
    lexgen.add('CHAR', r'[\w\W\n]')

    lexer = lexgen.build()

    tokens_iter = lexer.lex(text)

    possible_tokens = [rule.name for rule in lexer.rules]

    pg = ParserGenerator(possible_tokens)

    @pg.production('statement : statement words')
    @pg.production('statement : statement paren')
    def statement_wordsparen(p):
        return p[0] + p[1]

    @pg.production('statement : paren')
    @pg.production('statement : words')
    def statement(p):
        return p[0]

    @pg.production('paren : OPEN_PAREN words CLOSE_PAREN')
    def paren(p):
        return p[1].upper()

    @pg.production('paren : OPEN_PAREN CLOSE_PAREN')
    def paren_empty(p):
        return ''

    @pg.production('words : CHAR')
    def words(p):
        return p[0].value

    @pg.production('words : words CHAR')
    def words_char(p):
        return p[0] + p[1].value

    parser = pg.build()

    return parser.parse(tokens_iter)