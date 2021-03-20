from src.model import model
from typing import Tuple


# Default errors
class DefaultError(Exception):
    def __init__(self, error: str, hint: str = ""):
        error = f"\nError: {error}"
        hint = f"\nHint : {hint}" if hint else hint
        message = f"\n{error}{hint}"
        super().__init__(message)


class DefaultModuleError(Exception):
    def __init__(self, module: model, error: str, hint: str = ""):
        model_information = f"\nModel: {module}"
        error = f"\nError: {error}"
        hint = f"\nHint : {hint}" if hint else hint
        message = f"\n{model_information}{error}{hint}"
        super().__init__(message)


# Encrypt setting error
class EncryptSettingError(DefaultModuleError):
    def __init__(self, module: model):
        super().__init__(module, f"Module only accepts {module.setting} data.")


# Random module error
class RandomModuleError(DefaultModuleError):
    def __init__(self, module: model):
        super().__init__(module, f"Random module not found!", f"Give the model an working RandomHelper class")


# Importing exporting errors
class DirNotFound(DefaultError):
    def __init__(self, path: str, hint: str = ""):
        super().__init__(f'"{path}" directory could not be found!', hint)


class ExportModelError(DefaultError):
    def __init__(self, error: str, hint: str = ""):
        super().__init__(error, hint)


class ImportModelError(DefaultError):
    def __init__(self, error: str, hint: str = ""):
        super().__init__(error, hint)


# GUI
class EntryNotConvertible(DefaultError):
    def __init__(self, setting_name: str, input: str, var_type: type):
        super().__init__(f'Setting "{setting_name}" can not convert "{input}" to type {var_type}.',
                         "Make sure the input is compliant with the type.")


class EntryNotFilled(DefaultError):
    def __init__(self, setting_name: str):
        super().__init__(f'Setting "{setting_name}" is not filled.', "Fill setting to proceed")


class TextNotFoundLanguage(DefaultError):
    def __init__(self, *args: str):
        language_error = ".".join(args)
        super().__init__(f'Text for "{language_error}" could not be found')


# Language
class LanguageNotFound(DefaultError):
    def __init__(self, language_name: str):
        super().__init__(f'Language "{language_name}" could not be found')


# Translating Error
class TranslatingFailedLibrary(DefaultError):
    def __init__(self):
        super().__init__("Translating was unsuccessful because an error in the translating library")


class TranslatingFailed(DefaultError):
    def __init__(self):
        super().__init__("Translating was unsuccessful because the output was empty")
