def split_lines(text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        lines[i] = line
    return lines


def quote_and_join_strings_in_list(lst):
    return ", ".join([f'{repr(line)}' for line in lst])


class TextNode:
    def __init__(self, text):
        self.lines = split_lines(text)

    def __repr__(self):
        if len(self.lines) == 1:
            return f't({repr(self.lines[0])})'
        else:
            return f"t({{ {quote_and_join_strings_in_list(self.lines)} }})"

    def __str__(self):
        if len(self.lines) == 1:
            return repr(self.lines[0])
        else:
            return "\n".join(self.lines)


class InsertNode:
    seen_nodes = []

    def __init__(self, index, text=None):
        self.index = index
        if text:
            self.lines = split_lines(text)
        else:
            self.lines = None
        if not text and index in InsertNode.seen_nodes:
            self.repitition = True
        else:
            self.repitition = False
            InsertNode.seen_nodes.append(index)

    def __repr__(self):
        if not self.repitition:
            if self.lines:
                if len(self.lines) == 1:
                    return f'i({self.index}, {repr(self.lines[0])})'
                else:
                    return f"i({self.index}, {{ {quote_and_join_strings_in_list(self.lines)} }})"
            else:
                return f"i({self.index})"
        else:
            return f"rep({self.index})"


# class VisualNode:
#     def __init__(self, text=None, visual_func_name=None):
#         self.text = text
#         self.visual_func_name = visual_func_name
#
#     def __repr__(self):
#         if self.text:
#             return f"d(1, visual_func_name({self.tex}))"
#         else:
#             return f"d(1, {self.visual_func_name})"


class ChoiceNode:
    def __init__(self, nodes):
        self.index = -1
        self.nodes = nodes

    def __repr__(self):
        return f'c({self.index}, {{ {", ".join([repr(node) for node in self.nodes])} }})'


class SnippetNode:
    def __init__(self, index, nodes):
        self.index = index
        self.nodes = nodes
        self.renumber_nodes()
        self.correct_text_nodes()

    def renumber_nodes(self):
        count = 1
        for node in self.nodes:
            if type(node) in [InsertNode, ChoiceNode, SnippetNode]:
                node.index = count
                count += 1
            # if isinstance(node, InsertNode):
            #     node.index = count
            #     count += 1

    def correct_text_nodes(self):
        for i, node in enumerate(self.nodes):
            if isinstance(node, str):
                self.nodes[i] = TextNode(node)

    def __repr__(self):
        return f"""c({self.index}, {{ sn(nil, {{ {", ".join([repr(node) for node in self.nodes])} }} ), t('') }} )"""
