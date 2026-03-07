from commands import Command, PushCommand, PopCommand, ArithmeticCommand


class Parser:
    def __init__(self):
        self.comment_symbol = "//"

    def parse(self, line: str) -> Command:
        line = line.strip()

        if not line or line.startswith(self.comment_symbol):
            return None

        line = self._remove_inline_comment(line)

        parts = line.split()
        cmd_type = parts[0]

        match cmd_type:
            case "push":
                return PushCommand(parts[1], int(parts[2]))
            case "pop":
                return PopCommand(parts[1], int(parts[2]))
            case _:
                return ArithmeticCommand(cmd_type)

    def _remove_inline_comment(self, line: str) -> str:
        if self.comment_symbol in line:
            line = line.split(self.comment_symbol)[0]
        return line.strip()
