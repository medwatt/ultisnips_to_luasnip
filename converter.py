import re
from build_snippet import build_snippet

def split_file_into_snippets(file):
    """
    Split snippet file into a list of snippets.
    """
    snippet_regex = r"""\n(?:priority|context|snippet).*?endsnippet\n"""
    snippets = re.findall(snippet_regex, file, re.DOTALL)

    return snippets

if __name__ == "__main__":

    with open("./test.snippets", "r") as f:
        file = f.read()

    snippets = split_file_into_snippets(file)

    for snippet in snippets:
        try:
            converted = build_snippet(snippet)
            print(converted)
        except:
            pass
