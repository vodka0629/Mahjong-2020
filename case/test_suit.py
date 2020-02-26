import unittest
from mahjong.suit import *


class SuitTestCase(unittest.TestCase):
    def test_suit(self):
        test = Suit.Suit
        self.assertEqual(len(test), 7)

        test = Suit.Dragon
        self.assertEqual(len(test), 3)

        test = Suit.Flower
        self.assertEqual(len(test), 4)

        test = Suit.Season
        self.assertEqual(len(test), 4)

        test = Suit.get_wind_by_index(0)
        self.assertEqual(test, '东')

    def test_get_next_wind(self):
        test = Suit.get_next_wind('北')
        self.assertEqual(test, '东')

        test = Suit.get_next_wind('东')
        self.assertEqual(test, '南')

    def test_before_wind(self):
        current = '东'
        test = Suit.get_next_wind(current)
        should_be = "南"
        self.assertEqual(should_be, test)
        test = Suit.get_before_wind(current)
        should_be = "北"
        self.assertEqual(should_be, test)

        current = '北'
        test = Suit.get_next_wind(current)
        should_be = "东"
        self.assertEqual(should_be, test)
        test = Suit.get_before_wind(current)
        should_be = "西"
        self.assertEqual(should_be, test)

def main():
    unittest.main()


if __name__ == '__main__':
    main()
