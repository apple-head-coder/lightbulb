from lark import Transformer

from builtin_functions import *
from literal_parsers import *


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
    
    def if_statement(self, items):
        def run():
            condition = items[0]()
            condition_bool = condition.version("^^b")()  # ().^^b -> condition

            on_true = items[1]  # don't call yet
            if len(items) == 3:  # there's an else statement
                on_false = items[2]
            else:
                on_false = lambda: None

            if condition_bool.value:
                on_true()
            else:
                on_false()
        return run

    def while_loop(self, items):
        def run():
            condition = items[0]  # don't call yet

            inner = items[1] # don't call yet

            while condition().version("^^b")().value:  # ().^^b -> () -> condition
                inner()
        return run
    
    def for_loop(self, items):
        def run():
            # Don't call these yet
            first = items[0]
            condition = items[1]
            second = items[2]
            inner = items[3]

            first()
            while condition().version("^^b")().value:  # ().^^b -> () -> condition
                inner()
                second()
        return run
    
    def cvalues(self, items):
        # List of values separated by a comma
        return lambda: [value() for value in items]

    def op_or(self, items): return lambda: items[0]().version("^or")(items[1]())
    def op_and(self, items): return lambda: items[0]().version("^and")(items[1]())
    def op_not(self, items): return lambda: items[0]().version("^not")()

    def op_comp(self, items):
        def run():
            op = items[1]
            if op == "=":
                version = "^eq"
            elif op == ";=":
                version = "^neq"
            elif op == "<":
                version = "^less"
            elif op == ">":
                version = "^gtr"
            elif op == "<=":
                version = "^leq"
            elif op == ">=":
                version = "^geq"
            
            left = items[0]()
            right = items[2]()
            return left.version(version)(right)
        return run

    def op_addsub(self, items):
        def run():
            op = items[1]
            if op == "+":
                version = "^add"
            elif op == "-":
                version = "^sub"

            left = items[0]()
            right = items[2]()
            return left.version(version)(right)
        return run
    
    def op_muldiv(self, items):
        def run():
            op = items[1]
            if op == "*":
                version = "^mul"
            elif op == "/":
                version = "^div"
            
            left = items[0]()
            right = items[2]()
            return left.version(version)(right)
        return run

    def op_call(self, items):
        def run():
            arguments = items[0]()
            if not isinstance(arguments, list):
                arguments = [arguments]
            
            if len(items) == 3:  # called with version
                version_name = items[1]
                func = items[2]()
                func_version = func.version(version_name)
            else:  # called as default
                func = items[1]()
                func_version = func.default()

            return func_version(*arguments)
        return run
    
    def value_of(self, items):
        # Value of variable from given id string
        return lambda: self.global_vars[items[0]]

    def id(self, items):
        # Returns string of id instead of function
        return items[0]

    def literal(self, items):
        def run():
            literal_type = items[0]
            if len(items) == 2:  # non-empty literal
                literal_value = items[1]
            else:
                literal_value = ""

            if literal_type == "i":  # integer
                return create_lbint(int(literal_value))
            if literal_type == "s":  # string
                return create_lbstring(parse_string(literal_value))
            if literal_type == "b":  # boolean
                return create_lbboolean(parse_boolean(literal_value))
        return run
