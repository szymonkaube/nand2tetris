import sys

from parser import Parser


filename = sys.argv[1]
with open(filename, "r") as f:
    lines = f.read().splitlines()

parser = Parser()
parser_out = parser.parse(lines)
print(parser_out)
