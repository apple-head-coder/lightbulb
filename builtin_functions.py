from lbfunction import LBFunction


def _text(string):
    print(string.value, end="")


text = LBFunction({
    "^def": _text,
})

def create_lbint(value):
    return LBFunction({}, value)

def create_lbstring(value):
    return LBFunction({}, value)
