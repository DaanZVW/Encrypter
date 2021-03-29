class multiFunc:
    def __init__(self, *functions):
        self.functions = [item for item in functions]

    def __call__(self, param: list = None) -> list:
        returns = []

        if type(param) is not list:
            param = [param]

        for index, function in enumerate(self.functions):
            try:
                if len(param) <= index:
                    returns.append(function())
                else:
                    returns.append(function(param[index]))
            except TypeError:
                returns.append(function())

        returns = list(filter(lambda return_value: return_value is not None, returns))
        if (lenght := len(returns)) > 1:
            return returns
        elif lenght == 1:
            return returns[0]
        return []


class callbackFunc:
    def __init__(self, function, *args):
        self.function = function
        self.args = args

    def __call__(self, *args, **kwargs):
        return self.function(*self.args)


def langCall(language_dict: dict, *keys: str) -> str:
    widget_text = language_dict
    try:
        for key in keys:
            widget_text = widget_text[key]
        return str(widget_text)
    except (KeyError, TypeError):
        return str(".".join(keys))