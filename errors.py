class Error:
    def __init__(self, name, error):
        self.name = name
        self.error = error

    def show(self):
        return f"{self.name}: {self.error}"


class IllegalCharError(Error):
    def __init__(self, error):
        super().__init__("Illegal Character", error)


class IllegalOpError(Error):
    def __init__(self, error):
        super().__init__("Illegal Operation", error)


class ExpectedCharError(Error):
    def __init__(self, error):
        super().__init__("Expected character", error)
        