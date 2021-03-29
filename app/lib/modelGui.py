# Library's
import tkinter as tk
from enum import Enum

# Src files
import app.lib.TkMod as TkMod
from src.exceptions import EntryNotConvertible, EntryNotFilled


class modelGui(tk.Frame):
    """
    Class filling in attributes for a given model
    """
    def __init__(self, **kwargs) -> None:
        """
        Constructor
        :param kwargs: Other args which will be given to the tk.Entry
        """
        super().__init__(**kwargs)
        self.__current_row = 0
        self.__entry_inputs = list()

    def configure_gui(self, name: str, setting: Enum) -> None:
        """
        Display the information of the model
        :param name: Name of the model
        :param setting: Encrypt setting which the model uses
        """
        tk.Label(self, text="Name").grid(row=self.__current_row, column=0, sticky="w")
        tk.Label(self, text=name).grid(row=self.__current_row, column=1, sticky="w")
        self.__current_row += 1
        tk.Label(self, text="Setting").grid(row=self.__current_row, column=0, sticky="w")
        tk.Label(self, text=str(setting)).grid(row=self.__current_row, column=1, sticky="w")
        self.__current_row += 1

    def addSetting(self, setting_name: str, entry_object: tk, var_type: type) -> None:
        """
        Abstract function which adds an object to the menu
        :param setting_name: Name of the setting
        :param entry_object: Object which is added internally
        :param var_type: Type the variable is converted to
        """
        tk.Label(self, text=setting_name).grid(row=self.__current_row, column=0, sticky="w")
        entry_object.grid(row=self.__current_row, column=1, sticky="w")
        self.__entry_inputs.append((setting_name, entry_object, var_type))
        self.__current_row += 1

    def addEntrySetting(self, setting_name: str, var_type: type = str, entry_var_type: type = None) -> None:
        """
        Display a given setting of the model
        :param setting_name: Name of the setting
        :param var_type: Type of variable which the entry value is converted too
        :param entry_var_type: Type of variable which the entry is restricted by
        """
        if entry_var_type is None:
            entry_var_type = var_type
        self.addSetting(setting_name, TkMod.restrictedEntry(entry_var_type, master=self), var_type)

    def addCheckboxSetting(self, setting_name: str, choice_name: str, var_type: type = str) -> None:
        """
        Display a given setting of the model with checkbox
        :param setting_name: Name of the setting
        :param choice_name: Text beside checkbox
        :param var_type: Type of variable which the entry value is converted too
        """
        self.addSetting(setting_name, TkMod.checkboxEntry(choice_name, var_type, master=self), var_type)

    def addSelectionSetting(self, setting_name: str, selection_list: list, var_type: type = str) -> None:
        """
        Display a selection of settings for a model
        :param setting_name: Name of the setting
        :param selection_list: List with selection for user to choose
        :param var_type: Type of variable which the entry value is converted too
        """
        self.addSetting(setting_name, TkMod.selectionEntry(selection_list, master=self), var_type)

    def addEnumSelectionSetting(self, setting_name: str, selection_list: list, var_type: type = str) -> None:
        """
        Display a selection of settings for a model with enums
        :param setting_name: Name of the setting
        :param selection_list: List with selection for user to choose
        :param var_type: Type of variable which the entry value is converted too
        """
        selection_list = list(map(lambda option: ".".join(option.split(".")[1:]), selection_list))
        self.addSelectionSetting(setting_name, selection_list, var_type)

    def getResults(self) -> list:
        """
        Returns all the model information in a list
        :return: List with all the information of the made model
        """
        entry_results = []
        for entry in self.__entry_inputs:
            try:
                # When widget gives back None
                if entry[1].get() is None:
                    continue
                # When widget gives back empty string
                if not entry[1].get():
                    raise EntryNotFilled(entry[0])
                # When var_type is an Enum class
                elif issubclass(entry[2], Enum):
                    entry_results.append(entry[2][entry[1].get()].value)
                # Otherwise get it normally
                else:
                    entry_results.append(entry[2](entry[1].get()))
            except ValueError:
                raise EntryNotConvertible(entry[0], entry[1].get(), entry[2])
        return entry_results

