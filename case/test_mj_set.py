import unittest
from mahjong.mj_set import MjSet


class MjSetTestCase(unittest.TestCase):
    def test_mj_set(self):
        mj_set = MjSet(flower=True)
        count = len(mj_set.tiles)
        self.assertEqual(count, 144)

        mj_set = MjSet(flower=False)
        count = len(mj_set.tiles)
        self.assertEqual(count, 136)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
