from transform_snippet import transform_snippet


def build_snippet_definition(d):
    block = []
    for k, v in d["snippet"]["snippet_definition"].items():
        if isinstance(v, str):
            block.append(f"{k}={v}")
        elif k == "options":
            if "r" in v:
                block.append("regTrig=true")
            if "A" in v:
                block.append('snippetType="autosnippet"')
    if "priority" in d.keys():
        block.append(f'priority={d["priority"]}')
    return "\n\t{" + ", ".join(block) + "}"


def build_snippet_content_block(d):
    nodes = d["snippet"]["snippet_content"]
    return "\t{\n\t\t" + ",\n\t\t".join([repr(node) for node in nodes]) + "\n\t}"


def build_conditions_block(d):
    block = []
    if "context" in d.keys():
        block.append(d["context"][1:-3])
    if block:
        return "\n\t{ condition = " + ", ".join(block) + " }"
    else:
        return block


def build_snippet(text):
    d = transform_snippet(text)

    blocks = [
        build_snippet_definition(d),
        build_snippet_content_block(d),
        build_conditions_block(d),
    ]

    return "s(" + ",\n".join([block for block in blocks if len(block) > 0]) + "\n),"
