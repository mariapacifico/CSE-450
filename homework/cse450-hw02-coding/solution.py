
def question01(text):
    # Implement this function that takes a string and returns a list of tokens.
    # Each character in the string should be lexed into the tokens "UPPER", "LOWER" or "OTHER" depending on the case of the character.
    # See the open tests for better understanding of the assignment.

    from rply import LexerGenerator
    lg = LexerGenerator()

    # Add your code here
    lg.add('UPPER', r'[A-Z]')
    lg.add('LOWER', r'[a-z]')
    lg.add('OTHER', r'[^A-Za-z]')

    lexer = lg.build()

    return list(lexer.lex(text))

def question02(text):
    # Implement this function that takes a string and returns a list of tokens.
    # The string should be tokenized into:
    #   - NON_TITLE_CASE (things like: "table", "HOUSE");
    #   - TITLE_CASE (things like: "Hat", "Josh", "A"); and 
    #   - OTHER (things like punctation, digits).
    # Whitespaces should be ignored.
    # See the open tests for better understanding of the assignment.

    from rply import LexerGenerator
    lg = LexerGenerator()

    # Add your code here
    lg.add('TITLE_CASE', r'[A-Z][a-z]+')
    lg.add('NON_TITLE_CASE', r'[A-Za-z]+')
    lg.add('OTHER', r'[^A-Za-z]')
    lg.ignore(r'\s+')

    lexer = lg.build()

    return list(lexer.lex(text))


