# Library's
import tkinter as tk
from typing import *


class restrictedEntry(tk.Entry):
    """
    Entry object which restricts its input to given type
    """
    def __init__(self, restriction: type, **kwargs) -> None:
        """
        Constructor
        :param restriction: Type which the entry will restrict itself too
        :param kwargs: Other args which will be given to the tk.Entry
        """
        self.__var = tk.StringVar()
        self.__var.trace('w', self.__checkRestriction)
        super().__init__(textvariable=self.__var, **kwargs)
        self.__old_value = ''
        self.__restriction = restriction
        self.set, self.get = self.__var.set, self.__var.get

    def __checkRestriction(self, *args) -> None:
        """
        Function that will check its given input
        :param args: Incoming values, which are not needed
        """
        try:
            self.__old_value = str(self.__restriction(self.get()))
        except ValueError:
            if self.get() == "":
                self.__old_value = ""
            elif self.__restriction in (int, float) and self.get() == "-":
                pass
            else:
                self.set(self.__old_value)


class checkboxEntry(tk.Frame):
    """
    Entry object with a checkbox in for selecting output
    """
    def __init__(self, checkbox_text: str, entry_var_type: type, **kwargs) -> None:
        """
        Constructor
        :param checkbox_text: Text which is beside checkbox
        :param entry_var_type: Type of data the Entry box restricts itself too
        :param kwargs: Other args which will be given to the tk.Frame
        """
        super().__init__(**kwargs)
        self.__var = tk.IntVar()
        self.__var.trace('w', self.__entryBehaviour)
        tk.Checkbutton(self, text=checkbox_text, variable=self.__var, onvalue=1, offvalue=0).grid(column=0)
        self.__entry = restrictedEntry(entry_var_type, master=self, width=kwargs.get("width", None),
                                       state=kwargs.get("state", tk.DISABLED))
        self.__entry.grid(row=0, column=1)
        self.set = self.__entry.set
        self.__old_value = ""

    def get(self) -> None:
        """
        Function for returning the data
        NOTE: When checkbox is not selected will return None
        :return: Value of Entry or None
        """
        if not self.__var.get():
            return None
        return self.__entry.get()

    def __entryBehaviour(self, *args) -> None:
        """
        Function that disables entry field when interacting with checkbox
        :param args: Incoming values, which are not needed
        """
        if self.__var.get():
            self.__entry.set(self.__old_value)
            self.__entry.configure(state=tk.NORMAL)
        else:
            self.__old_value = self.__entry.get()
            self.__entry.set("")
            self.__entry.configure(state=tk.DISABLED)


class selectionEntry(tk.OptionMenu):
    """
    Selection Entry for selecting only given options
    """
    def __init__(self, menu_options: list, show_option: str = None, **kwargs):
        """
        Constructor
        :param menu_options: List of items where user can choose from
        :param show_option: String which is first displayed on selectionEntry
        :param kwargs: Other args which will be given to the tk.OptionMenu
        """
        self.__var = tk.StringVar()
        self.__var.set(menu_options[0] if show_option is None else show_option)
        super().__init__(kwargs.pop("master", None), self.__var, *menu_options, **kwargs)
        self.set, self.get = self.__var.set, self.__var.get


class buttonEntry(tk.Frame):
    """
    Entry where the input of a user will be given callback when the button is pressed.
    """
    def __init__(self, entry_var_type: type, button_text: str, callback: Callable[[str], None], **kwargs):
        """
        Constructor
        :param entry_var_type: Type of data the Entry box restricts itself too
        :param button_text: Text which is put on the button
        :param callback: Function which is ran when button is pressed
        :param kwargs: Other args which will be given to the tk.Frame
        """
        super().__init__(**kwargs)
        self.__entry = restrictedEntry(entry_var_type, master=self, width=kwargs.get("width", None))
        self.__entry.grid(column=0)
        self.__callback = callback
        tk.Button(self, text=button_text, command=self.__callback).grid(row=0, column=1)
        self.set, self.get = self.__entry.set, self.__entry.get

