import re

from data_types import ParsedInstruction, AFields, CFields


class Parser:
    def __init__(self):
        self.comment_symbol = "//"
        self.a_instruction_symbol = "@"
        self.register_value_length = 15

    def parse(self, lines: list) -> list[ParsedInstruction]:
        parsed_lines = []

        for line in lines:
            line = line.strip()

            if not line or line.startswith(self.comment_symbol):
                continue

            line = self._remove_inline_comment(line)
            if not line:
                continue

            is_a_instruction = line.startswith(self.a_instruction_symbol)
            if is_a_instruction:
                instruction = ParsedInstruction(
                    "A",
                    self._get_a_instruction_fields(line)
                )
            else:
                instruction = ParsedInstruction(
                    "C",
                    self._get_c_instruction_fields(line)
                )

            parsed_lines.append(instruction)

        return parsed_lines

    def _remove_inline_comment(self, line: str) -> str:
        line_w_no_comments = line
        if self.comment_symbol in line:
            line_w_no_comments = line.split(self.comment_symbol)[0]

        return line_w_no_comments

    def _get_a_instruction_fields(self, line: str) -> AFields:
        return AFields(line[1:])

    def _get_c_instruction_fields(self, line: str) -> CFields:
        pattern = r"(?:(?P<dest>[^=;]+)=)?(?P<comp>[^=;]+)(?:;(?P<jump>[^=;]+))?"
        match = re.fullmatch(pattern, line)

        dest = match.group("dest")
        comp = match.group("comp")
        jump = match.group("jump")

        return CFields(dest, comp, jump)
