from commands import Command, PushCommand, PopCommand, ArithmeticCommand


class Code:
    def __init__(self, filename: str):
        self.filename = filename.split(".")[0]
        self.segment_map = {
            "local": "LCL",
            "argument": "ARG",
            "pointer": ["THIS", "THAT"]
        }

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

        asm_load_d = ""
        if push_command.segment in ("local", "argument", "this", "that"):
            asm_load_d = f"@{segment_pointer}\nD=M\n@{i}\nA=D+A\nD=M\n"
        elif push_command.segment == "constant":
            asm_load_d = f"@{i}\nD=A\n"
        elif push_command.segment == "static":
            asm_load_d = f"@{self.filename}.{i}\nD=M\n"
        elif push_command.segment == "temp":
            target_address = 5 + int(i)
            asm_load_d = f"@{target_address}\nD=M\n"
        elif push_command.segment == "pointer":
            segment_pointer = segment_pointer[i]
            asm_load_d = f"@{segment_pointer}\nD=M\n"
        else:
            raise ValueError(f"Push command has unknown segment type: {
                             push_command.segment}")

        asm_push = (
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )

        return asm_load_d + asm_push

    def _get_pop_assembly(self, pop_command: PopCommand) -> str:
        pass

    def _get_arithmetic_assembly(self, arithmetic_command: ArithmeticCommand) -> str:
        pass
