import tkinter as Tk
import CPU
from typing import List

class App:

    #root: Tk.Tk = Tk.Tk()
    canvas: Tk.Canvas = Tk.Canvas(width=800, height=600, name="canvas")

    memory_texts: list[Tk.Entry] = []
    register_texts: list[Tk.Entry] = []

    last_text_changed: Tk.Text = None

    run_button: Tk.Button
    step_button: Tk.Button

    allowed_characters = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                          'A', 'B', 'C', 'D', 'E', 'F',
                          'a', 'b', 'c', 'd', 'e', 'f'}

    def __init__(self) -> None:
        self.cpu: CPU = CPU.CPU(self)

        self.create_ui()
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.mainloop()

    def create_memory_entries(self) -> None:
        for j in range(0, 16):
            for i in range(0, 16):
                new_text = Tk.Text(self.canvas, width=2, height=1, name=f"py_text_m{i + 16*j}")
                new_text.bind("<Button-1>", self.click)
                new_text.place(x=10+i*25, y=10+j*20)
                
                self.memory_texts.append(new_text)
                
                new_text.insert("1.0", f"{hex(j)[2:]}{hex(i)[2:]}")

    def create_register_entries(self) -> None:
        for i in range(0, 16):
            new_text = Tk.Text(self.canvas, width=2, height=1, name=f"py_text_r{i}")
            new_text.bind("<Button-1>", self.click)
            
            new_text.place(x=450, y=10+i*20)

            self.register_texts.append(new_text)

            new_text.insert("1.0", f"r{hex(i)[2:]}")
            


    def create_ui(self) -> None:
        self.create_register_entries()
        self.create_memory_entries()        

        self.run_button = Tk.Button(text="run", command=self.cpu.start_cpu_run)
        self.run_button.place(x=200, y=400)
        self.run_button = Tk.Button(text="step", command=self.cpu.step)
        self.run_button.place(x=200, y=420)
        


    def click(self, event: Tk.Event) -> None:
        if self.last_text_changed != None and self.last_text_changed._name != "canvas":
            self.check_last_change()
        self.last_text_changed = event.widget

    def check_last_change(self) -> None:
        name: str = self.last_text_changed._name
        value: str = self.last_text_changed.get("1.0", Tk.END)
        value = value.strip()[-2:]
        print(value)
        try:
            value_i = int(value, 16)
            if value_i > 255:
                raise ValueError
        except ValueError:
            self.last_text_changed.delete("1.0", Tk.END)
            if name[8] == "m":
                val =  self.cpu.memory[int(name[9:])]
            if name[8] == "r":
                val = self.cpu.registers[int(name[9:])]
            print(val)
            self.last_text_changed.insert("1.0", hex(val)[2:])
            return
        if len(value) == 1:
            self.last_text_changed.insert("1.0", "0")

        if name[8] == "m":
            self.cpu.memory[int(name[9:])] = value_i
        if name[8] == "r":
            self.cpu.registers[int(name[9:])] = value_i
        
        



    def change_memory_ui_val(self, address):
        new_val = hex(self.cpu.memory[address])[2:]
        self.memory_texts[address].delete("1.0", Tk.END)
        self.memory_texts[address].insert("1.0", new_val)

    def change_register_ui_val(self, address):
        new_val = hex(self.cpu.memory[address])[2:]
        self.register_texts[address].delete("1.0", Tk.END)
        self.register_texts[address].insert("1.0", new_val)

def main():
    app = App()


if __name__ == "__main__":
    main()
