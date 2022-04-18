# Library's
import os
import warnings
import importlib
from sys import platform
from copy import deepcopy
from functools import reduce
from typing import Callable, List, Tuple

# Src files
from src.model import model, encryptSettings
from src.exceptions import DirNotFound, ExportModelError, ImportModelError


class encrypter(model):
    """
    Interface class for all the models
    """
    def __init__(self) -> None:
        """
        Encrypter constructor
        """
        super().__init__("Encrypter", encryptSettings.allBase)
        self.__models = []

        self.directory_path = ""
        self.model_exceptions = ["template.py"]
        self.file_spacing = " "
        self.__file_encrypter = NotImplemented
        self.enviroment_home = str(os.environ["PYTHONPATH"].split(os.pathsep)[0]) + '/'
        if "win" in platform:
            self.enviroment_home = self.enviroment_home.replace("\\", "/")

    # Model
    def appendModel(self, model_t: model) -> bool:
        """
        Append a given model to execute model list
        :param model_t: Model which needs to be appended
        :return: Boolean
        """
        for model_t_internal in self.__models:
            if model_t.name == model_t_internal.name and not model_t_internal.checkRestriction(model_t.restrictions()):
                message = f"New {model_t.name} model settings doesnt match older {model_t_internal.name} model " \
                          f"settings, this may result in an unresolvable message when encrypted."
                warnings.warn(message)
        self.__models.append(model_t)
        return True

    def setFileEncrypter(self, model_t: model) -> bool:
        """
        Set the file encrypter to given model
        :param model_t: Model that encrypts and decrypts the file
        :return: If succeeded
        """
        self.__file_encrypter = model_t
        return True

    # Superclass functions
    def __internalEncrypt(self, text: str, function: Callable[[model, str], str], reverse: bool = False) -> str:
        """
        Encypt or Decrypt given text with function
        :param text: Text that needs encrypting or decrypting
        :param function: Lambda that calls encrypt or decrypt function
        :return: Encrypted or Decrypted text
        """
        new_text = str()

        for model_t in reversed(self.__models) if reverse else self.__models:
            if model_t.setting is encryptSettings.charBase:
                new_text = "".join(map(lambda char: function(model_t, char), text))

            if model_t.setting is encryptSettings.lineBase:
                new_text = "".join(map(lambda line: function(model_t, line), text.splitlines(keepends=True)))

            if model_t.setting in [encryptSettings.allBase, encryptSettings.lineOrAllBase]:
                new_text = function(model_t, text)

            text, new_text = new_text, str()

        return text

    def encrypt(self, text: str) -> str:
        """
        Encrypt text with internal model
        :param text: Text that needs encrypting
        :return: Encrypted text
        """
        return self.__internalEncrypt(text, lambda model_t, data: model_t.encrypt(data), False)

    def decrypt(self, text: str) -> str:
        """
        Decrypt text with internal model
        :param text: Text that needs decrypting
        :return: Decrypted text
        """
        return self.__internalEncrypt(text, lambda model_t, data: model_t.decrypt(data), True)

    # Export and import functions
    # Get models from directory
    def __getModelsPath(self) -> Tuple[str, List[str]]:
        """
        Internal function for getting paths to models of directory
        :return: Location of model, filename; though formatted for importlib
        """
        try:
            all_files = [f for f in os.listdir(self.directory_path) if os.path.isfile(f"{self.directory_path}{f}")]
        except FileNotFoundError:
            raise DirNotFound(self.directory_path, "Make sure the directory_path variable is set.")

        all_files = list(filter(lambda f: f not in self.model_exceptions, all_files))

        all_files = list(map(lambda f: ".".join(f.split(".")[:-1]), all_files))
        imp_dir = ".".join(self.directory_path.split("/"))
        return imp_dir, all_files

    def getModelsFromDirectory(self) -> List[model]:
        """
        Function for getting all the models from a given directory
        :return: The list with models
        """
        imp_dir, all_files = self.__getModelsPath()
        return list(map(lambda f: importlib.import_module(f"{imp_dir}{f}").getDefaultModel(), all_files))

    def getGUIFromDirectory(self, model_name: str, **kwargs):
        """
        Function for getting a gui of a model from a given directory
        :param model_name: Name of the model
        :param kwargs: Arguments the modelGui will be given
        :return: The GUI frame
        """
        imp_dir, all_files = self.__getModelsPath()
        model_names = self.getModelsFromDirectory()
        found_model = list(map(lambda model: model.name == model_name, model_names))
        if not max(found_model):
            raise ImportModelError(f'"{model_name}" Model does not exist', "Import the model to get access to it")

        gui_index = found_model.index(True)
        return importlib.import_module(f"{imp_dir}{all_files[gui_index]}").getModelGUI(**kwargs)

    # Working with paths
    def __stripEnvironment(self, filename: str) -> str:
        """
        Strip the environment variable of given filename to keep it abstract
        :param filename: Path of file
        :return: Path of file without environment variable
        """
        if self.enviroment_home in filename:
            filename = filename[len(self.enviroment_home):]
        return filename

    def setDirectoryPath(self, dirpath: str) -> None:
        """
        Set the internal directory_path
        :param dirpath: Path it will be set too
        """
        self.directory_path = self.__stripEnvironment(dirpath)

    def exportModel(self, filename: str) -> bool:
        """
        Export internal model to filename
        :param filename: Location where the model will be writen too
        :return: If succeeded
        """
        filename = self.__stripEnvironment(filename)

        dirs = "".join(filename.split("/")[:-1])
        if not os.path.exists(dirs):
            os.makedirs(dirs)

        module_attribute = list(map(lambda module: [module.name] + module.getAttributes(), self.__models))
        file_input = "\n".join(list(map(lambda module: self.file_spacing.join(module), module_attribute)))

        if self.__file_encrypter is not NotImplemented:
            file_input = self.__file_encrypter.encrypt(file_input)
        with open(filename, "w") as file:
            file.write(file_input)
        return True

    def importModel(self, filename: str) -> bool:
        """
        Import a model from a file
        :param filename: Location of model for importing
        :return: If succeeded
        """
        filename = self.__stripEnvironment(filename)

        if not os.path.exists(filename):
            raise ImportModelError(f'"{filename}" file not found!')

        self.__models.clear()

        model_directory = {module.name: module for module in self.getModelsFromDirectory()}

        with open(filename, "r") as file:
            file_output = file.read()

        if self.__file_encrypter is not NotImplemented:
            file_output = self.__file_encrypter.decrypt(file_output)

        for line in file_output.splitlines():
            model_information = line.split(self.file_spacing)
            if model_information[0] not in model_directory:
                raise ImportModelError(f'"{model_information[0]}" Model does not exist',
                                       "Import the model to get access to it")
            new_model = deepcopy(model_directory[model_information[0]])
            new_model.setAttributes(model_information[1:])
            self.appendModel(new_model)
        return True

    def __str__(self):
        if not self.__models:
            model_string = "None provided"
        else:
            model_string = str(reduce(lambda model1, model2: str(model1) + str(model2), self.__models))
        return f"Encrypter makes use of this model:\n" \
               f"----------------------------------\n" + \
               model_string
