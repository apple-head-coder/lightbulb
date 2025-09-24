from lark import Transformer

from builtin_functions import text, create_lbint, create_lbstring


# Transformers transform a tree into a single value by calling the corresponding
# method for each node and passing the return value to the parent node.
# LightbulbTransformer passes functions through the tree that when called return
# the corresponding value. This allows for precise control over order of execution.
class LightbulbTransformer(Transformer):
    def __init__(self, visit_tokens = True):
        self.global_vars = {
            "text": text,
        }

        super().__init__(visit_tokens)

    def blank(self, items):
        return lambda: None
    
    def statements(self, items):
        def run():
            for statement in items:
                statement()
        return run
    
    def assignment(self, items):
        def run():
            var_value = items[0]()
            var_name = items[1]  # id returns string - don't need to call

            self.global_vars[var_name] = var_value
        return run
    
    def function_call(self, items):
        def run():
            argument = items[0]()
            func = items[1]()
            func_version = func.default()

            func_version(argument)
        return run
    
    def value_of(self, items):
        # Value of variable from given id string
        return lambda: self.global_vars[items[0]]

    def id(self, items):
        return items[0]

    def literal(self, items):
        def run():
            literal_type = items[0]
            literal_value = items[1]

            if literal_type == "i":  # integer
                return create_lbint(int(literal_value))
            if literal_type == "s":  # string
                return create_lbstring(literal_value)
        return run
