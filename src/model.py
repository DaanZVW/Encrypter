# Library's
from enum import Enum
from typing import List


class encryptSettings(Enum):
    """
    Defines how information needs to be given
    """
    charBase = 0
    lineBase = 1
    allBase = 2
    lineOrAllBase = 3


class model:
    """
    Base model class which is used for making models for encrypting
    """
    def __init__(self, name: str, setting: Enum) -> None:
        """
        Constructor
        :param name: Name of the model
        :param setting: Encrypting setting
        """
        self.name = name
        self.setting = setting

    def encrypt(self, data: str) -> str:
        """
        Default implementation for encrypting, current state does nothing
        :param data: Data that needs encrypting
        :return: Data
        """
        print(f"encrypt function in module {self.name} is not implemented")
        return data

    def decrypt(self, data: str) -> str:
        """
        Default implementation for decrypting, current state does nothing
        :param data: Data that needs decrypting
        :return: Data
        """
        print(f"decrypt function in module {self.name} is not implemented")
        return data

    def restrictions(self) -> None:
        """
        Give back restrictions for this class
        :return: None, normally list with restrictions
        """
        return None

    def checkRestriction(self, restriction: list) -> bool:
        """
        Check given restrictions for this class
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

