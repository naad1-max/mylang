import tokens as t
import errors as e


class Tokenizer:
    def __init__(self, source: str | object):
        self.source = source
        self.main = None
        self.idx = -1
        self.forward()

    def forward(self):
        self.idx += 1
        if self.idx < len(self.source):
            self.main = self.source[self.idx]
        else:
            self.main = None

    def tokenize(self):
        tokens = []

        while self.main is not None:
            if self.main in " \t":
                self.forward()
            elif self.main in t.DIGITS:
                tokens.append(self.numericize())
            elif self.main == "+":
                tokens.append(t.Token(t.PLUS))
                self.forward()
            elif self.main == "-":
                tokens.append(t.Token(t.MINUS))
                self.forward()
            elif self.main == "*":
                tokens.append(t.Token(t.MUL))
                self.forward()
            elif self.main == "/":
                tokens.append(t.Token(t.DIV))
                self.forward()
            elif self.main == "(":
                tokens.append(t.Token(t.LPAREN))
                self.forward()
            elif self.main == ")":
                tokens.append(t.Token(t.RPAREN))
                self.forward()
            else:
                char = self.main
                self.forward()
                return [], e.IllegalCharError("'" + char + "'")

        tokens.append(t.Token(t.EOF))
        return tokens, None

    def numericize(self):
        value_as_str = ""
        point_counter = 0

        while self.main is not None and self.main in (t.DIGITS + "."):
            if self.main == ".":
                if point_counter == 1:
                    break
                point_counter += 1
                value_as_str += "."
            else:
                value_as_str += self.main
            self.forward()

        if point_counter == 0:
            return t.Token(t.INT, int(value_as_str))
        else:
            return t.Token(t.FLOAT, float(value_as_str))
