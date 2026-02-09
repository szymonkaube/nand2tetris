import sys

from parser import Parser
from code import Code


filename = sys.argv[1]
with open(filename, "r") as f:
    lines = f.read().splitlines()

result = []

parser = Parser()
code = Code()
for line in lines:
    instruction = parser.parse(line)
    if not instruction:
        continue

    binary = code.get_instruction_binary(instruction)
    print(binary)
