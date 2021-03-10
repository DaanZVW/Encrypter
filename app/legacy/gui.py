# Library's
import tkinter as tk
from tkinter import scrolledtext, filedialog

# Src files
from src.model import model
from src.encrypter import encrypter
from app.lib.modelGui import modelGui


class gui(tk.Frame):
    """
    GUI class for the encrypter
    """
    def __init__(self, master: tk.Frame = None, **kwargs) -> None:
        """
        Constructor
        :param master: Frame where it will be put on to
        :param kwargs: Other args which will be given to the tk.Frame
        """
        # Main panels
        super().__init__(master, **kwargs)
        self.__buttonpanel = tk.Frame(self, padx=5, pady=5, width=200)
        self.__encryptpanel = tk.Frame(self, padx=5, pady=5)
        self.__modelpanel = tk.Frame(self, padx=5, pady=5)
        self.__makemodelpanel = tk.Frame(self, padx=5, pady=5)
        self.__makemodelselect = tk.Frame(self.__makemodelpanel)
        self.__makemodelmake = tk.Frame(self.__makemodelpanel, padx=15)

        # Input field
        tk.Label(self.__encryptpanel, text="Fill in your data").grid(row=0, column=0, columnspan=6)
        self.__input_text = scrolledtext.ScrolledText(self.__encryptpanel, height=5, width=50)
        self.__input_text.grid(row=1, column=0, columnspan=6)

        # Output field
        tk.Label(self.__encryptpanel, text="Output of model").grid(row=2, column=0, columnspan=6)
        self.__output_text = scrolledtext.ScrolledText(self.__encryptpanel, height=5, width=50, state=tk.DISABLED)
        self.__output_text.grid(row=3, column=0, columnspan=6)

        # Buttons
        self.__make_model_button = tk.Button(
            self.__encryptpanel, text="Select Model Directory", command=self.__selectModelDir)
        self.__make_model_button.grid(row=4, column=0)
        self.__make_model_button = tk.Button(
            self.__encryptpanel, text="Get model", command=self.__importModel)
        self.__make_model_button.grid(row=4, column=1)
        self.__copy_button = tk.Button(
            self.__encryptpanel, text="Copy output", command=self.__copyOutput)
        self.__copy_button.grid(row=4, column=2)
        self.__paste_button = tk.Button(
            self.__encryptpanel, text="Paste input", command=self.__pasteInput)
        self.__paste_button.grid(row=4, column=3)
        self.__encrypt_button = tk.Button(
            self.__encryptpanel, text="Encrypt", command=self.__encrypt)
        self.__encrypt_button.grid(row=4, column=4)
        self.__decrypt_button = tk.Button(
            self.__encryptpanel, text="Decrypt", command=self.__decrypt)
        self.__decrypt_button.grid(row=4, column=5)

        # Modelpanel
        self.__model_text = scrolledtext.ScrolledText(self.__modelpanel, height=15, width=50, state=tk.DISABLED)
        self.__model_text.pack()

        # Makemodelpanel
        default_text = "Select a model directory..."
        self.__model_make_var = tk.StringVar()
        self.__model_make_var.set(default_text)
        self.__model_make = tk.OptionMenu(
            self.__makemodelselect, self.__model_make_var, default_text)
        self.__model_make.grid(row=0, column=0)

        self.__model_make_load = tk.Button(
            self.__makemodelselect, text="Load selected model", command=self.__loadModelForMake)
        self.__model_make_load.grid(row=1, column=0)
        self.__model_make_append = tk.Button(
            self.__makemodelselect, text="Append to model", command=self.__appendModelForMake)
        self.__model_make_append.grid(row=2, column=0)
        self.__model_make_export = tk.Button(
            self.__makemodelselect, text="Export model", command=self.__exportModelFromMake)
        self.__model_make_export.grid(row=3, column=0)

        self.__model_make_info = tk.Frame(
            self.__makemodelmake, padx=15)
        self.__model_make_info.pack()
        self.__model_make_info_model = modelGui()

        # Pack panels
        self.__makemodelselect.grid(row=0, column=0)
        self.__makemodelmake.grid(row=0, column=1)

        self.__buttonpanel.grid(row=0, column=0, rowspan=2)
        self.__encryptpanel.grid(row=0, column=1)
        self.__modelpanel.grid(row=0, column=2)
        self.__makemodelpanel.grid(row=1, column=1)
        self.pack()

        # Variables
        self.__model = encrypter()

        # Update functions
        self.__updateModel()

    def setEncryptModel(self, module: model) -> None:
        """
        Set the encrypting model
        :param module: Model which it will set too
        """
        self.__model.appendModel(module)
        self.__updateModel()

    def __updateOutputField(self, text: str) -> None:
        """
        Update the output field with given text
        :param text: Text it will be set too
        """
        self.__output_text.configure(state=tk.NORMAL)
        self.__output_text.delete(1.0, tk.END)
        self.__output_text.insert(1.0, text)
        self.__output_text.configure(state=tk.DISABLED)

    def __encrypt(self) -> None:
        """
        Encrypt whats in the input field
        """
        text = "\n".join(str(self.__input_text.get(1.0, tk.END)).splitlines())
        if not text:
            text = "Nothing to encrypt"
        self.__updateOutputField(self.__model.encrypt(text))

    def __decrypt(self) -> None:
        """
        Decrypt whats in the input field
        """
        text = "\n".join(str(self.__input_text.get(1.0, tk.END)).splitlines())
        if not text:
            text = "Nothing to decrypt"
        self.__updateOutputField(self.__model.decrypt(text))

    def __copyOutput(self) -> None:
        """
        Copy the output field in clipboard
        """
        self.clipboard_clear()
        self.clipboard_append("\n".join(str(self.__output_text.get(1.0, tk.END)).splitlines()))

    def __pasteInput(self) -> None:
        """
        Paste clipboard in input field
        """
        clipboard = self.clipboard_get()
        self.__input_text.delete(1.0, tk.END)
        self.__input_text.insert(1.0, clipboard)

    def __importModel(self) -> None:
        """
        Import model from file
        """
        filename = str(filedialog.askopenfilename(
            initialdir=self.__model.enviroment_home, title="Select model file"))
        if not filename:
            return
        self.__model.importModel(filename)
        self.__updateModel()

    def __updateModel(self) -> None:
        """
        Update the model information
        """
        self.__model_text.configure(state=tk.NORMAL)
        self.__model_text.delete(1.0, tk.END)
        self.__model_text.insert(1.0, "\n".join(str(self.__model).splitlines()))
        self.__model_text.configure(state=tk.DISABLED)

    def __updateModelSelect(self) -> None:
        """
        Update the selection menu
        """
        model_names = list(map(lambda model: model.name, self.__model.getModelsFromDirectory()))
        self.__model_make_var.set('Select Model')
        self.__model_make["menu"].delete(0, tk.END)
        for name in model_names:
            self.__model_make["menu"].add_command(label=name, command=tk._setit(self.__model_make_var, name))

    def __selectModelDir(self) -> None:
        """
        Select the directory where models are used
        """
        dir_path = str(filedialog.askdirectory(
            initialdir=self.__model.enviroment_home, title="Select the model directory")) + "/"
        if dir_path == "/":
            return
        self.__model.setDirectoryPath(dir_path)
        self.__updateModelSelect()

    def __loadModelForMake(self) -> None:
        """
        Load the model for making
        """
        items = []
        for index in range(self.__model_make["menu"].index("end")+1):
            items.append(self.__model_make["menu"].entrycget(index, "label"))

        gui_index = items.index(self.__model_make_var.get())
        self.__model_make_info_model.destroy()
        self.__model_make_info_model = self.__model.getGUIFromDirectory(items[gui_index], master=self.__model_make_info)
        self.__model_make_info_model.grid(sticky="w")

    def __appendModelForMake(self) -> None:
        """
        Append made model to internal model
        """
        for module in self.__model.getModelsFromDirectory():
            if module.name == self.__model_make_var.get():
                module.setAttributes(self.__model_make_info_model.getResults())
                self.__model.appendModel(module)
                self.__updateModel()
                break

    def __exportModelFromMake(self) -> None:
        """
        Export current made model to a file
        """
        file_extensions = [('Model Files', '*.model'), ('Text Files', '*.txt')]
        filename = filedialog.asksaveasfile(initialdir=self.__model.enviroment_home, title="Make new export file",
                                            filetypes=file_extensions, defaultextension=file_extensions)
        self.__model.exportModel(filename.name)
