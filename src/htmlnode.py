
class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = None if tag == None else tag.strip() # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = None if value == None else value   # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children    # A list of HTMLNode objects representing the children of this node
        self.props = props          # A dictionary of key-value pairs representing the attributes of the HTML tag.

    #
    # Renders object as an HTML string 
    #
    def to_html(self):
        #
        # Abstract method
        #
        raise NotImplementedError


    #
    # Render the properties of this object as HTML attribute key/value pairs
    #
    def props_to_html(self):
        if self.props == None or len(self.props)== 0:
            return ""
        
        attributes = ""
        for key, value in self.props.items():
            attributes += f" {key}=\"{value}\""

        return attributes
    
    def __repr__(self):
        tag = None if self.tag == None else f"\"{self.tag}\""
        value = None if self.value == None else f"\"{self.value}\""
        children = None if self.children == None else f"[{len(self.children)} children]"
        props = None if self.props == None else f"{self.props}"
        return f"HTMLNode({tag}, {value}, {children}, {props})"