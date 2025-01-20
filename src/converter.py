import re

from blocktext import block_to_block_type, markdown_to_blocks
from inlinetext import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown):
    base_node = ParentNode("div", [], None)
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "paragraph":
                base_node.children.append(create_paragraph(block))
            case "heading":
                base_node.children.append(create_heading(block))
            case "code":
                base_node.children.append(create_code(block))
            case "quote":
                base_node.children.append(create_quote(block))
            case "unordered list":
                base_node.children.append(create_unordered_list(block))
            case "ordered list":
                base_node.children.append(create_ordered_list(block))
    return base_node

def text_to_children(block):
    return list(map(text_node_to_html_node, text_to_textnodes(block)))
    

def create_paragraph(block):
    return ParentNode("p", text_to_children(block))


def create_heading(block):
    heading_level = 0
    for char in block:
        if char != "#":
            break
        heading_level += 1
    return ParentNode(f"h{heading_level}", text_to_children(block[heading_level + 1:]))


def create_code(block):
    new_block = "\n".join(block.split("\n")[1:-1])
    return ParentNode("pre", [
        LeafNode("code", new_block)
    ])


def create_quote(block):
    new_block = re.sub(r"^\>\s{0,1}(.*)", r"\1", block, flags=re.MULTILINE)
    return ParentNode("blockquote", text_to_children(new_block))


def create_unordered_list(block):
    lines = map(lambda line: line[2:], block.split("\n"))
    return ParentNode("ul", 
        list(map(lambda line: ParentNode("li", text_to_children(line)), lines)))


def create_ordered_list(block):
    lines = re.sub(r"^\d+\. (.*)", r"\1", block, flags=re.MULTILINE).split("\n")
    return ParentNode("ol",
        list(map(lambda line: ParentNode("li", text_to_children(line)), lines)))



