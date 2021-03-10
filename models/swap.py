# Library's
from enum import Enum
from typing import Callable, List

# Src files
from src.model import model, encryptSettings
from src.exceptions import RandomModuleError
from src.randomHelper import randomHelper, randomSettings

# Gui files
from app.legacy.gui import modelGui


def getDefaultModel() -> model:
    """
    This function will be used when importing models
    :return: Default model with default settings
    """
    return swap(swapSettings.default)


def getModelGUI(**kwargs) -> modelGui:
    """
    Get the GUI for the Swap module
    :param master: Frame to put it on
    """
    gui = modelGui(**kwargs)
    default_class = getDefaultModel()
    gui.configure_gui(default_class.name, default_class.setting)
    gui.addEnumSelectionSetting("Swap setting", list(map(lambda setting: str(setting), swapSettings)), swapSettings)
    gui.addSetting("Swap amount", int)
    gui.addCheckboxSetting("Random seed", "Custom", int)
    return gui


class swapSettings(Enum):
    """
    Swap settings for swap model
    """
    reverse = 1
    random = 2
    lineReverse = 3
    lineRandom = 4
    linearReverse = 5
    linearRandom = 6
    default = reverse


class swap(model):
    """
    Swap model for switch positions in given string
    """

    def __init__(self, setting: swapSettings):
        """
        Constructor
        :param setting: Setting which the model will be set too
        """
        super().__init__("Swap", encryptSettings.lineOrAllBase)
        self.__swap_setting = setting
        self.__swap_amount = 0
        self.__random_module = NotImplemented
        self.__encrypt = True

    # Functions for setting model
    def setSwapAmount(self, amount: int) -> None:
        """
        Set the swap amount
        :param amount: Number
        """
        self.__swap_amount = amount

    def setRandomModule(self, module: randomHelper) -> None:
        """
        Set the internal random module
        :param module: randomHelper
        """
        self.__random_module = module

    # Internal functions
    def __internalSwapReverse(self, data: List[str], amount: int) -> List[str]:
        """
        Reverse a given list of strings
        :param data: List of strings
        :param amount: Amount of paired data indexes
        :return: Reversed list of strings
        """
        if len(data) <= amount * 2 - 1:
            return data
        return data[-amount:] + self.__internalSwapReverse(data[amount:-amount], amount) + data[:amount]

    def __internalSwapLinear(self, data: List[str], amount: int, function: Callable[[List[str]], List[str]]) -> List[str]:
        """
        Do a function on pairs of amount
        :param data: List of strings
        :param amount: Amount of paired data indexes
        :param function: Function which is ran on every pair
        :return: List of strings
        """
        if len(data) <= amount * 2 - 1:
            return function(data)
        return function(data[:amount]) + self.__internalSwapLinear(data[amount:], amount, function)

    def __internalSwapRandom(self, data: List[str]) -> List[str]:
        """
        Randomise the position of data
        :param data: List of strings
        :return: Scrambled list of strings
        """
        if self.__random_module is NotImplemented:
            raise RandomModuleError(self)
        elif self.__encrypt:
            return self.__random_module.scramble(data)
        return self.__random_module.unscramble(data)

    # Model functions
    def encrypt(self, data: str) -> str:
        """
        Encrypt function for swapping data
        :param data: Data that needs swapping
        :return: Swapped string
        """
        if self.__swap_setting is swapSettings.reverse:
            return "".join(self.__internalSwapReverse(list(data), self.__swap_amount))

        
        elif self.__swap_setting is swapSettings.random:
            return "".join(self.__internalSwapRandom(list(data)))

        elif self.__swap_setting is swapSettings.lineReverse:
            return "".join(self.__internalSwapReverse(data.splitlines(keepends=True), self.__swap_amount))

        elif self.__swap_setting is swapSettings.lineRandom:
            return "".join(self.__internalSwapRandom(data.splitlines(keepends=True)))

        elif self.__swap_setting is swapSettings.linearReverse:
            return "".join(self.__internalSwapLinear(
                list(data), self.__swap_amount, lambda text: self.__internalSwapReverse(text, 1)
            ))

        elif self.__swap_setting is swapSettings.linearRandom:
            return "".join(self.__internalSwapLinear(
                list(data), self.__swap_amount, lambda text: self.__internalSwapRandom(text)
            ))

        return data

    def decrypt(self, data: str) -> str:
        """
        Decrypt function for swapping data
        :param data: Data that needs unswapping
        :return: Unswapped string
        """
        self.__encrypt = False
        encrypted_data = self.encrypt(data)
        self.__encrypt = True
        return encrypted_data

    def getAttributes(self) -> List[str]:
        """
        Get all attributes of model
        :return: None, normally list of attributes
        """
        if self.__random_module is NotImplemented:
            attributes = [self.__swap_setting.value, self.__swap_amount]
        else:
            attributes = [self.__swap_setting.value, self.__swap_amount, self.__random_module.seed]
        return list(map(lambda module: str(module), attributes))

    def setAttributes(self, attributes: List[str]) -> bool:
        """
        Set all attributes of model with getAttributes as input
        :return: If succeeded
        """
        attributes = list(map(lambda attribute: int(attribute), attributes))

        self.__swap_setting = swapSettings(attributes[0])
        self.__swap_amount = attributes[1]
        if len(attributes) > 2:
            self.__random_module = randomHelper(randomSettings.custom)
            self.__random_module.setInternalSeed(int(attributes[2]))
        else:
            self.__random_module = randomHelper(randomSettings.random)
        return True

    def __str__(self) -> str:
        return super().__str__() + f"Swap setting: {self.__swap_setting}\n\t" \
                                   f"Seed amount : {self.__random_module}\n\t" \
                                   f"Swap amount : {self.__swap_amount}\n"
