class Parser:
    def __init__(self):
        self.comment_symbol = "//"

    def parse(self, line: str):
        line = line.strip()

        if not line or line.startswith(self.comment_symbol):
            return None

        line = self._remove_inline_comment(line)
        return line

    def _remove_inline_comment(self, line: str) -> str:
        if self.comment_symbol in line:
            line = line.split(self.comment_symbol)[0]
        return line.strip()
