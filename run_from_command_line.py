import sys
from main import run

if len(sys.argv) < 2:
    print("No file provided")
    sys.exit(1)

with open(sys.argv[1]) as f:
    lines = f.read()

result, error = run(lines)
if error:
    print(error.show())
    quit()

print(result)
