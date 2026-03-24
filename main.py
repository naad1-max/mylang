import logic as l


def run(code: str | object):
    lines = code.split("\n")

    for line in lines:
        tokenizer = l.Tokenizer(line)
        tokens, error = tokenizer.tokenize()
        parser = l.Parser(tokens)
        result, error2 = parser.parse()
        
        if error:
            print(error.show())
        elif error2:
            print(error2.show())
        else:
            return result, None
