import main as m

print("WELCOME TO THE MYLANG REPL\nType 'q' to exit\n==========================")

while True:
    src = input(">>> ")
    tokens, error = m.run(src)

    if src.lower() == "q":
        break

    if error:
        print(error.show())
    else:
        print(tokens)
