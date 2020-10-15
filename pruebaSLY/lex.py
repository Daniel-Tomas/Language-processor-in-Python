# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { CTE_ENTERA, CADENA, CTE_LOGICA, OP_ARIT, OP_ESP,
               OP_REL, OP_LOG, OP_ASIG, ID, NUMBER, STRING, BOOLEAN, LET, ALERT,
               INPUT, FUNCTION, RETURN, IF, FOR,EOF}

    ignore = ' \t\n'
    ignore_comment = r'(?s)/\*.*?\*/'

    # Tokens
    CTE_ENTERA = r'\d+'
    CADENA = r'".*?"'
    CTE_LOGICA = r'true|false'
    OP_ESP = r'--'
    OP_ARIT = r'\+|-'
    OP_REL = r'=='
    OP_ASIG = r'='
    OP_LOG = r'&&'

    ID = r'[a-zA-Z][a-zA-Z0-9_]*'
    ID['number'] = NUMBER
    ID['string'] = STRING
    ID['boolean'] = BOOLEAN
    ID['let'] = LET
    ID['alert'] = ALERT
    ID['input'] = INPUT
    ID['function'] = FUNCTION
    ID['return'] = RETURN
    ID['if'] = IF
    ID['for'] = FOR

    # Revisar EOF quizá lo hace automáticamente
    literals = {'(', ')','{', '}', ',', ';', '/d'}

    def CTE_ENTERA(self, t):
        t.value = int(t.value)
        if t.value > 32767:
            print(f'Número fuera de rango: "{t.value}"')
            exit(1)
        return t

    def CADENA(self,t):
        t.value = t.value[1:-1]
        if len(t.value) > 64:
            print(f'Cadena demasiado larga: "{t.value}"')
            exit(1)
        return t

    def CTE_LOGICA(self, t):
        """Called when a token which is a logical constant is found

        It modifies the argument token changing its str value to an int value.
        The token value will be 0 if "false" is found or 1 if "true"

        Args:
            t(Token): Token which matches the logical constant pattern

        Returns:
            Token: Token modified
        """

        if t.value == 'false':
            t.value = 0
        else:
            t.value = 1
        return t

    #TODO: Para hacer cuando se de la TS
    #def ID(self,t):

    def OP_ARIT(self,t):
        if t.value == '+':
            t.value = 0
        else:
            t.value = 1
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

if __name__ == '__main__':
    #data = 'x_Aa= 3 + 42 * (s - t)'
    data = '''true'''
    lexer = CalcLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))