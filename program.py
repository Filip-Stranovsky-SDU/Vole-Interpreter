import tkinter as Tk
import CPU
from typing import List

class App:

    root: Tk.Tk = Tk.Tk()
    canvas: Tk.Canvas = Tk.Canvas(root, width=800, height=600)

    memory_entries: list[Tk.Entry] = []
    memory_entries_svars: list[Tk.StringVar] = []

    register_entries: list[Tk.Entry] = []
    register_entries_svars: list[Tk.StringVar] = []

    run_button: Tk.Button

    def __init__(self) -> None:
        self.cpu: CPU = CPU.CPU(self)

        self.create_ui()
        self.canvas.mainloop()

    def create_memory_entries(self) -> None:
        for j in range(0, 16):
            for i in range(0, 16):
                new_svar = Tk.StringVar(name=f"PY_SVAR_M{i + 16*j}", master=self.canvas)
                new_svar.trace_add("write", self.check_entry_string_memory)

                new_e = Tk.Entry(width=3, textvariable=new_svar)
                new_e.place(x=i*25, y=j*20)

                self.memory_entries.append(new_e)
                self.memory_entries_svars.append(new_svar)

                new_svar.set(f"{hex(j)[2:]}{hex(i)[2:]}") #In the end because needs to append first so check can run

    def create_register_entries(self) -> None:
        for i in range(0, 16):
            new_svar = Tk.StringVar(name=f"PY_SVAR_R{i}", master=self.canvas)
            new_svar.trace_add("write", self.check_entry_string_registers)
            
            new_e = Tk.Entry(width=2, textvariable=new_svar)
            new_e.place(x=400, y=i*20)

            self.register_entries.append(new_e)
            self.register_entries_svars.append(new_svar)

            new_svar.set(f"r{hex(i)[2:]}") #In the end because needs to append first so check can run



    def create_ui(self) -> None:
        self.create_register_entries()
        self.create_memory_entries()

        self.run_button = Tk.Button(text="run", command=self.cpu.start_cpu_run)
        self.run_button.place(x=200, y=400)
        


    def check_entry_string_memory(self, var, index, mode) -> None:
        address: int = int(var[9:])
        svar: Tk.StringVar = self.memory_entries_svars[address]
    
        try: 
            temp: int = int(svar.get(), 16)
        except ValueError:
            svar.set(hex(self.cpu.memory[address])[2:])
            return
        
        if(temp > 255):
            svar.set(hex(self.cpu.memory[address])[2:])
            return
        
        self.cpu.memory[address] = temp
        

    def check_entry_string_registers(self, var, index, mode) -> None:
        address: int = int(var[9:])
        svar: Tk.StringVar = self.register_entries_svars[address]
    
        try: 
            temp: int = int(svar.get(), 16)
        except ValueError:
            svar.set(hex(self.cpu.registers[address])[2:])
            return
        
        if(temp > 255):
            svar.set(hex(self.cpu.registers[address])[2:])
            return
        
        self.cpu.registers[address] = temp

def main():
    app = App()


if __name__ == "__main__":
    main()
