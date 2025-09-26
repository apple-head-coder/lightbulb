from lark import Transformer

from builtin_functions import text, create_lbint, create_lbstring, create_lbboolean


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
            arguments = items[0]()
            
            if len(items) == 3:  # called with version
                version_name = items[1]
                func = items[2]()
                func_version = func.version(version_name)
            else:  # called as default
                func = items[1]()
                func_version = func.default()

            return func_version(*arguments)
        return run
    
    def if_statement(self, items):
        def run():
            condition = items[0]()
            on_true = items[1]  # don't call yet
            if len(items) == 3:  # there's an else statement
                on_false = items[2]
            else:
                on_false = lambda: None

            if condition.value:
                on_true()
            else:
                on_false()
        return run
    
    def cvalues(self, items):
        # List of values separated by a comma
        return lambda: [value() for value in items]
    
    def value_of(self, items):
        # Value of variable from given id string
        return lambda: self.global_vars[items[0]]

    def id(self, items):
        # Returns string of id instead of function
        return items[0]

    def literal(self, items):
        def run():
            literal_type = items[0]
            literal_value = items[1]

            if literal_type == "i":  # integer
                return create_lbint(int(literal_value))
            if literal_type == "s":  # string
                return create_lbstring(literal_value)
            if literal_type == "b":  # boolean
                if literal_value in ("1", "t", "true"):
                    return create_lbboolean(True)
                elif literal_value in ("0", "f", "false"):
                    return create_lbboolean(False)
                raise ValueError(f"Invalid boolean literal: {literal_value}")
        return run
