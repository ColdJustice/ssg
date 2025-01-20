from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("a tag is required for a parent node")
        if self.children == None or len(self.children) == 0:
            raise ValueError("at least one child is required for a parent node")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html