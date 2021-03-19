class multiFunc:
    def __init__(self, *functions):
        self.__functions = functions

    def __call__(self, param):
        return list(map(lambda func: func(param), self.__functions))[0]


