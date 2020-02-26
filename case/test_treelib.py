import unittest
from random import random
from treelib import *


class TreelibTestCase(unittest.TestCase):
    def test_treelib(self):
        tree = Tree()

        arr = [1,2,3]
        a_id = f'{arr}' + str(random())
        tree.create_node(arr, a_id)

        arr = [5, 5, 5]
        b_id = f'{arr}' + str(random())
        tree.create_node(arr, b_id, parent=a_id)







def main():
    unittest.main()


if __name__ == '__main__':
    main()
