from Element import Element


class TreeBuilder:
    def __init__(self):
        self.tree = None

    def with_root(self, tag, text=""):
        self.tree = Element(None, include_location=False)
        self.tree.tag_name = tag
        self.tree.text = text
        return self

    def add_subtree(self, subtree):
        if isinstance(subtree, TreeBuilder):
            subtree = subtree.tree
        self.tree.children.append(subtree)
        return self

    def add_child(self, tag, text=""):
        child = Element(None, include_location=False)
        child.tag_name = tag
        child.text = text
        self.tree.children.append(child)
        return self
