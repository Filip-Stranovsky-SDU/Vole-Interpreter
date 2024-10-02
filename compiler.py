from typing import List, Dict

class Compiler:


    def __init__(self) -> None:
        self.instructions: Dict[str, callable] = {"load": self.manage_load,
                                                  "move": self.manage_move,
                                                  "addi": self.manage_addi,
                                                  "addf": self.manage_addf,
                                                  "store": self.manage_store,
                                                  "or": self.manage_bw,
                                                  "xor": self.manage_bw,
                                                  "and": self.manage_bw,
                                                  "ror": self.manage_ror,
                                                  "jmpEQ": self.manage_jump,
                                                  "jmpLE": self.manage_jump,
                                                  "halt": self.manage_halt
                                                }

    def compile(self, text_file) -> List[int]:
        with open(text_file, 'r') as f:
            lines = f.readlines()
        output: List[int] = []

        for line in lines:
            line = line.strip()
            instruction = line.split(' ')
            output = output + self.instructions[instruction[0]](instruction)

        return output
    
    ## SECTION OF MANAGING INDIVIDUAL FUNCTIONS
    def manage_halt(self, instruction):
        # C0, 00
        return [192, 00]

    def manage_bw(self, instruction):
        operand_vals: Dict[str, int] = {"or": 7, "and": 8, "xor": 9}
        operand = operand_vals[instruction[0]]

        registers = instruction[1].split(",")
        r = int(registers[0], 16)
        s = int(registers[1], 16)
        t = int(registers[2], 16)
        return [operand*16+r, s*16+t]
    
    def manage_ror(self, instruction):
        
        info = instruction[1].split(",")

        return [160+int(info[0], 16), int(info[1], 16)]