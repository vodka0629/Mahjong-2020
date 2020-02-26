import unittest
from mahjong.tile import *


class TileTestCase(unittest.TestCase):
    def test_tile(self):
        w1 = Tile('万', 1, '1万', 1001)
        self.assertEqual(str(w1), '[1万]')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
