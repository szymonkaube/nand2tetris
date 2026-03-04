import sys

from parser import Parser

vm_code_filepath = sys.argv[1]
with open(vm_code_filepath, 'r') as f:
    vm_lines = f.read().splitlines()

parser = Parser()
parsed_lines = []
for line in vm_lines:
    parsed_line = parser.parse(line)
    if (parsed_line):
        parsed_lines.append(parsed_line)

print(parsed_lines)
