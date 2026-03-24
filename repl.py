import main as m

print("WELCOME TO THE MYLANG REPL\nType 'q' to exit\n==========================")

while True:
    src = input(">>> ")

    if src.lower() == "q":
        break

    result, error = m.run(src)

    if error:
        print(error.show())
    else:
        print(result)
