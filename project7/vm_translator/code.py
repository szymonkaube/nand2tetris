from commands import Command, PushCommand, PopCommand, ArithmeticCommand


class Code:
    def __init__(self, filename: str):
        self.filename = filename.split(".")[0]
        self.segment_map = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "pointer": ["THIS", "THAT"]
        }
        self.arithmetic_map = {
            "add": "D+M",
            "sub": "M-D",
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
            "and": "D&M",
            "or": "D|M",
            "neg": "-M",
            "not": "!M"
        }
        self.logic_label_counter = 0

    def get_assembly(self, vm_command: Command) -> str:
        match vm_command:
            case PushCommand():
                return self._get_push_assembly(vm_command)
            case PopCommand():
                return self._get_pop_assembly(vm_command)
            case ArithmeticCommand():
                return self._get_arithmetic_assembly(vm_command)
            case _:
                raise ValueError(f"Unknown command type: {type(vm_command)}")

    def _get_push_assembly(self, push_command: PushCommand) -> str:
        segment_pointer = self.segment_map.get(push_command.segment)
        i = push_command.i

        if push_command.segment in ("local", "argument", "this", "that"):
            # addr = segment_pointer + i, D = *addr
            asm = [f"@{segment_pointer}", "D=M", f"@{i}", "A=D+A", "D=M"]
        elif push_command.segment == "constant":
            # D = i
            asm = [f"@{i}", "D=A"]
        elif push_command.segment == "static":
            # D = *FileName.i
            asm = [f"@{self.filename}.{i}", "D=M"]
        elif push_command.segment == "temp":
            # D = *(5 + i)
            target_address = 5 + int(i)
            asm = [f"@{target_address}", "D=M"]
        elif push_command.segment == "pointer":
            # pointer 0 -> THIS, pointer 1 -> THAT
            segment_pointer = segment_pointer[i]
            asm = [f"@{segment_pointer}", "D=M"]
        else:
            raise ValueError(f"Push command has unknown segment type: {push_command.segment}")

        # universal "push D to stack"
        asm.extend([
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ])

        return "\n".join(asm)

    def _get_pop_assembly(self, pop_command: PopCommand) -> str:
        segment_pointer = self.segment_map.get(pop_command.segment)
        i = pop_command.i

        if pop_command.segment in ("local", "argument", "this", "that"):
            asm = [f"@{segment_pointer}", "D=M", f"@{i}", "D=D+A",
                   "@R13", "M=D",
                   "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]
        elif pop_command.segment == "constant":
            raise ValueError("We cannot pop to constant")
        elif pop_command.segment == "static":
            asm = ["@SP", "AM=M-1", "D=M", f"@{self.filename}.{i}", "M=D"]
        elif pop_command.segment == "temp":
            target_address = 5 + int(i)
            asm = ["@SP", "AM=M-1", "D=M", f"@{target_address}", "M=D"]
        elif pop_command.segment == "pointer":
            segment_pointer = segment_pointer[i]
            asm = ["@SP", "AM=M-1", "D=M", f"@{segment_pointer}", "M=D"]
        else:
            raise ValueError(f"Pop command has unknown segment type: {pop_command.segment}")

        return "\n".join(asm)

    def _get_arithmetic_assembly(self, arithmetic_command: ArithmeticCommand) -> str:
        if arithmetic_command.op in ("add", "sub", "and", "or"):
            asm_op = self.arithmetic_map[arithmetic_command.op]
            asm = ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", f"M={asm_op}"]
        elif arithmetic_command.op in ("eq", "gt", "lt"):
            asm_op = self.arithmetic_map[arithmetic_command.op]
            asm = ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D",
                   f"@TRUE_{self.logic_label_counter}", f"D;{asm_op}",
                   "@SP", "A=M-1", "M=0",
                   f"@DONE_{self.logic_label_counter}", "0;JMP",
                   f"(TRUE_{self.logic_label_counter})",
                   "@SP", "A=M-1", "M=-1",
                   f"(DONE_{self.logic_label_counter})"]
            self.logic_label_counter += 1
        elif arithmetic_command.op in ("neg", "not"):
            asm_op = self.arithmetic_map[arithmetic_command.op]
            asm = ["@SP", "A=M-1", f"M={asm_op}"]
        else:
            raise ValueError(f"Arithmetic command has unknown operation type: f{arithmetic_command.op}")

        return "\n".join(asm)
