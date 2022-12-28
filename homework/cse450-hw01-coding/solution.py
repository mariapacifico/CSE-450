import re
from rply import LexerGenerator
from rply.errors import LexingError

def question01(line):
    # Write a python program that takes a line of text and outputs it prefixed by the number of characters in that line.
    # See test case for output format.
    new_string = str(len(line)) + ": " + line
    return new_string

def question02(sentence):
    # For a sentence, return a set of words (whitespace delimited strings).
    # If a digit (0-9) occurs in the sentence raise an exception.

    lexgen = LexerGenerator()
    # add any numbers
    lexgen.add('NUMBERS', r'[0-9]*')
    # ignore any other symbol
    lexgen.ignore(r'[^0-9]+')
    lexer = lexgen.build()
    # make a list
    tokens = list(lexer.lex(sentence))
    # there are numbers within the sentence
    if (len(tokens) > 0):
        raise Exception

    # if there are no numbers
    final_set = set()
    words = sentence.split()
    for word in words:
        final_set.add(word)

    return final_set