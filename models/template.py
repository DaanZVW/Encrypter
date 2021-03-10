# =========================================================
# = This file is only to showcase how to make a new model =
# =========================================================

# Library's
from enum import Enum
from typing import List

# Src files
from app.legacy.gui import modelGui
from src.model import model, encryptSettings


def getDefaultModel() -> model:
    """
    This function will be used when importing models
    """
    return defaultModel(defaultModelSettings.default)


def getModelGUI(**kwargs) -> modelGui:
    """
    Get the GUI for the default module
    :param master: Frame to put it on
    """
    gui = modelGui(**kwargs)
    default_class = getDefaultModel()
    gui.configure_gui(default_class.name, default_class.setting)
    gui.addEnumSelectionSetting("Default selection setting",
                                list(map(lambda selection: str(selection), defaultModelSettings)),
                                defaultModelSettings)
    gui.addSetting("Default setting", str, str)
    gui.addCheckboxSetting("Default checkbox setting", "Checkbox", str)
    return gui


class defaultModelSettings(Enum):
    """
    Defines how information needs to be given
    """
    default = 0


class defaultModel(model):
    """
    Template model which all other models need to follow
    Copy paste this file when making a new model
    """
    def __init__(self, setting: defaultModelSettings) -> None:
        """
        Constructor
        :param setting: Setting of this model
        """
        super().__init__("Default", encryptSettings.allBase)
        self.__default_setting = setting

    def encrypt(self, data: str) -> str:
        """
        Default implementation for encrypting, current state does nothing
        :param data: Data that needs encrypting
        :return: Data
        """
        return data

    def decrypt(self, data: str) -> str:
        """
        Default implementation for decrypting, current state does nothing
        :param data: Data that needs decrypting
        :return: Data
        """
        return data

    def restrictions(self) -> None:
        """
        Give back restrictions for this class
        NOTE: When there are no restrictions, don't implement this function
        :return: None, normally a list with restrictions
        """
        return None

    def checkRestriction(self, restriction: list) -> bool:
        """
        Check given restrictions for this class
        NOTE: When there are no restrictions, don't implement this function
        :param restriction: Restriction for the class
        :return: bool
        """
        return True

    def getAttributes(self) -> None:
        """
        Get all attributes of model
        :return: None, normally list of attributes
        """
        return None

    def setAttributes(self, attributes: List[str]) -> bool:
        """
        Set all attributes of model with getAttributes as input
        :return: If succeeded
        """
        return True

    def __str__(self):
        return f"{self.name}, {self.setting}:\n\t"

    def __repr__(self):
        return self.__str__() + ", "

