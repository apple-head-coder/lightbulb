from lark import Lark, Transformer
from rich import print as rich_print


class LBFunction:
    def __init__(self, versions, value = None):
        self.versions = versions
        self.value = value
    
    def default(self):
        return self.versions["^def"]

    def version(self, version):
        return self.versions[version]


class LightbultTransformer(Transformer):
    def __init__(self, visit_tokens = True):
        self.global_vars = {
            "text": LBFunction({"^def": lambda s: print(s.value, end="")}),
        }

        super().__init__(visit_tokens)

    def blank(self):
        return lambda: None
    
    def statements(self, items):
        def run():
            for statement in items:
                statement()
        return run
    
    def assignment(self, items):
        def run():
            var_name = items[1]
            var_value = items[0]()
            self.global_vars[var_name] = var_value
        return run
    
    def function_call(self, items):
        def run():
            func = items[1]()
            func_version = func.default()
            argument = items[0]()
            func_version(argument)
        return run
    
    def value_of(self, items):
        return lambda: self.global_vars[items[0]]

    def id(self, items):
        return items[0]

    def literal(self, items):
        def run():
            literal_type = items[0]
            literal_value = items[1]
            if literal_type == "i":
                return LBFunction({}, int(literal_value))
            if literal_type == "s":
                return LBFunction({}, literal_value)
        return run


parser = Lark.open("lightbulb.lark", parser="lalr")
lightbulb_transformer = LightbultTransformer()

path = input("Enter file path: ")
with open(path, "r") as file:
    code = file.read()

tree = parser.parse(code)
rich_print(tree)

program = lightbulb_transformer.transform(tree)
program()
