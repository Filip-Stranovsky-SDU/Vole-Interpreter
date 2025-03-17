from typing import List, Dict
import re

class Assembler:

    
    bw_operand_vals: Dict[str, int] = {"or": 7, "and": 8, "xor": 9, "addi": 5, "addf": 6}
    label_dictionary: Dict[str, int] = {}

    def __init__(self) -> None:
        self._instructions: Dict[str, callable] = {"load": self.manage_load,
                                                  "move": self.manage_move,
                                                  "addi": self.manage_bw_add,
                                                  "addf": self.manage_bw_add,
                                                  "store": self.manage_store,
                                                  "or": self.manage_bw_add,
                                                  "xor": self.manage_bw_add,
                                                  "and": self.manage_bw_add,
                                                  "ror": self.manage_ror,
                                                  "jmpEq": self.manage_jump,
                                                  "jmpLE": self.manage_jump,
                                                  "halt": self.manage_halt
                                                }

    def compile(self, text_file) -> List[int]:
        with open(text_file, 'r') as f:
            text = f.read()


        # Remove block comments (/* */)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    
        # Remove line comments (// to end of line)
        text = re.sub(r'//.*', '', text)
    
        # Remove whitespaces between a colon (:) and the next character
        text = re.sub(r':\s+', ':', text)
        # Remove trailing whitespaces at the end of each line (before \n)
        text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)

        # Remove empty lines or lines with only whitespace
        text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)
        # Optionally remove leftover newlines from empty lines
        text = re.sub(r'\n+', '\n', text)

        #Remove leading whitespaces at the start of each line
        text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)

        label_dict: Dict[str, int] = {}
        lines = text.splitlines()  # Split the text into lines


        replaced_lines: List[str] = []
        for i, line in enumerate(lines):
            match = re.match(r'^([^:]+):\s*(.*)', line)
            if match:
                key = match.group(1).strip()  # Group 1: Before the colon
                value = match.group(2).strip()  # Group 2: After the colon
                label_dict[key] = i  # Store in dictionary
            else:
                value = line
            replaced_lines.append(value)



        self.label_dictionary = label_dict
        output: List[int] = []

        for line in replaced_lines:
            line = line.strip()
            instruction = line.split(' ')
            output = output + self._instructions[instruction[0]](instruction)

        return output
    
    ## SECTION OF MANAGING INDIVIDUAL FUNCTIONS
    def manage_halt(self, instruction):
        # C0, 00
        return [192, 00]

    def manage_bw_add(self, instruction):
        operand = self.bw_operand_vals[instruction[0]]

        registers = instruction[1].split(",")
        r = int(registers[0][1], 16)
        s = int(registers[1][1], 16)
        t = int(registers[2][1], 16)
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
        
        #Check for labels:
        if info[1] in self.label_dictionary:
            info[1] = hex(self.label_dictionary[info[1]]*2)[2:]
        
        return [op*16+int(info[0][1], 16), int(info[1], 16)]
    
    def manage_store(self, instruction):
        info = instruction[1].split(",")
        if len(info[1]) == 3:
            return [14*16, int(info[0], 16)*16 + int(info[1][1], 16)]
        
        return [3*16 + int(info[0][1], 16), int(info[1][1:3], 16)]
    
    def manage_load(self, instruction):
        info = instruction[1:]

        #D  
        if len(info[1]) == 4 and '[R' in info[1]:
            return [13*16, int(info[0][1], 16)*16 + int(info[1][2], 16)]
        
        #2
        if not '[' in info[1]:
            if info[1] in self.label_dictionary:
                info[1] = hex(self.label_dictionary[ info[1] ] * 2)[2:]
            
            return [32 + int(info[0][1], 16), int(info[1], 16)]
        
        #1
        if info[1][1:-1] in self.label_dictionary:
            info[1] = hex(self.label_dictionary[ info[1][1:-1] ] * 2)[2:]
            info[1] = "[" + info[1] + "]"
        print(instruction)
        return [16 + int(info[0][1], 16), int(info[1][1:3], 16)] 
