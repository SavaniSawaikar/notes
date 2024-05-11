from lc.google_practice.binary_tree import BinaryTree

def test_create_a_binary_tree():
    tree = BinaryTree('a')
    assert tree.val == 'a'

def test_build_tree():
    tree = BinaryTree('a')
    tree.insert_left('b')
    tree.left.insert_right('d')
    tree.insert_right('c')
    tree.right.insert_left('e')
    tree.right.insert_right('f')

    assert [tree.val, tree.left.val, tree.left.right.val, tree.right.val, tree.right.left.val, tree.right.right.val] == ['a', 'b', 'd', 'c', 'e', 'f']