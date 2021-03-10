import tkinter as tk
from app.lib.gui import gui

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Encrypter")
    root.iconbitmap('res/gui/encrypter-logo.ico')
    gui_class = gui(master=root)
    gui_class.mainloop()




