import sys
from pathlib import Path

from parser import Parser
from code import Code
from symbol_table import SymbolTable


class HackAssembler:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.parser = Parser()
        self.code = Code()

    def assemble(self, assembly_program: str) -> str:
        program_lines = assembly_program.splitlines()

        self._first_pass(program_lines)
        machine_code_lines = self._second_pass(program_lines)

        return "\n".join(machine_code_lines)

    def _first_pass(self, assembly_lines: list[str]) -> None:
        instruction_address = 0

        for line in assembly_lines:
            parsed_line = self.parser.parse(line)
            if not parsed_line:
                continue

            if parsed_line.kind == "L":
                self.symbol_table.add_symbol(
                    parsed_line.symbol,
                    instruction_address
                )
            else:
                instruction_address += 1

    def _second_pass(self, assembly_lines: list[str]) -> list[str]:
        machine_code_lines = []
        for line in assembly_lines:
            parsed_line = self.parser.parse(line)
            if not parsed_line or parsed_line.kind == "L":
                continue

            if parsed_line.kind == "A" and not parsed_line.symbol.isdigit():
                if self.symbol_table.get_symbol(parsed_line.symbol) is None:
                    self.symbol_table.add_symbol(parsed_line.symbol)

                parsed_line.symbol = str(self.symbol_table.get_symbol(
                    parsed_line.symbol
                ))

            machine_code_line = self.code.get_instruction_binary(parsed_line)
            machine_code_lines.append(machine_code_line)

        return machine_code_lines


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    with open(input_filepath, "r") as f:
        assembly_program = f.read()

    hack_assembler = HackAssembler()
    machine_code = hack_assembler.assemble(assembly_program)

    if sys.argv[2]:
        output_path = sys.argv[2]
    else:
        input_path = Path(input_filepath)
        output_name = input_path.with_suffix(".hack").name
        output_path = Path.cwd() / output_name

    with open(output_path, "w") as f:
        f.write(machine_code)
