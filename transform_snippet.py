from lark import Transformer
from parser import ultisnips_parser
from luasnip_nodes import TextNode, InsertNode, ChoiceNode, SnippetNode


class LuaSnipTransformer(Transformer):
    def snippet(self, items):
        # return "s(" + "\n".join(items) + "\n),"
        return ("snippet", dict(items))

    def snippet_definition(self, items):
        # return "\n\t{" + ", ".join(items) + "},"
        return ("snippet_definition", dict(items))

    def trigger(self, s):
        (s,) = s
        if s[0] != "'" or s[0] != '"':
            s = f'"{s}"'
        return ("trig", s)

    def description(self, s):
        (s,) = s
        return ("dscr", s)

    def options(self, s):
        (s,) = s
        return ("options", list(s))

    def tabstop(self, s):
        if len(s) == 1:
            return InsertNode(s[0])
        elif len(s) == 2:
            if isinstance(s[1], ChoiceNode):
                s[1].index = s[0]
                return s[1]
            else:
                return InsertNode(s[0], s[1])
        else:
            return SnippetNode(s[0], s[1:])

    def conditional(self, s):
        nodes = []
        for string in s:
            nodes.append(TextNode(string))
        return ChoiceNode(nodes)

    def TEXT(self, text):
        return TextNode(text)

    def TABSTOP_TEXT(self, s):
        # return f't("{s}")'
        return f"{s}"

    def CHOICE(self, s):
        return s

    def INT(self, d):
        return int(d)

    def context(self, s):
        (s,) = s
        return ("context", s)

    def priority(self, d):
        return ("priority", int(d[0]))

    def snippet_content(self, s):
        # return "\t{\n\t\t" + ",\n\t\t".join([str(node) for node in s]) + "\n\t}"
        return ("snippet_content", s)

    def WORD(self, s):
        return s

    def ESCAPED_STRING(self, s):
        return str(s)

    def ultisnips(self, s):
        return dict(s)


def transform_snippet(text):

    tree = ultisnips_parser(text)

    # print(tree)
    # print("")
    # print(tree.pretty())

    # TODO: seen nodes should be cleared betweeen snippet runs
    # this must be done in a better way
    InsertNode.seen_nodes = []

    return LuaSnipTransformer().transform(tree)


