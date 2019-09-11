import tkinter as tk

class Display(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Cruise Control Display")

        tk.Label(self, text="This is your first GUI").pack()

        button_frame = tk.Frame(self)
        button_frame.pack(padx=15, pady=(0, 15), anchor='e')

        tk.Button(button_frame, text='Run', default='active',
                  command=self.click_run).pack(side='right')
        tk.Button(button_frame, text='Exit',
                  command=self.click_exit).pack(side='right')

    def click_run(self):
        print("The user clicked 'Run'")

    def click_exit(self):
        print("The user clicked 'Exit'")
        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    window = Display(root)
    window.mainloop()