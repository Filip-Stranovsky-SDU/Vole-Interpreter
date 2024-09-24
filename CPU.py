class CPU:

    registers: list[int] = [0] * 16
    memory: list[int] = [0]*256
    pc: int = 0 #Program Counter
    is_running: bool = False

    def __init__(self, program):
        self.program = program

    
    def parse_instruction(self, memory_adress: int):
        pass


    def step(self):
        instruction = self.parse_instruction(self.pc)
        self.pc = self.pc + 2

        match(instruction[0]):
            case 1:
                pass



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
