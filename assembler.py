from typing import List, Dict

class Assembler:


    def __init__(self) -> None:
        self.instructions: Dict[str, callable] = {"load": self.manage_load,
                                                  "move": self.manage_move,
                                                  "addi": self.manage_bw_add,
                                                  "addf": self.manage_bw_add,
                                                  "store": self.manage_store,
                                                  "or": self.manage_bw_add,
                                                  "xor": self.manage_bw_add,
                                                  "and": self.manage_bw_add,
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

    def manage_bw_add(self, instruction):
        operand_vals: Dict[str, int] = {"or": 7, "and": 8, "xor": 9, "addi": 5, "addf": 6}
        operand = operand_vals[instruction[0]]

        registers = instruction[1].split(",")
        r = int(registers[0], 16)
        s = int(registers[1], 16)
        t = int(registers[2], 16)
        return [operand*16+r, s*16+t]
    
    def manage_ror(self, instruction):
        
        info = instruction[1].split(",")

        return [160+int(info[0], 16), int(info[1], 16)]
    
    def manage_move(self, instruction):
        registers = instruction[1].split(",")
        r = int(registers[0], 16)
        s = int(registers[1], 16)

        return [40, r*16 + s]

    def manage_jump(self, instruction):
        op = 11
        if instruction[0] == "jmpLE":
            op = 15

        info = instruction[1].split(",")

        return [op*16+int(info[0][1], 16), int(info[1], 16)]
    
    def manage_store(self, instruction):
        info = instruction[1].split(",")

        if len(info[1]) == 3:
            return [14*16, int(info[0], 16)*16 + int(info[0][1], 16)]
        
        return [3*16 + int(info[0], 16), int(info[0][1:3], 16)]
    
    def manage_load(self, instruction):
        info = instruction[1].split(",")
        
        #2
        if not '[' in info[1]:
            return [32 + int(info[0], 16), int(info[1], 16)]
        
        #D  
        if len(info[1]) == 3:
            return [13*16, int(info[0], 16)*16 + int(info[1][1], 16)]
        
        #1
        return [16 + int(info[0], 16), int(info[1][1:3], 16)] 
