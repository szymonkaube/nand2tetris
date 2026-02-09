import sys
from pathlib import Path

from parser import Parser
from code import Code


input_filepath = sys.argv[1]
with open(input_filepath, "r") as f:
    lines = f.read().splitlines()

result = []

parser = Parser()
code = Code()
for line in lines:
    instruction = parser.parse(line)
    if not instruction:
        continue

    binary = code.get_instruction_binary(instruction)

    result.append(binary)

output = "\n".join(result)

input_path = Path(input_filepath)
output_name = input_path.with_suffix(".hack").name
output_path = Path.cwd() / output_name

with open(output_path, "w") as f:
    f.write(output)
