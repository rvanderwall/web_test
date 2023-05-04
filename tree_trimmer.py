from Element import Element
from config import Config


class TreeTrimmer:
    def __init__(self, cfg: Config):
        self.html_containers = cfg.html_containers
        self.html_ignore = cfg.html_ignore

    def _trim_tree(self, parent: Element, tree: Element):
        if tree.tag_name in self.html_ignore:
            return None

        children = tree.children

        if tree.tag_name in self.html_containers:
            # Put children into parent directly
            return_tree = None
        else:
            # Keep children here
            tree.children = []
            parent = tree
            return_tree = tree

        for child in children:
            child = self._trim_tree(parent, child)
            if child is not None:
                parent.children.append(child)

        return return_tree

    def trim_tree(self, tree: Element):
        return self._trim_tree(None, tree)
