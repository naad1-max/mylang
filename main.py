import logic as l


def run(code: str | object):
    lines = code.split("\n")

    for line in lines:
        tokenizer = l.Tokenizer(line)
        tokens, error = tokenizer.tokenize()
        return tokens, error
