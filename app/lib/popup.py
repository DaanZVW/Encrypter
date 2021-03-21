# Library's
import enum
import tkinter as tk
from tkinter import ttk


class popupWindow(tk.Toplevel):
    def __init__(self, title: str, information: str, return_to, function=None):
        super().__init__()
        self.title(title)
        tk.Label(self, text=information).pack(pady=5)

        self.__return_to = return_to
        self.__function = function
        self.after(10, self.__runFunction)  # Must be 1> otherwise widget wont be loaded

    def __runFunction(self) -> None:
        try:
            if self.__function is None:
                self.__return_to()
            else:
                self.__return_to(self.__function())
        finally:
            self.destroy()
            self.quit()


class progressbarSetting(enum.Enum):
    showOnly = 0
    showReturn = 1
    showButton = 2
    interact = 3


class progressbarStep(tk.Toplevel):
    def __init__(self, setting: progressbarSetting, maximum: int, title: str, info_loading: str):
        super().__init__()
        self.title(title)
        self.geometry("250x60")

        self.__maximum = maximum
        self.__function = None
        self.__return_to = None
        self.__setting = setting

        tk.Label(self, text=info_loading).pack(pady=5)
        self.__bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=220, mode="determinate", maximum=maximum)
        self.__bar.pack()

        self.after(1, self.runFunction)
        self.step = self.__bar.step

    def setFunctions(self, function, return_to=None) -> None:
        self.__function = function
        self.__return_to = return_to

    def runFunction(self) -> None:
        try:
            if self.__setting is progressbarSetting.showOnly:
                self.__function()
            elif self.__setting is progressbarSetting.showReturn:
                self.__return_to(self.__function())
        finally:
            self.destroy()
            self.quit()
