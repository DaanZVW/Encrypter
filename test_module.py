# Library's
import tkinter as tk

# Import GUI files
from app.lib.gui import gui

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Encrypter")
    root.iconbitmap('app/res/encrypter-logo.ico')
    gui_class = gui(master=root)
    gui_class.mainloop()

