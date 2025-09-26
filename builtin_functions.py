from lbfunction import LBFunction


def _text(value):
    string = value.version("^^s")()  # ().^^s -> value $ string
    print(string.value, end="")


text = LBFunction({
    "^def": _text,
})


def create_lbint(value):
    def _add(other): return create_lbint(value + other.value)
    def _sub(other): return create_lbint(value - other.value)
    def _mul(other): return create_lbint(value * other.value)
    def _div(other): return create_lbint(value // other.value)
    
    def _eq(other): return create_lbboolean(value == other.value)
    def _neq(other): return create_lbboolean(value != other.value)
    def _less(other): return create_lbboolean(value < other.value)
    def _gtr(other): return create_lbboolean(value > other.value)
    def _leq(other): return create_lbboolean(value <= other.value)
    def _geq(other): return create_lbboolean(value >= other.value)

    def _and(other): return create_lbboolean(value and other.value)
    def _or(other): return create_lbboolean(value or other.value)
    def _not(): return create_lbboolean(not value)

    def __i(): return create_lbint(value)
    def __s(): return create_lbstring(str(value))
    def __b(): return create_lbboolean(bool(value))

    return LBFunction({
        "^add": _add, "^sub": _sub, "^mul": _mul, "^div": _div,
        "^eq": _eq, "^neq": _neq, "^less": _less, "^gtr": _gtr, "^leq": _leq, "^geq": _geq,
        "^and": _and, "^or": _or, "^not": _not,
        "^^i": __i, "^^s": __s, "^^b": __b,
    }, value)


def create_lbstring(value):
    def _add(other): return create_lbstring(value + other.value)

    def _and(other): return create_lbboolean(value and other.value)
    def _or(other): return create_lbboolean(value or other.value)
    def _not(): return create_lbboolean(not value)

    def __i(): return create_lbint(int(value))
    def __s(): return create_lbstring(value)
    def __b(): return create_lbboolean(bool(value))

    return LBFunction({
        "^add": _add,
        "^and": _and, "^or": _or, "^not": _not,
        "^^i": __i, "^^s": __s, "^^b": __b,
    }, value)


def create_lbboolean(value):
    def _and(other): return create_lbboolean(value and other.value)
    def _or(other): return create_lbboolean(value or other.value)
    def _not(): return create_lbboolean(not value)

    def __i(): return create_lbint(int(value))
    def __s(): return create_lbstring(str(value))
    def __b(): return create_lbboolean(value)

    return LBFunction({
        "^and": _and, "^or": _or, "^not": _not,
        "^^i": __i, "^^s": __s, "^^b": __b,
    }, value)
