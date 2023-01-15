from lark import Lark

with open("./grammar.lark", "r") as f:
    grammar = f.read()

def ultisnips_parser(text):
    return Lark(grammar, start='ultisnips').parse(text)
