import tokens as t
import errors as e


class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.idx = -1
        self.main = None
        self.vars = {}
        self.forward()

    def forward(self):
        self.idx += 1
        self.main = self.source[self.idx] if self.idx < len(self.source) else None

    def tokenize(self):
        tokens = []

        while self.main is not None:
            if self.main in " \t\n\r":
                self.forward()
            elif self.main in t.DIGITS:
                tokens.append(self.numericize())
            elif self.main.isalpha():
                word = self.collect_word()
                if word == "let":
                    res = self.assign()
                    if isinstance(res, tuple):
                        return res
                    tokens.extend(res)
                elif word in self.vars:
                    tokens.append(t.Token(t.VAR, self.vars[word]))
                else:
                    return None, e.IllegalCharError("'" + word + "'")
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
        points = 0

        while self.main is not None and self.main in t.DIGITS + ".":
            if self.main == ".":
                if points == 1:
                    break
                points += 1
            num += self.main
            self.forward()

        if points == 0:
            return t.Token(t.INT, int(num))
        return t.Token(t.FLOAT, float(num))

    def collect_word(self):
        word = ""
        while self.main is not None and (
            self.main.isalpha() or self.main.isdigit() or self.main == "_"
        ):
            word += self.main
            self.forward()
        return word

    def assign(self):
        while self.main is not None and self.main in " \t":
            self.forward()
        name = ""
        while self.main is not None and (
            self.main.isalpha() or self.main.isdigit() or self.main == "_"
        ):
            name += self.main
            self.forward()
        while self.main is not None and self.main in " \t":
            self.forward()
        if self.main != "=":
            return [], e.ExpectedCharError("'=' expected")
        self.forward()
        while self.main is not None and self.main in " \t":
            self.forward()
        value_str = ""
        while self.main is not None and self.main not in " \t\n":
            value_str += self.main
            self.forward()
        try:
            value = float(value_str) if "." in value_str else int(value_str)
        except ValueError:
            return [], e.IllegalCharError(f"invalid value '{value_str}'")
        self.vars[name] = value
        return []


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
        results = []
        while self.current and self.current.type != t.EOF:
            result = self.expr()
            if isinstance(result, e.Error):
                return None, result
            results.append(result)
            if self.current and self.current.type == t.EOF:
                break
        if not results:
            return None, e.IllegalOpError("no expression")
        if len(results) == 1:
            return results[0], None
        return results, None

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
            result += right if op.type == t.PLUS else -right
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
    