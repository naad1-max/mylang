import sys
from main import run

if len(sys.argv) < 2:
    print("No file provided")
    sys.exit(1)

with open(sys.argv[1]) as f:
    lines = f.read().split("\n")

for line in lines:
    result, error = run(line)
    if error:
        print(error.show())
        break
    else:
        print(result)
