import sys, os
import ply.yacc as yacc
import ply.lex as lex

'''
T  = { '.', ';', '[', ']', num }
NT = { S, Is, RI, I }
P = { p1: Sentence  : Signal Intervals '.'
         p6: Signal : '+'
parser.sentido = 1
         p7: Signal : '-'		
parser.sentido = -1
         p2: Intervals : Interval RemainingIntervals
         p3: RemainingIntervals : 
         p4: RemainingIntervals : Interval RemainingIntervals
         p5: Interval  : '[' num ';' num ']'   
		CC1:    p[4] > p[2]  &
		CC2:    p[2] >= parser.anterior
		parser.anterior = p[4]
		parser.erro = not (CC1) or not (CC2)

 }
'''

# List of token names.   This is always required
tokens = (
    'NUM',
    'PLUS',
    'MINUS',
    'SEMICOLON',
    'DOT',
    'LBRACKET',
    'RBRACKET',
)

# Regular expression rules for simple tokens
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_SEMICOLON  = r';'
t_DOT        = r'\.'
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'
t_ignore     = ' \t'

# A regular expression rule with some action code
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Parsing rules
def p_sentence(p):
    '''Sentence : Signal Intervals DOT'''
    pass

def p_signal_plus(p):
    '''Signal : PLUS'''
    parser.sentido = 1

def p_signal_minus(p):
    '''Signal : MINUS'''
    parser.sentido = -1

def p_intervals(p):
    '''Intervals : Interval RemainingIntervals'''
    pass

def p_remaining_intervals_empty(p):
    '''RemainingIntervals :'''
    pass

def p_remaining_intervals(p):
    '''RemainingIntervals : Interval RemainingIntervals'''
    pass

def p_interval(p):
    '''Interval : LBRACKET NUM SEMICOLON NUM RBRACKET'''
    if p[4] > p[2] and p[2] >= parser.anterior:
        parser.anterior = p[4]
    else:
        parser.erro = True

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the lexer
lexer = lex.lex()

# Build the parser
parser = yacc.yacc()

# Read input and parse it
with open("test_input.txt", "r") as file:
    data = file.read()

parser.anterior = 0
parser.erro = False
parser.sentido = 1
parser.parse(data, lexer=lexer)
if parser.erro:
    print("Erro")
else:
    print("Ok")
