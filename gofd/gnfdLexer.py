# Generated from gnfd.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,13,59,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,
        1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,4,1,5,1,5,1,6,1,6,5,6,43,8,
        6,10,6,12,6,46,9,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,
        12,1,12,0,0,13,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,
        11,23,12,25,13,1,0,2,2,0,65,90,97,122,4,0,48,57,65,90,95,95,97,122,
        59,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,
        11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,
        21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,1,27,1,0,0,0,3,29,1,0,0,0,5,
        31,1,0,0,0,7,33,1,0,0,0,9,35,1,0,0,0,11,38,1,0,0,0,13,40,1,0,0,0,
        15,47,1,0,0,0,17,49,1,0,0,0,19,51,1,0,0,0,21,53,1,0,0,0,23,55,1,
        0,0,0,25,57,1,0,0,0,27,28,5,38,0,0,28,2,1,0,0,0,29,30,5,58,0,0,30,
        4,1,0,0,0,31,32,5,44,0,0,32,6,1,0,0,0,33,34,5,45,0,0,34,8,1,0,0,
        0,35,36,5,61,0,0,36,37,5,62,0,0,37,10,1,0,0,0,38,39,5,46,0,0,39,
        12,1,0,0,0,40,44,7,0,0,0,41,43,7,1,0,0,42,41,1,0,0,0,43,46,1,0,0,
        0,44,42,1,0,0,0,44,45,1,0,0,0,45,14,1,0,0,0,46,44,1,0,0,0,47,48,
        5,60,0,0,48,16,1,0,0,0,49,50,5,91,0,0,50,18,1,0,0,0,51,52,5,40,0,
        0,52,20,1,0,0,0,53,54,5,62,0,0,54,22,1,0,0,0,55,56,5,93,0,0,56,24,
        1,0,0,0,57,58,5,41,0,0,58,26,1,0,0,0,3,0,42,44,0
    ]

class gnfdLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    AMPERSAND = 1
    COLON = 2
    COMMA = 3
    DASH = 4
    DETERMINES = 5
    DOT = 6
    IDENTIFIER = 7
    LANGLE = 8
    LBRACK = 9
    LPAR = 10
    RANGLE = 11
    RBRACK = 12
    RPAR = 13

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'&'", "':'", "','", "'-'", "'=>'", "'.'", "'<'", "'['", "'('", 
            "'>'", "']'", "')'" ]

    symbolicNames = [ "<INVALID>",
            "AMPERSAND", "COLON", "COMMA", "DASH", "DETERMINES", "DOT", 
            "IDENTIFIER", "LANGLE", "LBRACK", "LPAR", "RANGLE", "RBRACK", 
            "RPAR" ]

    ruleNames = [ "AMPERSAND", "COLON", "COMMA", "DASH", "DETERMINES", "DOT", 
                  "IDENTIFIER", "LANGLE", "LBRACK", "LPAR", "RANGLE", "RBRACK", 
                  "RPAR" ]

    grammarFileName = "gnfd.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


