import re

def markdown_to_blocks(text):
    blocks = list(
        filter(lambda line: line != "",
               map(lambda line: line.strip(),
                   re.split(r"\n\s*\n", text))))
    return blocks

def extract_title(text):
    match = re.search(r"^\# (.*)", text, flags=re.MULTILINE)
    if not match:
        raise Exception("Document Error: A first-order header is required.")
    
    return match.group(1)

def block_to_block_type(block):
    lines = block.split("\n")
    matches = re.match(r"^[#]{1,6} ", block)
    ordered_list_regex = re.compile(r"^\d+\. ")

    if matches != None:
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if all(i.startswith(">") for i in lines):
        return "quote"
    if len(
        list(filter(lambda line: line.startswith("- "), lines)) + 
        list(filter(lambda line: line.startswith("* "), lines))) == len(lines):
        return "unordered list"
    if all(ordered_list_regex.match(line) != None for line in lines) and lines_are_ordered(lines):
        return "ordered list"
    return "paragraph"

def lines_are_ordered(lines):
    line_number = 1
    for line in lines:
        if not line.startswith(str(line_number)):
            return False
        line_number += 1
    return True
    