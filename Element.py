from selenium.webdriver.common.by import By
from config import Config


class Location:
    def __init__(self, web_element):
        if web_element is not None:
            self.x = web_element.rect['x']
            self.y = web_element.rect['y']
            self.height = web_element.rect['height']
            self.width = web_element.rect['width']
        else:
            self._set_from_json({})

    def to_json(self):
        json_doc = {
            "x": self.x,
            "y": self.y,
            "height": self.height,
            "width": self.width,
        }
        return json_doc

    def _set_from_json(self, json_doc):
        self.x = json_doc.get("loc_x", 0)
        self.y = json_doc.get("loc_y", 0)
        self.height = json_doc.get("height", 0)
        self.width = json_doc.get("width", 0)

    @staticmethod
    def from_json(json_doc):
        l = Location(None)
        l._set_from_json(json_doc)
        return l


class Element:
    def __init__(self, web_element, include_location: bool):
        if include_location:
            self.location = Location(web_element)
        else:
            self.location = None

        if web_element is not None:
            self.tag_name = web_element.tag_name
            self.text = self._get_text(web_element)
        else:
            self.tag_name = ""
            self.text = ""

        self.parent = None
        self.children = []

    @staticmethod
    def _get_text(web_element):
        if web_element.tag_name == "img":
            return f"{web_element.aria_role}:{web_element.accessible_name}"
        elif web_element.tag_name == "a":
            text = f"{web_element.aria_role}:{web_element.accessible_name}"
            return text
        else:
            return web_element.text

    def to_json(self):
        json_doc = {
            "tag_name": self.tag_name,
            "text": self.text,
            "children": [child.to_json() for child in self.children]
        }
        if isinstance(self.location, Location):
            json_doc["location"] = self.location.to_json()

        return json_doc

    @staticmethod
    def from_json(json_doc):
        if 'location' in json_doc:
            include_location = True
        else:
            include_location = False

        e = Element(None, include_location)
        e.location = Location.from_json(json_doc['location']) if 'location' in json_doc else None
        e.tag_name = json_doc["tag_name"]
        e.text = json_doc["text"]
        for child_json in json_doc["children"]:
            ce = Element.from_json(child_json)
            ce.parent = e
            e.children.append(ce)
        return e


def build_tree(web_element, cfg: Config):
    root = Element(web_element, cfg.include_location)
    for child in web_element.find_elements(By.XPATH, "./child::*"):
        try:
            tag = child.tag_name
        except:
            tag = None

        if tag is None or tag == 'iframe':
            continue

        c = build_tree(child, cfg)
        c.parent = root
        root.children.append(c)
    return root
