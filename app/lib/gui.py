# Library's
import tkinter as tk
from copy import deepcopy
import tkinter.scrolledtext, tkinter.filedialog, tkinter.simpledialog

# Src files
import src.encrypter as encrypter
import src.exceptions as exceptions
import app.lib.modelGui as modelGui

# GUI files
import app.lib.TkMod as TkMod

# Language helper
import app.languages.config.languageHelper as languageHelper


class gui(tk.Frame):
    """
    Class for making a encrypter gui
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # =========
        # Variables
        # =========
        self.__model = encrypter.encrypter()
        self.__model.setDirectoryPath(self.__model.enviroment_home + "models/")

        self.__lang_helper = languageHelper.languageHelper()
        try:
            self.__lang_data = self.__lang_helper.getLanguage()
        except exceptions.LanguageNotFound:
            self.__lang_data = self.__lang_helper.getLanguage("english.json")
        self.__json_call_error = False

        # ============
        # Button Panel
        # ============
        button_panel_width = 20
        button_panel_height = 100
        button_group_pady = 10

        self.__button_panel = tk.Frame(self, width=button_panel_width, height=button_panel_height)
        self.__bp_home_buttons = tk.Frame(self.__button_panel)
        self.__bp_widget_buttons = tk.Frame(self.__button_panel, pady=button_group_pady)

        TkMod.selectionEntry(self.__lang_helper.found_languages + [self.__langCall("button", "new_lang")],
                             self.__langCall("language"), master=self.__bp_home_buttons,
                             command=self.__reloadLanguage).grid(row=0, sticky="ew")

        self.__bp_modes = list(map(lambda mode: self.__langCall("mode", mode, "name"), self.__lang_data["mode"].keys()))
        TkMod.selectionEntry(self.__bp_modes, master=self.__bp_home_buttons,
                             command=self.__selectMode).grid(row=1, sticky="ew")

        tk.Button(self.__bp_home_buttons, text=self.__langCall("button", "exit"), command=self.__exit,
                  width=button_panel_width).grid(row=2, sticky="ew")

        # ================
        # Encrypting panel
        # ================
        # Panel
        self.__encypting_panel = tk.Frame(self, padx=5, pady=5)

        tk.Label(self.__encypting_panel, text=self.__langCall("mode", "encrypt", "encrypt_field", "top_text")).pack()
        self.__ep_encrypt_field = tkinter.scrolledtext.ScrolledText(self.__encypting_panel, height=5, width=50)
        self.__ep_encrypt_field.pack()

        tk.Label(self.__encypting_panel, text=self.__langCall("mode", "encrypt", "decrypt_field", "top_text")).pack()
        self.__ep_decrypt_field = tkinter.scrolledtext.ScrolledText(self.__encypting_panel, height=5, width=50)
        self.__ep_decrypt_field.pack()

        # Buttons
        self.__ep_widget_buttons = tk.Frame(self.__bp_widget_buttons)
        tk.Button(self.__ep_widget_buttons, text=self.__langCall("mode", "encrypt", "button", "encrypt"),
                  command=self.__encrypt, width=button_panel_width).grid(row=0)
        tk.Button(self.__ep_widget_buttons, text=self.__langCall("mode", "encrypt", "button", "decrypt"),
                  command=self.__decrypt, width=button_panel_width).grid(row=1)
        tk.Button(self.__ep_widget_buttons, text=self.__langCall("mode", "encrypt", "button", "switch"),
                  command=self.__switchEncryptFields, width=button_panel_width).grid(row=2)
        tk.Button(self.__ep_widget_buttons, text=self.__langCall("mode", "encrypt", "button", "clear"),
                  command=self.__clearEncryptFields, width=button_panel_width).grid(row=3)

        # ===============
        # Configure panel
        # ===============
        # Panel
        self.__configure_panel = tk.Frame(self, padx=5)

        self.__configure_model = modelGui.modelGui()
        self.__cp_model_info = tkinter.scrolledtext.ScrolledText(self.__configure_panel,
                                                                 height=15, width=50, state=tk.DISABLED)
        self.__cp_model_info.grid(row=0, column=1, sticky="n")

        # Buttons
        self.__cp_widget_buttons = tk.Frame(self.__bp_widget_buttons)

        model_names = list(map(lambda model: model.name, self.__model.getModelsFromDirectory()))
        self.__cp_model_select = TkMod.selectionEntry(model_names, master=self.__cp_widget_buttons,
                                                      command=self.__loadModelGui)
        self.__cp_model_select.grid(sticky="ew")

        tk.Button(self.__cp_widget_buttons, text=self.__langCall("mode", "configure", "button", "append"),
                  width=button_panel_width, command=self.__appendModel).grid(row=1)
        tk.Button(self.__cp_widget_buttons, text=self.__langCall("mode", "configure", "button", "clear"),
                  width=button_panel_width, command=self.__clearModel).grid(row=2)
        tk.Button(self.__cp_widget_buttons, text=self.__langCall("mode", "configure", "button", "import", "name"),
                  width=button_panel_width, command=self.__importModel).grid(row=3)
        tk.Button(self.__cp_widget_buttons, text=self.__langCall("mode", "configure", "button", "export", "name"),
                  width=button_panel_width, command=self.__exportModel).grid(row=4)

        # =================
        # Advanced settings
        # =================
        self.__advanced_panel = tk.Frame(self, padx=5)
        tk.Button(self.__advanced_panel, text="klik dan", command=self.__test).pack()

        # =============
        # Panel packing
        # =============
        self.__bp_home_buttons.grid(row=0, column=0)

        self.__bp_widget_buttons.grid(row=1, sticky="ew")
        self.__button_panel.grid(row=0, sticky="ns")

        self.__widget_grid_settings = {"row": 0, "column": 1, "sticky": "ns"}

        self.pack()

        # ===============
        # Final functions
        # ===============
        self.__selectMode(self.__bp_modes[0])
        self.__loadModelGui(model_names[0])
        self.__updateModelInfo()

    # =============
    # GUI functions
    # =============
    # Language functions
    def __langCall(self, *args: str) -> str:
        widget_text = self.__lang_data
        try:
            for i in args:
                widget_text = widget_text[i]
            return str(widget_text)
        except (KeyError, TypeError):
            if self.__json_call_error:
                raise exceptions.TextNotFoundLanguage(*args)
            return str(".".join(args))

    # Entry fields functions
    def __setEntryField(self, entry_field: tk, text: str, end_state: tk = tk.NORMAL) -> None:
        entry_field.configure(state=tk.NORMAL)
        entry_field.delete(1.0, tk.END)
        entry_field.insert(1.0, text)
        entry_field.configure(state=end_state)

    def __getEntryField(self, entry_field: tk) -> str:
        return "\n".join(entry_field.get(1.0, tk.END).splitlines())

    # Home buttons
    def __reloadLanguage(self, language: str) -> None:
        if self.__lang_data["language"] == language:
            return

        if language not in self.__lang_helper.found_languages:
            language = tkinter.simpledialog.askstring(title="Give new language",
                                                      prompt="This may take a while...")
            if language is None:
                return

        self.__lang_helper.getLanguage(language)
        tmp_model = self.__model
        self.destroy()
        self.__init__()
        self.__model = tmp_model
        self.__updateModelInfo()

    def __selectMode(self, mode: str) -> None:
        self.__encypting_panel.grid_forget()
        self.__ep_widget_buttons.pack_forget()
        self.__configure_panel.grid_forget()
        self.__cp_widget_buttons.pack_forget()
        self.__advanced_panel.pack_forget()

        if mode is self.__bp_modes[0]:
            self.__configure_panel.grid(self.__widget_grid_settings)
            self.__cp_widget_buttons.pack()
        elif mode is self.__bp_modes[1]:
            self.__encypting_panel.grid(self.__widget_grid_settings)
            self.__ep_widget_buttons.pack()
        elif mode is self.__bp_modes[3]:
            self.__advanced_panel.grid(self.__widget_grid_settings)

    def __exit(self) -> None:
        exit()

    # ================
    # Widget functions
    # ================
    # Encrypt
    def __encrypt(self) -> None:
        input_text = self.__getEntryField(self.__ep_encrypt_field)
        if not input_text:
            encrypted_text = self.__langCall("mode", "encrypt", "encrypt_field", "no_fill")
        else:
            encrypted_text = self.__model.encrypt(input_text)
        self.__setEntryField(self.__ep_decrypt_field, encrypted_text)

    def __decrypt(self) -> None:
        input_text = self.__getEntryField(self.__ep_decrypt_field)
        if not input_text:
            decrypted_text = self.__langCall("mode", "encrypt", "decrypt_field", "no_fill")
        else:
            decrypted_text = self.__model.decrypt(input_text)
        self.__setEntryField(self.__ep_encrypt_field, decrypted_text)

    def __switchEncryptFields(self) -> None:
        tmp_text = self.__getEntryField(self.__ep_encrypt_field)
        self.__setEntryField(self.__ep_encrypt_field, self.__getEntryField(self.__ep_decrypt_field))
        self.__setEntryField(self.__ep_decrypt_field, tmp_text)

    def __clearEncryptFields(self) -> None:
        self.__setEntryField(self.__ep_encrypt_field, "")
        self.__setEntryField(self.__ep_decrypt_field, "")

    # Configure model
    def __loadModelGui(self, model_type: str) -> None:
        new_model_gui = self.__model.getGUIFromDirectory(model_type, master=self.__configure_panel)
        self.__configure_model.destroy()
        self.__configure_model = new_model_gui
        self.__configure_model.grid(row=0, padx=5, pady=5, sticky="nw")

    def __updateModelInfo(self) -> None:
        self.__setEntryField(self.__cp_model_info, str(self.__model), tk.DISABLED)

    def __appendModel(self) -> None:
        selected_model = tuple(filter(lambda module: module.name == self.__cp_model_select.get(),
                                      self.__model.getModelsFromDirectory()))
        selected_model[0].setAttributes(self.__configure_model.getResults())
        self.__model.appendModel(selected_model[0])
        self.__updateModelInfo()

    def __clearModel(self) -> None:
        self.__model = encrypter.encrypter()
        self.__updateModelInfo()

    def __importModel(self) -> None:
        filename = tkinter.filedialog.askopenfilename(initialdir=self.__model.enviroment_home,
                                                      title=self.__langCall("mode", "configure", "button", "import",
                                                                            "window_title"))
        if not filename:
            return
        self.__model.importModel(filename)
        self.__updateModelInfo()

    def __exportModel(self) -> None:
        file_extensions = [('Model Files', '*.model'), ('Text Files', '*.txt')]
        filename = tkinter.filedialog.asksaveasfile(initialdir=self.__model.enviroment_home,
                                                    title=self.__langCall("mode", "configure", "button", "export",
                                                                          "window_title"),
                                                    filetypes=file_extensions, defaultextension=file_extensions)
        try:
            self.__model.exportModel(filename.name)
        except AttributeError:
            raise exceptions.ExportModelError("Filename not given", "Select a file")


    def __test(self):
        john = tkinter.simpledialog.askstring(title="Dit is een test", prompt="Testo?")
        print(john)
