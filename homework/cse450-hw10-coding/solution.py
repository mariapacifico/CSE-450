# Homework 10
# Student name: Maria Pacifico

from rply import LexerGenerator
from rply import ParserGenerator

def question01(text):
    # Use RPLY to write a compiler for a simple markup language
    # that recognizes links in the format [[URL]]((TEXT)) and 
    # converts them into HTML hyperlinks. In this language, the URL
    # is enclosed in double square brackets, and the link text is
    # enclosed in double parentheses. The link should be converted
    # by the compiler into an HTML hyperlink. For example, the 
    # following input text:
    # 
    # Class website: [[https://www.cse.msu.edu/~cse450/]]((here))
    #
    # should compile into the following output:
    #
    # Class website: <a href='https://www.cse.msu.edu/~cse450/'>here</a>
    #
    # We assume the URL is properly formatted.
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
    # sets of brackets and parentheses is possible but not easy 
    # either. I suggest to catch the link as a whole lexeme, and
    # then perform manual textual analysis of the corresponding tokens.

    lexgen = LexerGenerator()

    lexgen.add('URL', r'\[\[[^\]]*\]\]')
    lexgen.add('TEXT', r'\(\([^\)]*\)\)')

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

    @pg.production('word : word CHAR')
    def word_chars(p):
        return p[0] + p[1].value

    @pg.production('word : CHAR')
    def word_char(p):
        return p[0].value

    @pg.production('word : link')
    def word_link(p):
        return p[0]

    @pg.production('link : url text')
    def link(p):
        print('LINK', p[0], p[1])
        return "<a href='"+p[0]+"'>"+p[1]+"</a>"

    @pg.production('text : TEXT')
    def text(p):
        end_index = p[0].value.find("))")
        return p[0].value[2:end_index]

    @pg.production('url : URL')
    def url(p):
        end_index = p[0].value.find("]]")
        return p[0].value[2:end_index]

    parser = pg.build()

    return parser.parse(tokens_iter)