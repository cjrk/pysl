from .parsec import *
import os

whitespace = regex(r'[ \t]*')
lexeme = lambda p: p << whitespace
optional = lambda p, default: p ^ string('').result(default)

lparen = lexeme(string('('))
rparen = lexeme(string(')'))
lbracket = lexeme(string('['))
rbracket = lexeme(string(']'))
comma = lexeme(string(','))
colon = lexeme(string(':'))
le =  lexeme(string(os.linesep)) # lineending

ident = lexeme(regex(r'[a-zA-Z_][a-zA-Z0-9_]*'))
comment = whitespace >> regex("//.*?")


## for generators
def join(elements, sep='', start='', end=''):
	result = start
	result += sep.join(elements)
	result += end
	return result