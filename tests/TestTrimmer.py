import unittest
from tree_trimmer import TreeTrimmer
from config import Config
from tests.TreeBuilder import TreeBuilder as TB


class TestTrimmer(unittest.TestCase):
    def test_can_create(self):
        cfg = Config()
        tt = TreeTrimmer(cfg)
        self.assertIsNotNone(tt)

    def test_div_in_div(self):
        cfg = Config()
        tt = TreeTrimmer(cfg)
        tree = TB().with_root("body") \
            .add_subtree(TB().with_root("div")
                         .add_child("div", "gc text").tree).tree

        rt = tt.trim_tree(tree)
        self.assertIsNotNone(rt)
        self.assertEqual(1, len(rt.children))
        child = rt.children[0]
        self.assertEqual(0, len(child.children))
        self.assertEqual("gc text", child.text)

    def test_empty_div_in_div(self):
        cfg = Config()
        tt = TreeTrimmer(cfg)
        tree = TB().with_root("body") \
                   .add_subtree(
                       TB().with_root("div")\
                           .add_subtree(
                               TB().with_root("div")\
                                   .add_child("div"))\
                           .add_child("div"))\
                   .tree

        rt = tt.trim_tree(tree)
        self.assertIsNotNone(rt)
        self.assertEqual(0, len(rt.children))

    def test_empty_div_collapses_in_div(self):
        cfg = Config()
        tt = TreeTrimmer(cfg)
        tree = TB().with_root("body") \
                   .add_subtree(
                       TB().with_root("div")\
                           .add_child("div")\
                           .add_child("div", "child1"))\
                   .tree

        rt = tt.trim_tree(tree)
        self.assertIsNotNone(rt)
        self.assertEqual(1, len(rt.children))
        self.assertEqual("child1", rt.children[0].text)

    def test_2div_in_div(self):
        cfg = Config()
        tt = TreeTrimmer(cfg)
        tree = TB().with_root("body")\
            .add_child("div", "child1")\
            .add_child("div", "child2")\
            .tree

        rt = tt.trim_tree(tree)
        self.assertIsNotNone(rt)
        self.assertEqual(2, len(rt.children))
        self.assertEqual("child1", rt.children[0].text)
        self.assertEqual("child2", rt.children[1].text)

    def test_nested_div_in_div(self):
        cfg = Config()
        tt = TreeTrimmer(cfg)
        tree = TB().with_root("body")\
            .add_subtree(TB().with_root("div")
                        .add_child("div", "child1")\
                        .add_child("div", "child2"))\
            .tree

        rt = tt.trim_tree(tree)
        self.assertIsNotNone(rt)
        self.assertEqual(1, len(rt.children))
        rt = rt.children[0]
        self.assertEqual(2, len(rt.children))
        self.assertEqual("child1", rt.children[0].text)
        self.assertEqual("child2", rt.children[1].text)

    def test_deep_nested_div_in_div(self):
        cfg = Config()
        tt = TreeTrimmer(cfg)
        tree = TB().with_root("body")\
            .add_subtree(TB().with_root("div")\
                         .add_subtree(TB().with_root("div")\
                            .add_child("div", "child1")))\
            .add_subtree(TB().with_root("div")\
                        .add_subtree(TB().with_root("div")\
                            .add_child("div", "child2")))\
            .tree

        rt = tt.trim_tree(tree)
        self.assertIsNotNone(rt)
        self.assertEqual(2, len(rt.children))
        self.assertEqual("child1", rt.children[0].text)
        self.assertEqual("child2", rt.children[1].text)

    def test_table_div_in_div(self):
        cfg = Config()
        tt = TreeTrimmer(cfg)
        tree = TB().with_root("body")\
            .add_subtree(TB().with_root("div", "text1")\
                .add_subtree(TB().with_root("div", "text11")\
                        .add_subtree(TB().with_root("div", "text111")\
                            .add_child("div", "child111")))\
                .add_subtree(TB().with_root("div", "text12")\
                        .add_subtree(TB().with_root("div", "text121")\
                            .add_child("button", "child121"))))\
            .add_subtree(TB().with_root("div", "text2")\
                .add_subtree(TB().with_root("div", "text21")\
                        .add_subtree(TB().with_root("div", "text211")\
                            .add_child("div", "child211")))\
                .add_subtree(TB().with_root("div", "text22")\
                        .add_subtree(TB().with_root("div", "text221")\
                            .add_child("button", "child221"))))\
            .tree

        rt = tt.trim_tree(tree)
        self.assertIsNotNone(rt)
        self.assertEqual(2, len(rt.children))
        c1 = rt.children[0]
        self.assertEqual(2, len(c1.children))
        self.assertEqual("child111", c1.children[0].text)
        self.assertEqual("child121", c1.children[1].text)

        c2 = rt.children[1]
        self.assertEqual(2, len(c2.children))
        self.assertEqual("child211", c2.children[0].text)
        self.assertEqual("child221", c2.children[1].text)
