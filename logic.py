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


class Parser:
    def __init__(self, tokens: list | object):
        self.tokens = tokens
        self.idx = -1
        self.current = None
        self.advance()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current = self.tokens[self.idx]
        else:
            self.current = None

    def parse(self):
        result = self.expr()
        if self.current is not None and self.current.type != t.EOF:
            return 0, e.IllegalCharError("unexpected token")
        return result, None

    def expr(self):
        result = self.term()

        while self.current is not None and self.current.type in (t.PLUS, t.MINUS):
            op = self.current
            self.advance()
            right = self.term()

            if op.type == t.PLUS:
                result = result + right
            elif op.type == t.MINUS:
                result = result - right

        return result

    def term(self):
        result = self.factor()

        while self.current is not None and self.current.type in (t.MUL, t.DIV):
            op = self.current
            self.advance()
            right = self.factor()

            if op.type == t.MUL:
                result = result * right
            elif op.type == t.DIV:
                if right == 0:
                    return e.IllegalOpError("division by zero")
                result = result / right

        return result

    def factor(self):
        token = self.current

        if token.type in (t.INT, t.FLOAT):
            self.advance()
            return token.value

        elif token.type == t.LPAREN:
            self.advance()
            result = self.expr()
            if self.current is None or self.current.type != t.RPAREN:
                return e.IllegalOpError("missing closing parenthesis")
            self.advance()
            return result

        elif token.type == t.PLUS:
            self.advance()
            return self.factor()

        elif token.type == t.MINUS:
            self.advance()
            return -self.factor()

        return e.IllegalOpError("invalid syntax")
