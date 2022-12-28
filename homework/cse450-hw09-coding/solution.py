# Homework 9
# Student name: Maria Pacifico

from rply import LexerGenerator
from rply import ParserGenerator

def question01(text):
    # Use RPLY to write a compiler for a simple markup language
    # that recognizes URLs and converts them into HTML hyperlinks.
    # In this language, a URL enclosed in double square brackets
    # should be converted by the compiler into an HTML hyperlink
    # with the link text defaulted to [link]. For example, the 
    # following input text:
    # 
    # Nick's website: [[https://nick-ivanov.com]]
    #
    # should compile into the following output:
    #
    # Nick's website: <a href='https://nick-ivanov.com'>[link]</a>
    #
    # We assume the URL in the brackets is properly formatted.
    #
    # Remember, you should use RPLY lexing and parsing for that.
    # Bypassing this requirement will result in 0 points for the
    # assignment, even if all tests pass.
    #
    # As always, see the unit tests to better understand the 
    # assignment.
    # 
    # Tip: Representing links through grammar rules is possible
    # but fraught with challenges. Tracking opening and closing
    # sets of brackets is possible but not easy either. I suggest
    # to catch the link as a whole lexeme, and then perform 
    # manual analysis of the corresponding tokens.

    lexgen = LexerGenerator()

    lexgen.add('LINK', r'\[\[[^\]]*\]\]')
    lexgen.add('CHAR', r'[\w\W\n^\[^\]]')

    lexer = lexgen.build()

    tokens_iter = lexer.lex(text)

    possible_tokens = [rule.name for rule in lexer.rules]

    pg = ParserGenerator(possible_tokens)


    @pg.production('statement : statement word')
    def statement_words(p):
        return p[0] + p[1]

    @pg.production('statement : word')
    def statement_word(p):
        return p[0]

    @pg.production('word : LINK')
    def link(p):
        end_index = p[0].value.find(']')
        return "<a href='"+p[0].value[2:end_index]+"'>[link]</a>"

    @pg.production('word : word CHAR')
    def word_chars(p):
        return p[0] + p[1].value

    @pg.production('word : CHAR')
    def word_char(p):
        return p[0].value

    parser = pg.build()

    return parser.parse(tokens_iter)