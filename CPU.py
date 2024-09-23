class CPU:
    def __init__(self):
        self.registers = [0] * 16
        self.memory = [0]*256
        self.pc = 0 #Program Counter

    
    def parse_instruction(self, memory_adress: int):
        pass