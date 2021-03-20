class multiFunc:
    def __init__(self, *functions):
        self.__functions = functions

    def __call__(self, param):
        return list(map(lambda func: func(param), self.__functions))[0]


def langCall(language_dict: dict, *keys: str) -> str:
    widget_text = language_dict
    try:
        for key in keys:
            widget_text = widget_text[key]
        return str(widget_text)
    except (KeyError, TypeError):
        return str(".".join(keys))