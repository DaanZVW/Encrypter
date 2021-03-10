# Library's
import warnings
from enum import Enum
from typing import Callable, List

# Src files
from src.model import model, encryptSettings
from src.exceptions import EncryptSettingError

# Gui files
from app.legacy.gui import modelGui


def getDefaultModel():
    """
    This function will be used when importing models
    :return: Default model with default settings
    """
    return shift(shiftSettings.default)


def getModelGUI(**kwargs) -> modelGui:
    """
    Get the GUI for the shift module
    :param master: Frame to put it on
    """
    gui = modelGui(**kwargs)
    default_class = getDefaultModel()
    gui.configure_gui(default_class.name, default_class.setting)
    gui.addEnumSelectionSetting("Shift Setting", list(map(lambda setting: str(setting), shiftSettings)), shiftSettings)
    gui.addSetting("Shift amount", int)
    return gui


class shiftSettings(Enum):
    """
    Settings for ASCII shifting model
    """
    full = 255
    letters = 75
    lettersDigits = 85
    printable = 189
    default = full


class shift(model):
    """
    Model for shifting letters in ascii
    """

    def __init__(self, setting: shiftSettings) -> None:
        """
        Constructor
        :param setting: Setting which the model will be set too
        """
        super().__init__("Shift", encryptSettings.charBase)
        self.__shift_amount = 0
        self.__shift_setting = setting

        if setting in [shiftSettings.letters, shiftSettings.lettersDigits]:
            self.__char_begin, self.__char_end = 10, 122

        elif setting is shiftSettings.printable:
            self.__char_begin, self.__char_end = 10, 255

        else:
            self.__char_begin, self.__char_end = 0, 255

    # Functions for setting model
    def setShiftAmount(self, amount: int) -> None:
        """
        Set the shifting amount for every character
        :param amount: Amount which every character will be shifted
        """
        self.__shift_amount = amount

        if self.__shift_setting.value < abs(amount):
            warn_message = "Shift amount is more than selected range: 0 - {}".format(
                self.__shift_setting
            )
            warnings.warn(warn_message)

        elif self.__shift_setting.value / 2 < abs(amount) and self.__shift_setting != shiftSettings.full:
            optimized_number = self.__shift_setting.value - abs(amount)
            optimized_number *= -1 if abs(amount) == amount else 1
            warn_message = "Shift amount is not optimized, try shift_amount: {}".format(optimized_number)
            warnings.warn(warn_message)

    # Internal functions
    def __overflowCondition(self, char: int, shift_amount: int, function: Callable[[str], bool]) -> str:
        """
        Overflow function which keeps between begin and end. Only lowers shift_amount if function is true
        :param char: Char you want converted
        :param shift_amount: Amount shifted in ascii
        :param function: Lambda function which checks if a char is correct
        :return: New char
        """
        step = 1 if shift_amount > 0 else -1

        while shift_amount != 0:
            while True:
                char += step
                if char < self.__char_begin:
                    char += self.__char_end - self.__char_begin + 1
                elif char > self.__char_end:
                    char -= self.__char_end - self.__char_begin + 1

                if function(chr(char)):
                    break
            shift_amount -= step

        return chr(char)

    def __overflow(self, char: str, shift_amount: int) -> str:
        """
        Overflow function, uses itself when full ascii is used
        :param char: Char you want converted
        :param shift_amount: Amount shifted in ascii
        :return: New char
        """
        char = ord(char)

        if self.__shift_setting == shiftSettings.letters:
            return self.__overflowCondition(
                char, shift_amount, lambda char_t: char_t.isalpha() or char_t.isspace() or char_t == "\n"
            )

        elif self.__shift_setting == shiftSettings.lettersDigits:
            return self.__overflowCondition(
                char, shift_amount, lambda char_t: char_t.isalnum() or char_t.isspace() or char_t == "\n"
            )

        elif self.__shift_setting == shiftSettings.printable:
            return self.__overflowCondition(
                char, shift_amount, lambda char_t: char_t.isprintable() or char_t == "\n"
            )

        char += shift_amount

        while True:
            if char < self.__char_begin:
                char += self.__char_end - self.__char_begin
            elif char > self.__char_end:
                char -= self.__char_end - self.__char_begin
            else:
                return chr(char)

    # Model functions
    def encrypt(self, char: str) -> str:
        """
        Function which encrypts a given char
        :param char: Character you want converted
        :return: Encrypted character
        """
        if len(char) > 1:
            raise EncryptSettingError(self)
        return self.__overflow(char, self.__shift_amount)

    def decrypt(self, char: str) -> str:
        """
        Function which decrypts a given char
        :param char: Character you want converted
        :return: Decrypted character
        """
        if len(char) > 1:
            raise EncryptSettingError(self)
        return self.__overflow(char, -self.__shift_amount)

    def restrictions(self) -> list:
        """
        Give back restrictions for this class
        :return: list
        """
        return [self.__shift_setting]

    def checkRestriction(self, restriction: list) -> bool:
        """
        Check given restrictions for this class
        :param restriction: Restriction for the class
        :return: bool
        """
        if restriction == None:
            return True
        return self.__shift_setting == restriction[0]

    def getAttributes(self) -> List[str]:
        """
        Get all attributes of model
        :return: None, normally list of attributes
        """
        return [str(self.__shift_setting.value), str(self.__shift_amount)]

    def setAttributes(self, attributes: List[str]) -> bool:
        """
        Set all attributes of model with getAttributes as input
        :return: If succeeded
        """
        attributes = list(map(lambda attribute: int(attribute), attributes))

        self.__shift_setting = shiftSettings(attributes[0])
        self.__shift_amount = attributes[1]
        return True

    def __str__(self) -> str:
        return super().__str__() + f"Shift setting: {self.__shift_setting}\n\t" \
                                   f"Shift amount : {self.__shift_amount}\n"
