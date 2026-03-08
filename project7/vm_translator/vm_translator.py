import sys
from pathlib import Path

from parser import Parser
from code import Code


class VMTranslator:
    def __init__(self, filename):
        self.filename = filename
        self.parser = Parser()
        self.code = Code(filename)

    def translate(self, vm_code: str) -> str:
        vm_lines = vm_code.splitlines()
        asm_lines = []
        for vm_line in vm_lines:
            parsed_line = self.parser.parse(vm_line)
            if parsed_line:
                asm_code = self.code.get_assembly(parsed_line)
                asm_lines.append(f"// {vm_line}")
                asm_lines.append(asm_code)

        return "\n".join(asm_lines)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    filename = input_filepath.split("/")[0]
    with open(input_filepath, "r") as f:
        vm_code = f.read()

    vm_translator = VMTranslator(filename)
    asm = vm_translator.translate(vm_code)

    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        input_path = Path(input_filepath)
        output_name = input_path.with_suffix(".asm").name
        output_path = Path.cwd() / output_name

    with open(output_path, "w") as f:
        f.write(asm)

