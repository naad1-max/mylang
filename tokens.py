DIGITS = "0123456789"

VAR = "VAR"
INT = "INT"
FLOAT = "FLOAT"

PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
EQUAL = "EQUAL"

LPAREN = "LPAREN"
RPAREN = "RPAREN"

EOF = "EOF"


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
    