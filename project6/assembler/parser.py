import re

from data_types import ParsedLine, CFields


class Parser:
    def __init__(self):
        self.comment_symbol = "//"
        self.a_instruction_symbol = "@"

    def parse(self, line: str) -> ParsedLine | None:
        line = line.strip()

        if not line or line.startswith(self.comment_symbol):
            return None

        line = self._remove_inline_comment(line)
        if not line:
            return None

        is_symbol_line = self._is_symbol_line(line)
        is_a_instruction = line.startswith(self.a_instruction_symbol)
        if is_symbol_line:
            parsed_line = ParsedLine(
                kind="L",
                symbol=self._get_symbol_line_symbol(line)
            )
        elif is_a_instruction:
            parsed_line = ParsedLine(
                kind="A",
                symbol=self._get_a_instruction_fields(line)
            )
        else:
            parsed_line = ParsedLine(
                kind="C",
                fields=self._get_c_instruction_fields(line)
            )

        return parsed_line

    def _is_symbol_line(self, line: str) -> bool:
        return line.startswith("(") and line.endswith(")")

    def _remove_inline_comment(self, line: str) -> str:
        if self.comment_symbol in line:
            line = line.split(self.comment_symbol)[0]

        return line.strip()

    def _get_a_instruction_fields(self, line: str) -> str:
        return line[1:]

    def _get_c_instruction_fields(self, line: str) -> CFields:
        pattern = r"(?:(?P<dest>[^=;]+)=)?(?P<comp>[^=;]+)(?:;(?P<jump>[^=;]+))?"
        match = re.fullmatch(pattern, line)

        dest = match.group("dest")
        comp = match.group("comp")
        jump = match.group("jump")

        return CFields(dest, comp, jump)

    def _get_symbol_line_symbol(self, line: str) -> str:
        return line[1:-1]
