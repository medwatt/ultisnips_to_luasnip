import re

#######################################################################
#                          useful functions                           #
#######################################################################

def replace_substring(s, start, end, repl="@"):
    """
    Replace section of string between `start` and `end` with `repl`.
    """
    n = end - start + 1
    return s[:start] + repl *n + s[end+1:]

def add_spaces(string, n_spaces):
    """
    Add `n_spaces` spaces to the left of each line in `string`.
    """
    lines = string.split("\n")
    spaces = " " * n_spaces
    for i, line in enumerate(lines):
        lines[i] = spaces + line
    return "\n".join(lines)

def split_and_make(string, delimiter, opening, closing):
    """
    Split `string` using `delimiter`, enclose each resulting substring
    in quotes, and place the entire string between `opening` and `closing`.
    """
    substrings = string.split(delimiter)
    for i, line in enumerate(substrings):
        substrings[i] = f'{opening}"{line}"{closing}'
    return ", ".join(substrings)

def extract_match(match, idx):
    """
    Obtain the regex group at index `idx` from the match object and return it.
    """
    try:
        return match.group(idx)
    except AttributeError:
        return None

#######################################################################
#                            luasnip nodes                            #
#######################################################################

def make_text_node(text):
    """
    For snippets that contain no tab stops
    """
    lines = text.split("\n")
    for i, line in enumerate(lines):
        lines[i] = f'"{line}"'
    text = ", ".join(lines)
    return f"\n{{t({{{text}}})}}"

def make_insert_node(idx, text=""):
    if text:
        return f'i({idx}, "{text}")'
    else:
        return f'i({idx})'

def make_replacement_node(idx):
    return f'rep({idx})'

def make_choice_node(idx, text):
    text = "{" + split_and_make(text, ",", "t(", ")") + "}"
    return f'c({idx}, {text})'

def make_visual_node(idx, text=""):
    if text:
        return f'd({idx}, get_visual("{text}"))'
    else:
        return f'd({idx}, get_visual)'

#######################################################################
#                          parsing functions                          #
#######################################################################

def find_tab_stops(string):
    """
    Find the indices of all tab stops in the string, including nested ones.
    """
    result = []     # list of list of tab stops
    nested = []     # list of tuples of tab stops. The last tap stop is the enclosing one
    stack = []
    previous_char = ""

    i = 0

    while i < len(string):
        char = string[i]

        # found the start of a tap stop with curly brackets
        if char == '{' and previous_char == "$":
            stack.append(i)
            previous_char = ""

        # found the end of a tap stop with curly brackets
        elif char == '}':
            if stack:
                start = stack.pop()
                nested.append((start, i))

        # find tab stops of the form $\d+
        elif char == '$':
            count = 0
            # valid tab stop
            for j, st in enumerate(string[i+1:]):
                try:
                    int(st)
                    count += 1
                except:
                    break
            if count > 0:
                result.append([(i, i + count)])
                i += count
            # the $ might be the beginning of a tab stop with curly brackets
            else:
                previous_char = char

        if not stack and nested:
            result.append(nested)
            nested = []

        i += 1
    return result

def make_nodes(string, lst_indices):
    """
    Make snippet nodes based on the list of indices.
    """
    nodes = []             # list of nodes in the snippet
    seen_tab_stops = []    # keep track of seen tab stops to identify replacement nodes

    for tab_stop in lst_indices:

        begin = tab_stop[-1][0]
        end = tab_stop[-1][1]

        if len(tab_stop) == 1:

            # TYPE: $1
            if end == begin + 1:
                idx = string[begin+1:end+1]
                if idx not in seen_tab_stops:
                    seen_tab_stops.append(idx)
                    nodes.append(make_insert_node(idx))
                else:
                    nodes.append(make_replacement_node(idx))
                string = replace_substring(string, begin, end)
                continue

            s = string[begin+1:end]

            #---------------------------------------------------------------------#

            # TYPE: $1:VISUAL:text
            m = re.search(r"""^\s*VISUAL\s*:?(.*?)$""", s)
            if m:
                nodes.append(make_visual_node('"FIX"', m.group(1)))
                string = replace_substring(string, begin, end)
                continue

            # TYPE: $1|<18,18~60,>60|
            m = re.search(r"""^(\d+)\s*\|(.*?)\|$""", s)
            if m:
                idx = seen_tab_stops.append(m.group(1))
                nodes.append(make_choice_node(m.group(1), m.group(2)))
                string = replace_substring(string, begin, end)
                continue

            # TYPE: $1:text
            m = re.search(r"""^(\d+)\s*:(.*?)$""", s)
            if m:
                seen_tab_stops.append(m.group(1))
                nodes.append(make_insert_node(m.group(1), m.group(2)))
                string = replace_substring(string, begin-1, end)
                continue

            #---------------------------------------------------------------------#

        elif len(tab_stop) > 1:
            r = string[begin+1:end]
            idx = r[:r.find(":")]

            s =string[tab_stop[-2][0]+1:tab_stop[-2][1]]

            # TYPE: ${1:${VISUAL:text}
            m = re.search(r"""VISUAL(?:\s*:)?(.*?$)?""", s)
            if m:
                seen_tab_stops.append(idx)
                nodes.append(make_visual_node(idx, m.group(1)))
                string = replace_substring(string, begin-1, end)
                continue

    delimited_snippet = re.sub("@{2,}", "<>", string)
    return  delimited_snippet, nodes


class LuaSnip:
    def __init__(self, file, delimiter="<>"):
        self.file = file
        self.delimiter = delimiter

    def split_file_into_snippets(self):
        """
        Split snippet file into a list of snippets.
        """
        snippet_regex = r"""\n(?:priority|context|snippet).*?endsnippet\n"""
        self.snippets = re.findall(snippet_regex, self.file, re.DOTALL)

    def parse_snippet(self, snippet):
        """
        Parse the content of a snippet.
        """
        priority_regex = r"""priority\s+(\d+)\s*\n"""
        context_regex = r"""\n\W*context\s+\W+(\w+)\W.*?\n"""
        snippet_definition_regex = r"""snippet\s+(.*?)(?:\s+['"](.*)['"])?(?:\s+(.*?))?\n"""
        snippet_content_regex = r"""snippet.*?\n(.*?)\nendsnippet"""

        priority_match = re.search(priority_regex, snippet)
        context_match = re.search(context_regex, snippet)
        snippet_definition_match = re.search(snippet_definition_regex, snippet)
        snippet_content_match = re.search(snippet_content_regex, snippet, re.DOTALL)

        snippet_trigger = extract_match(snippet_definition_match, 1)
        snippet_description = extract_match(snippet_definition_match, 2)

        priority = extract_match(priority_match, 1)
        try:
            priority = int(priority)
        except:
            priority = None


        self.snippet_parameters = {
            "trig": snippet_trigger,
            "dscr": snippet_description,
            "priority": priority,
        }

        context = extract_match(context_match, 1)
        self.snippet_condition = context

        self.snippet_content = extract_match(snippet_content_match, 1)

        snippet_options = extract_match(snippet_definition_match, 3)
        if snippet_options:
            self.snippet_options = list(snippet_options)
        else:
            self.snippet_options = []

    def prepare_snippet_parameters(self):
        """
        Prepare the snippet parameter block.
        """
        block = []
        for k, v in self.snippet_parameters.items():
            if k in ["trig", "dscr", "priority"] and v is not None:
                if isinstance(v, str):
                    block.append(f'{k}="{v}"')
                else:
                    block.append(f"{k}={v}")

        # convert ultisnips options to luasnip options
        for opt in self.snippet_options:
            if opt == "A":
                block.append('snippetType="autosnippet"')
            elif opt == "r":
                block.append("regTrig=false")

        return ",\n".join(block)


    def prepare_content_block(self):
        """
        Prepare the actual content of the snippet.
        """
        lst_tab_stops = find_tab_stops(self.snippet_content)
        if lst_tab_stops:
            delimited_snippet, nodes = make_nodes(self.snippet_content, lst_tab_stops)
            return self.prepare_format_block(delimited_snippet, nodes)
        else:
            return make_text_node(self.snippet_content)

    def prepare_format_block(self, snippet_delimited, tab_stops):
        format_block = "\nfmta("
        format_block += "\n[[\n"
        format_block += snippet_delimited
        format_block += "\n]],\n"
        format_block += "{\n"
        format_block += (",\n").join(tab_stops)
        format_block += "\n}\n"
        format_block += ")"
        return format_block

    def prepare_condition_block(self):
        if self.snippet_condition:
            return f"condition = {self.snippet_condition}"
        else:
            return None

    def build_snippet(self):

        param_block = self.prepare_snippet_parameters()
        content_block = self.prepare_content_block()
        condition_block = self.prepare_condition_block()

        snippet = ""
        snippet += "s(\n"
        snippet += "{\n" + param_block + "\n},"
        snippet += content_block

        if self.snippet_condition:
            snippet += ",\n"
            snippet += "{" + condition_block + "},"

        snippet += "\n),\n"

        return snippet

    def convert(self):
        self.split_file_into_snippets()
        snippets = []

        for snippet in self.snippets:
            self.parse_snippet(snippet)
            converted = self.build_snippet()
            snippets.append(converted)

        return snippets


if __name__ == "__main__":
    snippet_file = "./test.snippets"
    with open(snippet_file, "r") as f:
        snippet_string = f.read()

    luasnip = LuaSnip(snippet_string)
    converted = luasnip.convert()

    for c in converted:
        print(c)
