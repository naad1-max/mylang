class Error:
    def __init__(self, name: str, error: str | object):
        self.name = name
        self.error = error

    def show(self):
        error_str = f"{self.name}: {self.error}"
        return error_str


class IllegalCharError(Error):
    def __init__(self, error):
        super().__init__("Illegal Character", error)
