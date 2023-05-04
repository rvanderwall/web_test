import json
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import Config
from Element import Element, build_tree
from tree_trimmer import TreeTrimmer

def get_DOM_tree(cfg: Config) -> Element:
    driver = webdriver.Chrome(cfg.path_to_chrome_driver)
    driver.get(cfg.URL)
    dom_tree = driver.find_element(By.TAG_NAME, 'body')
    tree = build_tree(dom_tree, cfg)
    driver.quit()
    return tree


if __name__ == '__main__':
    cfg = Config()
    TREE = f'{cfg.prefix}tree.json'
    TRIMMED = f'{cfg.prefix}trimmed_tree.json'

    # tree = get_DOM_tree(cfg)
    #
    # with open(TREE, 'w', encoding='utf-8') as f:
    #     json.dump(tree.to_json(), f, ensure_ascii=False, indent=4)

    with open(TREE, 'r') as json_data:
        tree_json = json.load(json_data)
        tree = Element.from_json(tree_json)

    trimmed_tree = TreeTrimmer(cfg).trim_tree(tree)
    with open(TRIMMED, 'w', encoding='utf-8') as f:
        json.dump(trimmed_tree.to_json(), f, ensure_ascii=False, indent=4)
