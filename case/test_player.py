import unittest
from mahjong.player import *
from mahjong.mj_set import *


class PlayerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pygame.mixer.init()

    def test_player(self):
        mj_set = MjSet()
        mj_set.shuffle()
        player = Player("向明")
        player.draw_stack(mj_set)
        test = player.concealed
        self.assertEqual(4, len(player.concealed))

    def test_exposed_kong(self):
        mj_set = MjSet()
        player = Player("向明")
        owner = Player("大乔")

        for _ in range(3):
            player.draw(mj_set)
        north = mj_set.draw()

        mj_set.shuffle()
        for _ in range(10):
            player.draw(mj_set)

        test = f'{north}'
        should_be = u'[北]'
        self.assertEqual(test, should_be)

        player.try_exposed_kong(north, owner, mj_set)
        should_be = u'[北],[北],[北],[北](大乔)'
        test = ','.join([f'{x}' for x in player.exposed])
        self.assertEqual(test, should_be)
        self.assertEqual(len(player.concealed), 11)

    def test_exposed_pong(self):
        mj_set = MjSet()
        player = Player("向明")
        owner = Player("大乔")

        for _ in range(2):
            player.draw(mj_set)
        north = mj_set.draw()

        mj_set.shuffle()
        for _ in range(11):
            player.draw(mj_set)

        test = f'{north}'
        should_be = u'[北]'
        self.assertEqual(test, should_be)

        player.try_exposed_pong(north, owner)
        should_be = u'exposed pong:[北],[北],[北](大乔)'
        test = (','.join([f'{x.expose_type}:{x}' for x in player.exposed]))
        self.assertEqual(test, should_be)
        self.assertEqual(len(player.concealed), 11)

    def test_exposed_chow(self):
        mj_set = MjSet()
        player = Player("向明")
        owner = Player("甄姬")
        for _ in range(2):
            for x in range(3):
                mj_set.draw_from_back()
            player.draw_from_back(mj_set)
        for x in range(3):
            mj_set.draw_from_back()
        sample = mj_set.draw_from_back()
        for _ in range(3):
            for x in range(3):
                mj_set.draw_from_back()
            player.draw_from_back(mj_set)

        mj_set.shuffle()
        for _ in range(6):
            player.draw(mj_set)
        should_be = u'[1万] [2万] [4万] [5万] [6万]'
        self.assertTrue(Rule.convert_tiles_to_str(player.concealed).index(should_be) == 0)
        should_be = u'[3万]'
        test = f'{sample}'
        self.assertEqual(should_be, test)
        player.try_exposed_chow(sample, owner)
        should_be = u'(甄姬)'
        test = ','.join([f'{x.expose_type}:{x}' for x in player.exposed])
        self.assertTrue(test.index(should_be) > 0)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
