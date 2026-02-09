from typing import Optional


class SymbolTable:
    def __init__(self):
        self.table = {
            "R0": 0, "R1": 1, "R2": 2, "R3": 3,
            "R4": 4, "R5": 5, "R6": 6, "R7": 7,
            "R8": 8, "R9": 9, "R10": 10, "R11": 11,
            "R12": 12, "R13": 13, "R14": 14, "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4
        }
        self.first_free_address = 16

    def add_symbol(self, symbol: str, address: Optional[int] = None) -> None:
        if address is None:
            address = self._get_free_address()
        self.table[symbol] = address

    def get_symbol(self, symbol: str) -> Optional[int]:
        try:
            return self.table[symbol]
        except KeyError:
            return None

    def _get_free_address(self) -> int:
        free_address = self.first_free_address
        if free_address + 1 >= self.table["SCREEN"]:
            raise Exception("No more free addresses left.")
        else:
            self.first_free_address += 1
        return free_address
