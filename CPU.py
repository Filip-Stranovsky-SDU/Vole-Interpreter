from typing import List

class CPU:

    registers: list[int] = [0] * 16
    memory: list[int] = [0]*256
    pc: int = 0 #Program Counter
    is_running: bool = False

    def __init__(self, program):
        self.program = program
        
        self.op_code_fucntions: List[function] = [self.load_m_r, self.load_v_r, self.store_r_m,
                                                self.move_r_r, self.addi, self.addf,
                                                self.bw_or, self.bw_and, self.bw_xor,
                                                self.bw_ror, self.jmp_eq, self.halt,
                                                self.load_rm_r, self.store_r_rm, self.jmp_le]

    
    def parse_instruction(self, memory_adress: int) -> list[int]:
        current_memory_val = self.memory[memory_adress]
        next_memory_val = self.memory[memory_adress + 1]

        return [current_memory_val>>4, current_memory_val%16, next_memory_val>>4, next_memory_val%16]


    def step(self):
        instruction = self.parse_instruction(self.pc)
        self.pc = self.pc + 2

        self.op_code_fucntions[instruction[0]](instruction)

        print(self.registers)
        

    def run(self):
        self.step()
        if self.is_running:
            self.program.canvas.after(1000, self.run)

        
    
    def start_cpu_run(self):
        if not self.is_running:
            self.is_running = True
            self.run()
        else:
            self.is_running = False

    ## SECTION OF INDIVIDUAL INSTRUCTIONS:
    def load_m_r(self, instruction):
        #1RXY
        #load R, [XY]
        #register[R] = XY
        self.registers[instruction[1]] = self.memory[instruction[2]*16 + instruction[3]]
    
    def load_v_r(self, instruction):
        #2RXY
        #load R, [XY]
        #register[R] := XY
        self.registers[instruction[1]] = instruction[2]*16 + instruction[3]

    def store_r_m(self, instruction):
        #3RXY
        #store R, [XY]
        #memory[XY] := register[R]
        self.memory[instruction[2]*16 + instruction[3]] = self.registers[instruction[1]]
    
    def move_r_r(self, instruction):
        #40RS
        #move S, R
        #register[S] := register[R]
        self.registers[instruction[3]] = self.registers[instruction[2]]
    
    def addi(self, instruction):
        #5RST
        #addi R,S,T
        #register[R] := register[S] + register[T]
        self.registers[instruction[3]] = self.registers[instruction[1]] + self.registers[instruction[2]]

        self.registers[instruction[3]] = self.registers[instruction[3]] % 256

    def addf(self, instruction):
        #6RST
        #addf R,S,T
        #register[R] := register[S] + register[T]
        r_s = self.registers[instruction[2]]
        r_t = self.registers[instruction[3]]
        
        sign_s = r_s // 128
        sign_t = r_t // 128

        exponent_s = (r_s >> 4) % 8
        exponent_t = (r_t >> 4) % 8

        mantissa_s = r_s % 16
        mantissa_t = r_t % 16
        
        result = sign_s * (mantissa_s << exponent_s) + sign_t * (mantissa_t << exponent_t)
        self.registers[instruction[3]] = 0

        if(result < 0):
            result = -result
            self.registers[instruction[3]] = self.registers[instruction[3]] + 128
        while(result > 16):
            result = result >> 1
            self.registers[instruction[3]] = self.registers[instruction[3]] + 16
        self.registers[instruction[3]] = self.registers[instruction[3]] + result

    def bw_or(self, instruction):
        #7RST
        #or R,S,T
        #register[R] := register[S] or register[T]
        self.registers[instruction[3]] = self.registers[instruction[1]] | self.registers[instruction[2]]

    def bw_and(self, instruction):
        #8RST
        #and R,S,T
        #register[R] := register[S] and register[T]
        self.registers[instruction[3]] = self.registers[instruction[1]] & self.registers[instruction[2]]
    
    def bw_xor(self, instruction):
        #9RST
        #xor R,S,T
        #register[R] := register[S] xor register[T]
        self.registers[instruction[3]] = self.registers[instruction[1]] ^ self.registers[instruction[2]]
    
    def bw_ror(self, instruction):
        #AR0X
        #ror R,X
        #register[R] := register[R] ROR X
        n = self.registers[instruction[1]]
        d = instruction[3]
        self.registers[instruction[1]] = (n >> d)|(n << (8 - d)) & 0xFF

    def jmp_eq(self, instruction):
        #BRXY
        #jmpEQ R=R0, XY
        #PC:=XY, if R=R0
        if self.registers[instruction[1]] == self.registers[0]:
            self.pc = instruction[2]*16 + instruction[3]
        
    def halt(self, instruction):
        #C000
        #halt program
        self.is_running = False
    
    def load_rm_r(self, instruction):
        #D0RS
        #load R,[S]
        #register[r] := memory[register[s]]
        self.registers[instruction[2]] = self.memory[self.registers[instruction[3]]]
    
    def store_r_rm(self, instruction):
        #E0RS
        #store R,[S]
        #memory[register[s]] := register[r]
        self.memory[self.registers[instruction[3]]] = self.registers[instruction[2]]

    def jmp_le(self, instruction):
        #FRXY
        #jmpEQ R<=R0, XY
        #PC:=XY, if R<=R0
        if self.registers[instruction[1]] <= self.registers[0]:
            self.pc = instruction[2]*16 + instruction[3]