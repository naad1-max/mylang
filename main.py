import logic as l


def run(code):
    tokenizer = l.Tokenizer(code)
    tokens, error = tokenizer.tokenize()
    if error:
        return None, error
    parser = l.Parser(tokens)
    result, error = parser.parse()
    if error:
        return None, error
    return result, None
