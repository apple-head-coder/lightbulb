from lark import Lark
from rich import print as rich_print

from lbtransformer import LightbulbTransformer

parser = Lark.open("lightbulb.lark", parser="lalr")
lightbulb_transformer = LightbulbTransformer()

path = input("Enter file path: ")
with open(path, "r") as file:
    code = file.read()

tree = parser.parse(code)
rich_print(tree)

program = lightbulb_transformer.transform(tree)
program()
