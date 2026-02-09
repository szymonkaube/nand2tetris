from typing import Optional

from data_types import ParsedLine


class Code:
    COMP = {
        "0":   "0101010",
        "1":   "0111111",
        "-1":  "0111010",
        "D":   "0001100",
        "A":   "0110000",
        "!D":  "0001101",
        "!A":  "0110001",
        "-D":  "0001111",
        "-A":  "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",

        # a = 1 (M versions)
        "M":   "1110000",
        "!M":  "1110001",
        "-M":  "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101",
    }

    DEST = {
        None:  "000",
        "M":   "001",
        "D":   "010",
        "MD":  "011",
        "A":   "100",
        "AM":  "101",
        "AD":  "110",
        "AMD": "111",
    }

    JUMP = {
        None:  "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    def get_instruction_binary(self, line: ParsedLine):
        if line.kind == "A":
            return self._a_instruction_to_binary(line)
        else:
            return self._c_instruction_to_binary(line)

    def _a_instruction_to_binary(self, line: ParsedLine) -> str:
        binary = format(int(line.symbol), "b")
        num_padding_zeros = 16 - len(binary)
        return num_padding_zeros * "0" + binary

    def _c_instruction_to_binary(self, line: ParsedLine) -> str:
        return (
            "111"
            + self._comp(line.fields.comp)
            + self._dest(line.fields.dest)
            + self._jump(line.fields.jump)
        )

    def _comp(self, mnemonic: str) -> str:
        return self.COMP[mnemonic]

    def _dest(self, mnemonic: Optional[str]) -> str:
        return self.DEST[mnemonic]

    def _jump(self, mnemonic: Optional[str]) -> str:
        return self.JUMP[mnemonic]
