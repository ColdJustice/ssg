import os
import shutil
from blocktext import extract_title
from converter import markdown_to_html_node
from textnode import TextNode, TextType


def main():
    copy_tree("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")


def copy_tree(from_root, to_root):
    if not os.path.exists(from_root):
        raise Exception(f"Source path '{from_root}' does not exist!")
    
    if os.path.exists(to_root):
        shutil.rmtree(to_root)
    
    os.mkdir(to_root)

    files = os.listdir(from_root)
    for file in files:
        from_path = os.path.join(from_root, file)
        to_path = os.path.join(to_root, file)
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_tree(from_path, to_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    handle = open(from_path)
    markdown = handle.read()
    handle.close()
    handle = open(template_path)
    template = handle.read()
    handle.close()
    markdown_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", markdown_html)

    handle = open(dest_path, 'w')
    handle.write(template)
    handle.close


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception(f"Source path '{from_root}' does not exist!")
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    files = os.listdir(dir_path_content)
    for file in files:
        content_file_path = os.path.join(dir_path_content, file)
        destination_file_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
        if os.path.isfile(content_file_path):
            generate_page(content_file_path, template_path, destination_file_path)
        else:
            generate_pages_recursive(content_file_path, template_path, destination_file_path)


if __name__ == "__main__":
    main()
    