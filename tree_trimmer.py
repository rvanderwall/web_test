from Element import Element
from config import Config


class TreeTrimmer:
    def __init__(self, cfg: Config):
        self.html_containers = cfg.html_containers
        self.html_ignore = cfg.html_ignore

    # if a container has no children and no text, collapse it out
    # If a container has no children but has text, return it as a leaf
    # If a container has only a single child, collapse it
    def _trim_tree(self, parent: Element, tree: Element):
        if tree.tag_name in self.html_ignore:
            return None

        orig_parent = parent
        children = tree.children
        collapse_node = False
        check_children = False

        if tree.tag_name in self.html_containers:
            if len(children) == 0 and not tree.has_text():
                collapse_node = True
            if len(children) == 1:
                collapse_node = True
            if len(children) > 1:
                check_children = True  # If a container has multiple children but they all collapsed out, collapse this

        if collapse_node:
            # Put children into parent directly
            return_tree = None
        else:
            # Keep children in this node
            tree.children = []
            parent = tree
            return_tree = tree

        for child in children:
            child = self._trim_tree(parent, child)
            if child is not None:
                parent.children.append(child)

        if check_children:
            # See if our children got collapsed out
            if len(return_tree.children) == 0:
                # No children, collapse out this node
                return_tree = None
            elif len(return_tree.children) == 1:
                # Only one child remains, collapse this node
                orig_parent.children.append(return_tree.children[0])
                return_tree = None

        return return_tree

    def trim_tree(self, tree: Element):
        return self._trim_tree(None, tree)
