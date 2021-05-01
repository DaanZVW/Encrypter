# Library's
import tkinter as tk
from tkinter import ttk

# Files
from app.lib.utils import multiFunc


class popupWindow(tk.Toplevel):
    def __init__(self, title: str, information: str, return_to: multiFunc, function: multiFunc = None) -> None:
        super().__init__()
        self.title(title)
        tk.Label(self, text=information).pack(pady=5)

        self.return_to = return_to
        self.function = function

    def __call__(self, *args, **kwargs):
        try:
            if self.function is None:
                self.return_to()
            else:
                self.return_to(self.function())
        finally:
            self.destroy()
            self.quit()


class progressbarStep(popupWindow):
    def __init__(self, title: str, info_loading: str, maximum: int, return_to: multiFunc, function: multiFunc) -> None:
        super().__init__(title, info_loading, return_to)
        self.geometry("250x60")

        self.__bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=220, mode="determinate", maximum=maximum)
        self.__bar.pack()

        function.functions.extend([lambda: self.__bar.step(1), lambda: self.update_idletasks()])
        self.function = function

        # Doing it after 50ms so the popupWindow can display itself
        self.after(50, self.__call__)

