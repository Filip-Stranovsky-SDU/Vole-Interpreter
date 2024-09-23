import tkinter as Tk
import CPU


class App:
    def __init__(self):
        self.canvas = Tk.Canvas(width=800, height=600)

        self.memory_entries = []
        self.register_entries = []

        self.create_ui()
        
        self.cpu = CPU.CPU()

        self.canvas.mainloop()

    def create_memory_entries(self):
        for i in range(0, 16):
            for j in range(0, 16):
                new_e = Tk.Entry(width=2)
                new_e.insert(0, f"{hex(j)[2:]}{hex(i)[2:]}")
                new_e.place(x=i*20, y=j*20)
                self.memory_entries.append(new_e)

    def create_register_entries(self):
        for i in range(0, 16):
            new_e = Tk.Entry(width=2)
            new_e.insert(0, f"r{hex(i)[2:]}")
            new_e.place(x=400, y=i*20)
            self.register_entries.append(new_e)

    def create_ui(self):
        self.create_register_entries()
        self.create_memory_entries()
def main():
    app = App()


if __name__ == "__main__":
    main()
