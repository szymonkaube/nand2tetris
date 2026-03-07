import sys

from parser import Parser
from code import Code

vm_code_filepath = sys.argv[1]
with open(vm_code_filepath, 'r') as f:
    vm_lines = f.read().splitlines()

parser = Parser()
filename = vm_code_filepath.split("/")[0]
code = Code(filename)

asm_lines = []
for line in vm_lines:
    parsed_line = parser.parse(line)
    if (parsed_line):
        asm_code = code.get_assembly(parsed_line)
        asm_lines.append(asm_code)

asm = "\n".join(asm_lines)
print(asm)
