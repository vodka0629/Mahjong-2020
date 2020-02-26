import unittest
from mahjong.player_ai import *
from mahjong.mj_set import MjSet
from mahjong.rule import Rule


class PlayerAiTestCase(unittest.TestCase):
    def test_player_ai_base(self):
        mj_set = MjSet()
        ai = PlayerAi("貂蝉")
        for _ in range(13):
            ai.draw(mj_set)
        self.assertEqual(len(ai.concealed), 13)

        mj_set.shuffle()
        for _ in range(10):
            ai.draw(mj_set)
            tile = ai.decide_discard()
            self.assertIsNotNone(tile)
            ai.discard(tile)

        self.assertEqual(len(ai.concealed), 13)
        self.assertEqual(len(ai.discarded), 10)

    def test_ai_mahjong(self):
        mj_set = MjSet()
        ai = PlayerAi("西施")
        mj_set.shuffle()
        for _ in range(13):
            ai.draw(mj_set)
        ai.sort_concealed()

        mj_set.shuffle()
        mahjong = False
        for _ in range(100):
            tile = ai.draw(mj_set)
            if Rule.is_mahjong(ai.concealed):
                mahjong = True
                break
            tile = ai.decide_discard()
            ai.discard(tile)
            ai.sort_concealed()

        # self.assertTrue(mahjong)
        self.assertGreater(len(ai.concealed), 0)
        # print("concealed: " + Rule.convert_tiles_to_str(ai.concealed))






def main():
    unittest.main()


if __name__ == '__main__':
    main()
