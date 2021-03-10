# Library's
from enum import Enum
import random
import time


class randomSettings(Enum):
    """
    Settings for the randomHelper class
    """
    custom = 0
    random = 1


class randomHelper:
    """
    Interface for the random generator
    """
    def __init__(self, setting: randomSettings) -> None:
        """
        Constructor
        :param setting: Setting which the randomHelper will be set too
        """
        self.__random_setting = setting
        self.seed = time.time_ns() if setting is randomSettings.random else 0

    def setInternalSeed(self, seed: int = 0) -> None:
        """
        Set the internal seed which will be set at every random function
        :param seed: Which seed it will be set to
        """
        if self.__random_setting is not randomSettings.random:
            self.seed = seed

    def setSeed(self) -> None:
        """
        Set the internal seed manually
        """
        random.seed(self.seed)
    
    def scramble(self, data: list) -> list:
        """
        Scramble a given list with internal seed
        :param data: List with data
        :return: Scrambled list with data
        """
        random.seed(self.seed)
        random.shuffle(data)
        return data

    def unscramble(self, data: list) -> list:
        """
        Unscramble a given list with internal seed
        :param data: List with data
        :return: Unscrambled list with data
        """
        pos_data = list(range(len(data)))
        shuffled_data = list(zip(data, self.scramble(pos_data)))
        shuffled_data.sort(key=lambda x: x[1])
        return list(map(lambda x: x[0], shuffled_data))

    def __str__(self):
        return f"{self.seed}"


