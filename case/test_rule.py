import unittest
from mahjong.rule import *


class RuleTestCase(unittest.TestCase):
    def test_rule_convert(self):
        mj_set = MjSet()
        mj_set.shuffle()
        concealed = []
        for _ in range(13):
            concealed.append(mj_set.draw())
        test1 = Rule.convert_tiles_to_str(concealed)
        arr = Rule.convert_tiles_to_arr(concealed)
        tiles = Rule.convert_arr_to_tiles(arr)
        test2 = Rule.convert_tiles_to_str(tiles)
        self.assertEqual(test1, test2)

    def test_rule_mahjong(self):
        mj_set = MjSet()
        tiles = []
        for _ in range(4):
            for x in range(3):
                tiles.append(mj_set.draw())
            mj_set.draw()
        tiles.append(mj_set.draw())
        tiles.append(mj_set.draw())
        # print(Rule.convert_tiles_to_str(tiles))
        test = Rule.is_mahjong(tiles)
        self.assertTrue(test)

        mj_set.shuffle()
        tiles = []
        for _ in range(14):
            tiles.append(mj_set.draw())
        # print(Rule.convert_tiles_to_str(tiles))
        test = Rule.is_mahjong(tiles)
        self.assertFalse(test)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
