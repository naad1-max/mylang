import tokens as t
import errors as e


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.idx = -1
        self.main = None
        self.forward()

    def forward(self):
        self.idx += 1
        self.main = self.source[self.idx] if self.idx < len(self.source) else None

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
                return None, e.IllegalCharError("'" + char + "'")

        tokens.append(t.Token(t.EOF))
        return tokens, None

    def numericize(self):
        num = ""
        dots = 0

        while self.main is not None and self.main in t.DIGITS + ".":
            if self.main == ".":
                if dots == 1:
                    break
                dots += 1
            num += self.main
            self.forward()

        if dots == 0:
            return t.Token(t.INT, int(num))
        return t.Token(t.FLOAT, float(num))


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = -1
        self.current = None
        self.advance()

    def advance(self):
        self.idx += 1
        self.current = self.tokens[self.idx] if self.idx < len(self.tokens) else None

    def parse(self):
        result = self.expr()
        if isinstance(result, e.Error):
            return None, result
        if self.current and self.current.type != t.EOF:
            return None, e.IllegalOpError("unexpected token")
        return result, None

    def expr(self):
        result = self.term()
        if isinstance(result, e.Error):
            return result

        while self.current and self.current.type in (t.PLUS, t.MINUS):
            op = self.current
            self.advance()
            right = self.term()

            if isinstance(right, e.Error):
                return right

            if op.type == t.PLUS:
                result += right
            else:
                result -= right

        return result

    def term(self):
        result = self.factor()
        if isinstance(result, e.Error):
            return result

        while self.current and self.current.type in (t.MUL, t.DIV):
            op = self.current
            self.advance()
            right = self.factor()

            if isinstance(right, e.Error):
                return right

            if op.type == t.MUL:
                result *= right
            else:
                if right == 0:
                    return e.IllegalOpError("division by zero")
                result /= right

        return result

    def factor(self):
        token = self.current

        if token.type in (t.INT, t.FLOAT):
            self.advance()
            return token.value

        if token.type == t.LPAREN:
            self.advance()
            result = self.expr()
            if isinstance(result, e.Error):
                return result
            if not self.current or self.current.type != t.RPAREN:
                return e.IllegalOpError("missing closing parenthesis")
            self.advance()
            return result

        if token.type == t.PLUS:
            self.advance()
            return self.factor()

        if token.type == t.MINUS:
            self.advance()
            value = self.factor()
            if isinstance(value, e.Error):
                return value
            return -value

        return e.IllegalOpError("invalid syntax")
