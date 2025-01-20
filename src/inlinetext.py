import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        splits = old_node.text.split(delimiter)
        #
        # Check for an un-terminated segment like "Hey *now!"
        #
        if len(splits) % 2 == 0:
            raise Exception(f"Missing closing {delimiter} in \"{old_node.text}\"")

        if len(splits) == 1:
            new_nodes.append(old_node)
            continue
        #
        # Every other split item with an odd-numbered index
        # should be added as `text_type`
        #
        for index in range(0, len(splits), 2):
            if splits[index] != "":
                new_nodes.append(TextNode(splits[index], TextType.TEXT))
            if index + 1 < len(splits):
                new_nodes.append(TextNode(splits[index + 1], text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    return split_link_type_nodes(
        old_nodes,
        extract_markdown_images,
        lambda alt_text, link: f"![{alt_text}]({link})",
        lambda alt_text, link: TextNode(alt_text, TextType.IMAGE, url=link),
        "image link")


def split_nodes_link(old_nodes):
    return split_link_type_nodes(
        old_nodes,
        extract_markdown_links,
        lambda link_text, src: f"[{link_text}]({src})",
        lambda link_text, src: TextNode(link_text, TextType.LINK, url=src),
        "URL link")


def split_link_type_nodes(
        old_nodes,
        extracter,
        split_delimiter_pattern,
        link_type_node_formatter,
        link_type_name):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extracter(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        for link in links:
            if original_text == "":
                continue

            link_display_text, link_url = link
            split_delimiter = split_delimiter_pattern(link_display_text, link_url)
            segments = original_text.split(split_delimiter, 1)
            if segments[0] != "":
                new_nodes.append(TextNode(segments[0], TextType.TEXT))
            new_nodes.append(link_type_node_formatter(link_display_text, link_url))
            original_text = segments[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))        
            
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?:(?:^\[)|(?:[^!]\[))(.*?)\]\(([^)]*)\)", text)


def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
    