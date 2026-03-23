import logic as l


def run(code: str | object):
    tokenizer = l.Tokenizer(code)
    tokens, error = tokenizer.tokenize()

    return tokens, error
