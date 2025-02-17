from lark import Lark

# Load the grammar from the file
with open("grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr")

# Test parsing and print tree
tree = parser.parse("+ [1:5][10:20].")
print(tree.pretty())
