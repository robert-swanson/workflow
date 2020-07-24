import sys

args = sys.argv[1:]

invalidChars = ['~', '"', '#', '%', '&', '*', ':', '<', '>', '?', '/' '\\', '{', '}', '|']

def main(args):
    if len(args) != 1:
        print("Usage: python3 onedriveNames.py <filename/dirname>")
    name = args[0]

    print(name)
