import unittest

from mahjong.calc import *
from mahjong.expose import Expose
from mahjong.mj_set import MjSet


class CalcTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        MjSet.generate_dictionary()

    def test_calc_1(self):
        self.assertTrue(MjSet.dictionary != None)
        flowers = [610, 620, 630, 640, 710, 720, 730, 740, ]
        tiles = Rule.convert_arr_to_tiles(flowers)
        calc = Calc(flowers=tiles)
        test = calc.花牌()
        should_be = ('花牌', 8, [])
        self.assertEqual(test, should_be)

    def test_calc_2(self):
        flowers = []
        calc = Calc(flowers=flowers, by_self=True)
        test = calc.自摸()
        should_be = ('自摸', 1, [])
        self.assertEqual(test, should_be)

    def test_calc_3(self):
        flowers = []
        arr = [101, 102, 103, 104, 105, 106, 109, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.单钓g(groups[0])
        should_be = ('单钓', 1, [])
        self.assertEqual(test, should_be)

    def test_calc_4(self):
        flowers = []
        arr = [101, 102, 103, 105, 106, 109, 109, 104, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.单钓g(groups[0])
        should_be = ('单钓', 1, [])
        self.assertNotEqual(test, should_be)

    def test_calc_5(self):
        flowers = []
        arr = [103, 105, 106, 106, 104]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.坎张g(groups[0])
        should_be = ('坎张', 1, [])
        self.assertEqual(test, should_be)

        arr = [101, 102, 103, 109, 109, 104, 106, 105, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.坎张g(groups[0])
        should_be = ('坎张', 1, [])
        self.assertEqual(test, should_be)

        arr = [510, 510, 103, 103, 103, 104, 106, 105, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.坎张g(groups[0])
        should_be = ('坎张', 1, [])
        self.assertEqual(test, should_be)

        arr = [510, 510, 103, 103, 103, 105, 106, 107, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.坎张g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_6(self):
        flowers = []
        arr = [101, 102, 106, 106, 103]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.边张g(groups[0])
        should_be = ('边张', 1, [])
        self.assertEqual(test, should_be)

        MjSet.generate_dictionary()
        flowers = []
        arr = [510, 510, 105, 106, 107, 108, 109, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.边张g(groups[0])
        should_be = False  # 听多张
        self.assertEqual(test, should_be)

        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.边张g(groups[0])
        should_be = ('边张', 1, [])
        self.assertEqual(test, should_be)

    def test_calc_7(self):
        flowers = []
        arr = [510, 510]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        test = calc.无字()
        should_be = ('无字', 1, [])
        self.assertNotEqual(test, should_be)

        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        test = calc.无字()
        should_be = ('无字', 1, [])
        self.assertEqual(test, should_be)

        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose])
        test = calc.无字()
        should_be = ('无字', 1, [])
        self.assertEqual(test, should_be)

        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose])
        test = calc.无字()
        should_be = ('无字', 1, [])
        self.assertNotEqual(test, should_be)

    def test_calc_8(self):
        flowers = []
        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose])
        test = calc.缺一门()
        should_be = ('缺一门', 1, [])
        self.assertEqual(test, should_be)

        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose])
        test = calc.缺一门()
        should_be = ('缺一门', 1, [])
        self.assertNotEqual(test, should_be)

    def test_calc_9(self):
        flowers = []
        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose])
        test = calc.明杠()
        should_be = ('明杠', 1)
        self.assertNotEqual(test, should_be)

        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose])
        test = calc.明杠()
        should_be = ('明杠', 1, [])
        self.assertEqual(test, should_be)

        arr = [101, 102, 103, 106, 106, 208, 209, 207]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.明杠()
        should_be = ('明杠', 2, [])
        self.assertEqual(test, should_be)

    def test_calc_10(self):
        flowers = []
        arr = [101, 101, 101, 109, 109, 108, 107, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.幺九刻g(groups[0])
        should_be = ('幺九刻', 3, [])
        self.assertEqual(test, should_be)

        arr = [101, 101, 101, 109, 109, 109, 107, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.幺九刻g(groups[0])
        should_be = ('幺九刻', 4, [])
        self.assertEqual(test, should_be)

        arr = [101, 101, 101, 109, 109, 109, 107, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.幺九刻g(groups[0])
        should_be = ('幺九刻', 4, [])
        self.assertEqual(test, should_be)

        # 幺九刻，不包含门风刻，圈风刻
        arr = [101, 101, 101, 530, 530, 530, 107, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3], prevailing_wind='东')
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.幺九刻g(groups[0])
        should_be = ('幺九刻', 3, [])
        self.assertEqual(test, should_be)

        arr = [101, 101, 101, 530, 530, 530, 107, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3], prevailing_wind='东',
                    winner_position='西')
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.幺九刻g(groups[0])
        should_be = ('幺九刻', 2, [])
        self.assertEqual(test, should_be)

    def test_get_best_mahjong_melds(self):
        arr = [101, 101, 101,
               102, 103, 104, 105, 106, 107, 108,
               109, 109, 109,
               105]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=[], by_self=True, concealed=tiles, exposed=[])
        test = calc.get_mahjong_combins()
        should_be = [[[101, 101, 101], [102, 103, 104], [106, 107, 108], [109, 109, 109], [105, 105]]]
        self.assertEqual(test, should_be)

        arr = [101, 101, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=[], by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.get_mahjong_combins()
        should_be = [[[101, 101], [301, 301, 301]]]
        self.assertEqual(test, should_be)

        arr = [101, 101, 101, 102, 102, 102, 103, 103, 103, 104, 104]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=[], by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.get_mahjong_combins()
        should_be = [
            [[101, 102, 103], [101, 102, 103], [101, 102, 103], [104, 104], [301, 301, 301]],
            [[101, 102, 103], [102, 103, 104], [102, 103, 104], [101, 101], [301, 301, 301]],
            [[101, 101, 101], [102, 102, 102], [103, 103, 103], [104, 104], [301, 301, 301]],
        ]
        self.assertEqual(test, should_be)

    def test_get_best_mahjong_melds_by_suit_group(self):
        arr = [101, 101, 101, 102, 102, 102, 103, 103, 103, 104, 104]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 301, 301]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=[], by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group()
        should_be = [
            {100: [[1, 2, 3], [1, 2, 3], [1, 2, 3], [4, 4]], 300: [[1, 1, 1]]},
            {100: [[1, 2, 3], [2, 3, 4], [2, 3, 4], [1, 1]], 300: [[1, 1, 1]]},
            {100: [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4]], 300: [[1, 1, 1]]}
        ]
        self.assertTrue(should_be, groups)

    def test_calc_11(self):
        flowers = []
        arr = [101, 102, 103, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [307, 308, 309]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.老少副g(groups[0])
        should_be = (('老少副', 1, []))
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 102, 103, 107, 108, 109, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [307, 308, 309]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.老少副g(groups[0])
        should_be = (('老少副', 2, []))
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 101, 107, 108, 109, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [304, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [307, 308, 309]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.老少副g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_12(self):
        flowers = []
        arr = [101, 102, 103, 105, 106, 107, 108, 108]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [304, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [305, 306, 307]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.连六g(groups[0])
        should_be = ('连六', 1, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [107, 109, 108, 105, 104, 106, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [304, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [305, 306, 307]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.连六g(groups[0])
        should_be = ('连六', 2, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [107, 109, 106, 105, 104, 106, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [304, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [305, 306, 307]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.连六g(groups[0])
        should_be = ('连六', 1, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [107, 109, 106, 105, 104, 106, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [204, 202, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [305, 306, 307]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.连六g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_13(self):
        flowers = []
        arr = [102, 103, 104, 105, 104, 106, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [302, 303, 304]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [302, 303, 304]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.喜相逢g(groups[0])
        should_be = ('喜相逢', 1, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [102, 103, 104, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [302, 303, 304]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.喜相逢g(groups[0])
        should_be = ('喜相逢', 2, [])
        self.assertEqual(test, should_be)

    def test_calc_14(self):
        flowers = []
        arr = [101, 102, 103, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [302, 303, 304]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [302, 303, 304]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一般高g(groups[0])
        should_be = ('一般高', 2, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 102, 103, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [305, 303, 304]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [302, 303, 304]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一般高g(groups[0])
        should_be = ('一般高', 1, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 101, 104, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [107, 108, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一般高g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 102, 103, 104, 104]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr4 = [410, 410, 410]
        tiles4 = Rule.convert_arr_to_tiles(arr4)
        expose4 = Expose(expose_type='exposed pong', inners=tiles4, outer=None, outer_owner=None)
        arr2 = [306, 307, 308]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [307, 308, 309]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose4, expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一般高g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_15(self):
        flowers = []
        arr = [101, 102, 103, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [302, 303, 304]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [302, 303, 304]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        arr = calc.convert_tiles_to_arr(with_exposed=True)
        should_be = [101, 102, 103, 101, 102, 103, 410, 410, 302, 303, 304, 302, 303, 304]
        self.assertEqual(should_be, arr)

    def test_calc_16(self):
        flowers = []
        arr = [101, 102, 103, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [302, 303, 304]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [302, 303, 304]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.断幺()
        should_be = False
        self.assertEqual(should_be, test)

        flowers = []
        arr = [104, 102, 103, 208, 208]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [302, 303, 304]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [302, 303, 304]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.断幺()
        should_be = ('断幺', 2, ['无字'])
        self.assertEqual(should_be, test)

    def test_calc_17(self):
        flowers = []
        arr = [101, 102, 103, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [209, 209, 209, 209]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.暗杠()
        should_be = ('暗杠', 4, [])
        self.assertEqual(should_be, test)

    def test_calc_18(self):
        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [209, 209, 209, 209]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.双暗刻g(groups[0])
        should_be = ('双暗刻', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [209, 209, 209, 209]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.双暗刻g(groups[0])
        should_be = ('双暗刻', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [209, 209, 209]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.双暗刻g(groups[0])
        should_be = False
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 102, 102, 102, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [209, 209, 209, 209]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.双暗刻g(groups[0])
        should_be = ('双暗刻', 2, [])
        self.assertEqual(should_be, test)

    def test_calc_19(self):
        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.双同刻g(groups[0])
        should_be = ('双同刻', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 102, 102, 102, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [202, 202, 202]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed pong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.双同刻g(groups[0])
        should_be = ('双同刻', 4, [])
        self.assertEqual(should_be, test)

    def test_calc_20(self):
        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.四归一()
        should_be = ('四归一', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 102, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.四归一()
        should_be = False
        self.assertEqual(should_be, test)

    def test_calc_21(self):
        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.平和g(groups[0])
        should_be = False
        self.assertEqual(should_be, test)

        flowers = []
        arr = [510, 510, 510, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.平和g(groups[0])
        should_be = False
        self.assertEqual(should_be, test)

        flowers = []
        arr = [209, 209, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [206, 206, 206]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed pong', inners=tiles3, outer=None, outer_owner=None)
        arr4 = [101, 102, 103]
        tiles4 = Rule.convert_arr_to_tiles(arr4)
        expose4 = Expose(expose_type='exposed chow', inners=tiles4, outer=None, outer_owner=None)
        arr5 = [104, 105, 106]
        tiles5 = Rule.convert_arr_to_tiles(arr5)
        expose5 = Expose(expose_type='exposed chow', inners=tiles5, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose4, expose5])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.平和g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.平和g(groups[0])
        should_be = False
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.平和g(groups[0])
        should_be = False
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 102, 103, 102, 103, 104, 102, 102]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [205, 206, 207]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.平和g(groups[0])
        should_be = ('平和', 2, ['无字'])
        self.assertEqual(should_be, test)

        arr = [101, 102, 103, 104, 105, 106,
               107, 108, 109, 202, 203, 204,
               303, 303]
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.平和g(groups[0])
        should_be = ('平和', 2, ['无字'])
        self.assertEqual(should_be, test)

    def test_calc_22(self):
        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [205, 205, 205, 205, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=False, concealed=tiles, exposed=[expose2])
        test = calc.门前清()
        should_be = ('门前清', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=False, concealed=tiles, exposed=[])
        test = calc.门前清()
        should_be = ('门前清', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.门前清()
        should_be = False
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [205, 205, 205, 205, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.门前清()
        should_be = False
        self.assertEqual(should_be, test)

    def test_calc_23(self):
        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510, 510, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2], winner_position='东')
        test = calc.门风刻()
        should_be = ('门风刻', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510, 510, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2], winner_position='西')
        test = calc.门风刻()
        should_be = False
        self.assertEqual(should_be, test)

    def test_calc_24(self):
        flowers = []
        arr = [510, 510, 510, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [520, 520, 520, 520, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2], winner_position='北',
                    prevailing_wind='东')
        test = calc.圈风刻()
        should_be = ('圈风刻', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510, 510, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2], winner_position='东',
                    prevailing_wind='西')
        test = calc.圈风刻()
        should_be = False
        self.assertEqual(should_be, test)

    def test_calc_25(self):
        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [520, 520, 520, 520, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2], winner_position='北',
                    prevailing_wind='东')
        test = calc.箭刻()
        should_be = ('箭刻', 2, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [420, 420, 420, 420, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2], winner_position='北',
                    prevailing_wind='东')
        test = calc.箭刻()
        should_be = ('箭刻', 4, [])
        self.assertEqual(should_be, test)

    def test_calc_26(self):
        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 201, 201]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [520, 520, 520, 520, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        left = [301, 302, 303, 304, 305]
        tiles_left = Rule.convert_arr_to_tiles(left)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2], left=tiles_left)
        test = calc.和绝张()
        should_be = ('和绝张', 4, [])
        self.assertEqual(should_be, test)

    def test_calc_27(self):
        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 201, 201]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [520, 520, 520, 520, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [520, 520, 520, 520, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.双明杠()
        should_be = ('双明杠', 4, [])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 201, 201]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [520, 520, 520, 520, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [520, 520, 520, 520, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.双明杠()
        should_be = False
        self.assertEqual(should_be, test)

    def test_calc_27(self):
        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 201, 201]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.不求人()
        should_be = ('不求人', 4, ['自摸'])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 201, 201]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=False, concealed=tiles, exposed=[])
        test = calc.不求人()
        should_be = False
        self.assertEqual(should_be, test)

        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 201, 201]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [520, 520, 520, 520, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.不求人()
        should_be = ('不求人', 4, ['自摸'])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [410, 410, 410, 101, 102, 103, 201, 201]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [520, 520, 520, 520, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.不求人()
        should_be = False
        self.assertEqual(should_be, test)

    def test_calc_28(self):
        flowers = []
        arr = [510, 510, 105, 106, 107, 108, 109, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全带幺g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 101, 102, 103, 108, 109, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles)
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全带幺g(groups[0])
        should_be = ('全带幺', 4, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 101, 102, 103, 108, 109, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [520, 520, 520, 520, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全带幺g(groups[0])
        should_be = ('全带幺', 4, [])
        self.assertEqual(test, should_be)

    def test_calc_29(self):
        MjSet.generate_dictionary()
        flowers = []
        arr = [410, 410, 410, 106, 107, 108, 109, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [420, 420, 420, 420, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.双箭刻g(groups[0])
        should_be = ('双箭刻', 6, ['箭刻'])
        self.assertEqual(test, should_be)

        MjSet.generate_dictionary()
        flowers = []
        arr = [410, 410, 410, 106, 107, 108, 109, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.双箭刻g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_30(self):
        flowers = []
        arr = [410, 410, 410, 106, 107, 108, 109, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [420, 420, 420, 420, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [410, 410, 410, 410, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.双暗杠()
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [410, 410, 410, 106, 107, 108, 109, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [420, 420, 420, 420, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [410, 410, 410, 410, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.双暗杠()
        should_be = ('双暗杠', 6, [])
        self.assertEqual(test, should_be)

    def test_calc_31(self):
        flowers = []
        arr = [101, 101]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [420, 420, 420, 420, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [410, 410, 410, 410, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.全求人()
        should_be = False  # ('双暗杠', 6, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [420, 420, 420, 420, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [410, 410, 410, 410, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.全求人()
        should_be = ('全求人', 6, ['单钓'])
        self.assertEqual(test, should_be)

    def test_calc_32(self):
        flowers = []
        arr = [101, 101]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [420, 420, 420, 420, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [410, 410, 410, 410, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.五门齐g(groups[0])
        should_be = False  # ('五门齐', 6, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 201, 202, 203, 301, 302, 303, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [420, 420, 420, 420, ]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed pong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.五门齐g(groups[0])
        should_be = ('五门齐', 6, [])
        self.assertEqual(test, should_be)

    def test_calc_33(self):
        flowers = []
        arr = [101, 101, 102, 103, 104, 103, 104, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [302, 303, 304]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [204, 205, 206]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色三步高g(groups[0])
        should_be = ('三色三步高', 6, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 102, 103, 104, 103, 104, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [204, 205, 206]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色三步高g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_34(self):
        flowers = []
        arr = [101, 101, 102, 103, 104, 103, 104, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [410, 410, 410]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed pong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.混一色g(groups[0])
        should_be = ('混一色', 6, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 102, 103, 104, 103, 104, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [510, 510, 510]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed pong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.混一色g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [202, 203, 205, 206, 207, 205, 206, 207, 209, 209, 209, 420, 420, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.混一色g(groups[0])
        should_be = ('混一色', 6, [])
        self.assertEqual(test, should_be)

    def test_calc_35(self):
        flowers = []
        arr = [101, 101, 101, 103, 103, 103, 102, 102, 102, 520, 520]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.碰碰和g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 101, 103, 103, 103, 102, 102, 102, 520, 520]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510, 510]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.碰碰和g(groups[1])
        should_be = ('碰碰和', 6, [])
        self.assertEqual(test, should_be)

    def test_calc_37(self):
        flowers = []
        arr = [101, 101, 101, 103, 103, 103, 102, 102, 102, 520, 520]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.海底捞月()
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 101, 103, 103, 103, 102, 102, 102, 520, 520]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=False, concealed=tiles, exposed=[expose2])
        test = calc.海底捞月()
        should_be = ('海底捞月', 8, [])
        self.assertEqual(test, should_be)

    def test_calc_38(self):
        flowers = []
        arr = [101, 101, 101, 103, 103, 103, 102, 102, 102, 520, 520]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=False, concealed=tiles, exposed=[expose2])
        test = calc.妙手回春()
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 101, 103, 103, 103, 102, 102, 102, 520, 520]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.妙手回春()
        should_be = ('妙手回春', 8, [])
        self.assertEqual(test, should_be)

    def test_calc_39(self):
        flowers = []
        arr = [101, 102, 103, 103, 104, 105, 520, 520, 307, 308, 309]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [202, 202, 202]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr_left = arr + arr2 + [309]
        left = Rule.convert_arr_to_tiles(arr_left)
        calc = Calc(flowers=flowers, by_self=False, concealed=tiles, exposed=[expose2], left=left)
        test = calc.calc()
        should_be = [('无番和', 8, []), ('', '', []), ('总计', 8, [])]
        self.assertEqual(test, should_be)

    def test_calc_40(self):
        flowers = []
        arr = [101, 101, 101, 202, 202, 202, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [303, 303, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色三节高g(groups[0])
        should_be = ('三色三节高', 8, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [104, 104, 104, 202, 202, 202, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [303, 303, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色三节高g(groups[0])
        should_be = ('三色三节高', 8, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [204, 204, 204, 202, 202, 202, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [303, 303, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色三节高g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_41(self):
        flowers = []
        arr = [103, 104, 105, 203, 204, 205, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [303, 304, 305]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色三同顺g(groups[0])
        should_be = ('三色三同顺', 8, ['喜相逢'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [103, 104, 105, 203, 204, 205, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [304, 304, 304]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色三同顺g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [203, 204, 205, 203, 204, 205, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [303, 304, 305]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色三同顺g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_41(self):
        flowers = []
        arr = [202, 203, 204, 208, 208, 208, 209, 209]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [430, 430, 430]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.推不倒()
        should_be = ('推不倒', 8, ['缺一门'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [202, 203, 204, 208, 208, 208, 109, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [430, 430, 430]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.推不倒()
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [202, 203, 204, 208, 208, 208, 510, 510]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [430, 430, 430]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        test = calc.推不倒()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_42(self):
        flowers = []
        arr = [101, 102, 103, 204, 205, 206, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [307, 308, 309]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.花龙g(groups[0])
        should_be = ('花龙', 8, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 102, 103, 204, 205, 206, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [207, 208, 209]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.花龙g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_43(self):
        flowers = []
        arr = [520, 520, 520, 530, 530, 530, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [540, 540, 540]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三风刻()
        should_be = ('三风刻', 12, ['幺九刻'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [520, 520, 520, 530, 530, 530, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [430, 430, 430]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三风刻()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_44(self):
        flowers = []
        arr = [101, 101, 101, 102, 102, 102, 304, 304]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [203, 203, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.小于五()
        should_be = ('小于五', 12, ['无字'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 101, 102, 102, 102, 510, 510]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [203, 203, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.小于五()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_45(self):
        flowers = []
        arr = [106, 106, 106, 107, 107, 107, 308, 308]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [209, 209, 209]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.大于五()
        should_be = ('大于五', 12, ['无字'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [106, 106, 106, 107, 107, 107, 308, 308]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.大于五()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_45(self):
        flowers = []
        arr = [201, 204, 207, 102, 105, 108, 308, 308, 105, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [303, 306, 309]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.组合龙()
        should_be = ('组合龙', 12, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 204, 207, 102, 105, 108, 303, 306, 309, 308, 308, 410, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.组合龙()
        should_be = ('组合龙', 12, [])
        self.assertEqual(test, should_be)

    def test_calc_46(self):
        flowers = []
        arr = [201, 204, 207, 102, 105, 108, 510, 520, 530, 420, 430, 303, 306, 309]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全不靠()
        should_be = ('全不靠', 12, ['五门齐', '不求人', '门前清'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 204, 207, 102, 105, 108, 510, 520, 530, 420, 430]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [303, 306, 309]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全不靠()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_47(self):
        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [209, 209, 209, 209]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [208, 208, 208, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三暗刻g(groups[0])
        should_be = ('三暗刻', 16, ['双暗刻'])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 102, 102, 102, 103, 103, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三暗刻g(groups[1])
        should_be = ('三暗刻', 16, ['双暗刻'])
        self.assertEqual(should_be, test)

    def test_calc_48(self):
        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [301, 301, 301]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed pong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三同刻g(groups[0])
        should_be = ('三同刻', 16, ['双同刻'])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [101, 101, 101, 101, 102, 103, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [301, 302, 303]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed pong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三同刻g(groups[0])
        should_be = False
        self.assertEqual(should_be, test)

    def test_calc_49(self):
        flowers = []
        arr = [103, 104, 105, 204, 205, 206, 305, 305]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [105, 106, 107]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全带五g(groups[0])
        should_be = ('全带五', 16, ['断幺', '无字'])
        self.assertEqual(should_be, test)

        flowers = []
        arr = [103, 104, 105, 204, 205, 206, 304, 304]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [105, 106, 107]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全带五g(groups[0])
        should_be = False
        self.assertEqual(should_be, test)

    def test_calc_50(self):
        flowers = []
        arr = [101, 101, 104, 105, 106]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [102, 103, 104]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [103, 104, 105]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色三步高g(groups[0])
        should_be = ('一色三步高', 16, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 204, 205, 206]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [202, 203, 204]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [206, 207, 208]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色三步高g(groups[0])
        should_be = ('一色三步高', 16, [])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 204, 205, 206]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [202, 203, 204]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色三步高g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_51(self):
        flowers = []
        arr = [105, 105, 201, 202, 203, 307, 308, 309]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 208, 209]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色双龙会g(groups[0])
        should_be = ('三色双龙会', 16, ["平和", "老少副", "喜相逢", "无字"])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [205, 205, 201, 202, 203, 307, 308, 309]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 208, 209]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色双龙会g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [104, 104, 201, 202, 203, 307, 308, 309]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [301, 302, 303]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 208, 209]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.三色双龙会g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_52(self):
        flowers = []
        arr = [201, 202, 203, 202, 203, 204, 308, 308]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [204, 205, 206]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 208, 209]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.清龙g(groups[0])
        should_be = ('清龙', 16, ["连六", "老少副"])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 202, 203, 202, 203, 204, 308, 308]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [204, 205, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 208, 209]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.清龙g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_53(self):
        flowers = []
        arr = [201, 202, 203, 102, 103, 101, 302, 302]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 202, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [101, 102, 103]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全小()
        should_be = ('全小', 24, ['小于五', '无字'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 202, 203, 102, 103, 101, 510, 510]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 202, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [101, 102, 103]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全小()
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 202, 203, 202, 203, 204, 105, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 202, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [101, 102, 103]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全小()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_54(self):
        flowers = []
        arr = [204, 205, 206, 106, 106, 106, 305, 305]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [204, 205, 206]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [104, 105, 106]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全中()
        should_be = ('全中', 24, ['断幺'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [204, 205, 206, 106, 106, 106, 302, 302]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [204, 205, 206]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [104, 105, 106]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全中()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_55(self):
        flowers = []
        arr = [207, 207, 207, 107, 108, 109, 309, 309]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [208, 208, 208]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [109, 109, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed pong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全大()
        should_be = ('全大', 24, ['大于五', '无字'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [207, 207, 207, 107, 108, 109, 309, 309]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [208, 208, 208]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [101, 101, 101]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed pong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        test = calc.全大()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_56(self):
        flowers = []
        arr = [201, 201, 201, 102, 103, 101, 302, 302]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [203, 203, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [202, 202, 202, 202]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色三节高g(groups[0])
        should_be = ('一色三节高', 24, ['一色三同顺'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 201, 201, 102, 103, 101, 302, 302]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [204, 204, 204]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [202, 202, 202, 202]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色三节高g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_57(self):
        flowers = []
        arr = [201, 201, 201, 102, 103, 101, 302, 302]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [203, 203, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [202, 202, 202, 202]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色三同顺g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 201, 201, 203, 204, 205, 302, 302]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [203, 204, 205]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [203, 204, 205]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色三同顺g(groups[0])
        should_be = ('一色三同顺', 24, ['一色三节高'])
        self.assertEqual(test, should_be)

    def test_calc_58(self):
        flowers = []
        arr = [201, 201, 201, 202, 203, 201, 209, 209]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [203, 203, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [202, 202, 202, 202]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.清一色g(groups[0])
        should_be = ('清一色', 24, ['无字'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 201, 201, 202, 203, 201, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [203, 203, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [202, 202, 202, 202]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.清一色g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_59(self):
        flowers = []
        arr = [202, 202, 202, 204, 204, 204, 510, 510]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [308, 308, 308, 308]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [106, 106, 106, 106]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全双刻g(groups[0])
        should_be = ('全双刻', 24, ['碰碰和', '断幺', '无字'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 202, 203, 204, 204, 204, 510, 510]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [308, 308, 308, 308]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [106, 106, 106, 106]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全双刻g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

        flowers = []
        arr = [203, 203, 203, 204, 204, 204, 510, 510]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [308, 308, 308, 308]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [106, 106, 106, 106]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.全双刻g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_60(self):
        flowers = []
        arr = [510, 520, 530, 540, 410, 420, 430, 301, 304, 307, 202, 205, 103, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.七星不靠()
        should_be = ('七星不靠', 24, ['全不靠', '五门齐', '不求人', '门前清'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [520, 530, 540, 410, 420, 430, 301, 304, 307, 202, 205, 103, 109, 106]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.七星不靠()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_61(self):
        flowers = []
        arr = [510, 520, 530, 540, 410, 420, 430, 510, 520, 530, 540, 410, 420, 430, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.七对()
        should_be = ('七对', 24, ['不求人', '门前清', '单钓'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 520, 530, 540, 410, 420, 430, 510, 520, 530, 540, 410, 420, 410, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.七对()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_62(self):
        flowers = []
        arr = [103, 102, 101, 202, 203, 204, 301, 301, 301, 410, 410, 410, 420, 420, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.calc()
        should_be = ('箭刻', 2, [])
        self.assertTrue(should_be in test)

    def test_calc_63(self):
        flowers = []
        arr = [103, 102, 101, 202, 203, 204, 301, 301, 301, 410, 410, 109, 108, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.calc()
        dont = ('单钓', 1, [])
        self.assertTrue(dont not in test)

    def test_calc_64(self):
        flowers = []
        arr = [103, 102, 101, 202, 203, 204, 301, 301, 301, 410, 410, 109, 108, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        test = calc.calc()
        dont = ('单钓', 1, [])
        self.assertTrue(dont not in test)

    def test_calc_65(self):
        flowers = []
        arr = [101, 101, 101, 209, 209, 209, 301, 301, 301, 410, 410, 520, 520, 520]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.混幺九g(groups[0])
        should_be = ('混幺九', 32, ['碰碰和', '全带幺', '幺九刻'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 102, 103, 209, 209, 209, 301, 301, 301, 410, 410, 520, 520, 520]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.混幺九g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_66(self):
        flowers = []
        arr = [101, 101]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [308, 308, 308, 308]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [106, 106, 106, 106]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        arr4 = [101, 101, 101, 101]
        tiles4 = Rule.convert_arr_to_tiles(arr4)
        expose4 = Expose(expose_type='exposed kong on exposed pong', inners=tiles4, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose4])
        test = calc.三杠()
        should_be = ('三杠', 32, [])
        self.assertEqual(test, should_be)

    def test_calc_67(self):
        flowers = []
        arr = [101, 101, 307, 307, 307, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [308, 308, 308, 308]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [306, 306, 306, 306]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        arr4 = [309, 309, 309, 309]
        tiles4 = Rule.convert_arr_to_tiles(arr4)
        expose4 = Expose(expose_type='exposed kong on exposed pong', inners=tiles4, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose4])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色四节高g(groups[0])
        should_be = ('一色四节高', 48, ['一色三同顺', '一色三节高', '碰碰和'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 101, 307, 307, 307, 306, 306, 306, 308, 308, 308, 309, 309, 309]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色四节高g(groups[0])
        should_be = ('一色四节高', 48, ['一色三同顺', '一色三节高', '碰碰和'])
        self.assertEqual(test, should_be)

    def test_calc_68(self):
        flowers = []
        arr = [101, 101, 104, 105, 106, 105, 106, 107]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [102, 103, 104]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [103, 104, 105]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色四步高g(groups[0])
        should_be = ('一色四步高', 32, ['一色三步高', '连六', '老少副'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [430, 430, 101, 102, 103, 103, 104, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [105, 106, 107]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [107, 108, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色四步高g(groups[0])
        should_be = ('一色四步高', 32, ['一色三步高', '连六', '老少副'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [430, 430, 201, 202, 203, 103, 104, 105]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [105, 106, 107]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [107, 108, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色四步高g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_69(self):
        flowers = []
        arr = [101, 101, 102, 103, 104, 102, 103, 104]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [102, 103, 104]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [102, 103, 104]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色四同顺g(groups[1])
        should_be = ('一色四同顺', 48, ['一色三同顺', '一色三节高', '四归一', '一般高'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 102, 103, 104, 102, 103, 104]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [102, 103, 104]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [102, 103, 104]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色四同顺g(groups[0])
        should_be = ('一色四同顺', 48, ['一色三同顺', '一色三节高', '四归一', '一般高'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 102, 103, 104, 410, 410, 410, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [102, 103, 104]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [102, 103, 104]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色四同顺g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_70(self):
        flowers = []
        arr = [201, 202, 203, 207, 208, 209, 205, 205]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 202, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 208, 209, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色双龙会g(groups[0])
        should_be = ('一色双龙会', 64, ['七对', '清一色', '平和', '一般高', '老少副', '无字'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 202, 203, 207, 208, 209, 305, 305]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 202, 203]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='exposed chow', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 208, 209, ]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed chow', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.一色双龙会g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_71(self):
        flowers = []
        arr = [209, 209]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 207, 207, 207]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        arr2 = [202, 202, 202, 202]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose4 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [203, 203, 203, 203]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose4, expose5])
        test = calc.四暗刻()
        should_be = ('四暗刻', 64, ['碰碰和', '不求人', '门前清'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [209, 209]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [207, 207, 207, 207]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        arr2 = [202, 202, 202, 202]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose4 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [203, 203, 203, 203]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose4, expose5])
        test = calc.四暗刻()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_72(self):
        flowers = []
        arr = [510, 510, 530, 530, 530, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [410, 410, 410, 410]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [430, 430, 430, 430]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [540, 540, 540, 540]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose5])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.字一色g(groups[0])
        should_be = ('字一色', 64, ['碰碰和', '全带幺', '幺九刻'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 203, 203, 203, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [410, 410, 410, 410]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [430, 430, 430, 430]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [540, 540, 540, 540]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose5])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.字一色g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_73(self):
        flowers = []
        arr = [420, 420, 530, 530, 530, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [410, 410, 410, 410]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [430, 430, 430, 430]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [540, 540, 540, 540]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose5])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.小三元g(groups[0])
        should_be = ('小三元', 64, ['双箭刻', '箭刻'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 530, 530, 530, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [410, 410, 410, 410]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [430, 430, 430, 430]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.小三元g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_74(self):
        flowers = []
        arr = [420, 420, 420, 530, 530, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510, 510]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [520, 520, 520, 520]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [540, 540, 540, 540]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose5])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.小四喜g(groups[0])
        should_be = ('小四喜', 64, ['三风刻', '幺九刻'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [420, 420, 530, 530, 530, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [510, 510, 510, 510]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [520, 520, 520, 520]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [540, 540, 540, 540]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose5])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.小四喜g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_75(self):
        flowers = []
        arr = [101, 101, 101, 309, 309, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [301, 301, 301, 301]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [109, 109, 109, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose5])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.清幺九g(groups[0])
        should_be = ('清幺九', 64, ['碰碰和', '全带幺', '双同刻', '幺九刻', '无字'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 309, 309, 309, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [301, 301, 301, 301]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [109, 109, 109, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose5])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.清幺九g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_76(self):
        flowers = []
        arr = [101, 109, 201, 209, 301, 309, 410, 420, 430, 510, 520, 530, 540, 540]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.十三幺()
        should_be = ('十三幺', 64, ['五门齐', '不求人', '门前清', '单钓'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [101, 109, 201, 209, 301, 309, 410, 420, 430, 510, 520, 530]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.十三幺()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_77(self):
        flowers = []
        arr = [102, 103, 104, 105, 106, 107, 108, 102, 103, 104, 105, 106, 107, 108]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.连七对()
        should_be = ('连七对', 88, ['清一色', '七对', '不求人', '门前清', '无字', '单钓'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [102, 103, 104, 105, 106, 107, 109, 102, 103, 104, 105, 106, 107, 109]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.连七对()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_78(self):
        flowers = []
        arr = [510, 510, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr2 = [309, 309, 309, 309]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose4 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [301, 301, 301, 301]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [109, 109, 109, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose4, expose5])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.四杠()
        should_be = ('四杠', 88, ['碰碰和', '单钓'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr2 = [309, 309, 309, 309]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose4 = Expose(expose_type='exposed kong on exposed pong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [301, 301, 301, 301]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [109, 109, 109, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose4, expose5])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.四杠()
        should_be = ('四杠', 88, ['碰碰和', '单钓'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 510, 309, 309, 309, ]
        tiles = Rule.convert_arr_to_tiles(arr)
        arr2 = [201, 201, 201, 201]
        tiles2 = Rule.convert_arr_to_tiles(arr2)
        expose2 = Expose(expose_type='concealed kong', inners=tiles2, outer=None, outer_owner=None)
        arr3 = [301, 301, 301, 301]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose3 = Expose(expose_type='exposed kong', inners=tiles3, outer=None, outer_owner=None)
        arr3 = [109, 109, 109, 109]
        tiles3 = Rule.convert_arr_to_tiles(arr3)
        expose5 = Expose(expose_type='concealed kong', inners=tiles3, outer=None, outer_owner=None)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[expose2, expose3, expose5])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.四杠()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_79(self):
        flowers = []
        arr = [201, 201, 201, 202, 203, 204, 205, 206, 207, 208, 209, 209, 209, 202]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.九莲宝灯()
        should_be = ('九莲宝灯', 88, ['清一色', '不求人', '门前清', '无字', '幺九刻'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [201, 201, 201, 202, 203, 204, 205, 206, 207, 208, 209, 209, 209, 302]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.九莲宝灯()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_80(self):
        flowers = []
        arr = [302, 303, 304, 302, 303, 304, 306, 306, 306, 308, 308, 308, 420, 420]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.绿一色()
        should_be = ('绿一色', 88, ['混一色'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [302, 303, 304, 302, 303, 304, 306, 306, 306, 308, 308, 308, 410, 410]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        # groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.绿一色()
        should_be = False
        self.assertEqual(test, should_be)

    def test_calc_81(self):
        flowers = []
        arr = [410, 420, 430, 410, 420, 430, 410, 420, 430, 102, 103, 104, 303, 303]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.大三元g(groups[0])
        should_be = ('大三元', 88, ['双箭刻', '箭刻'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [410, 420, 430, 410, 420, 430, 410, 420, 102, 103, 104, 303, 303, 303]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.大三元g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)
        
    def test_calc_82(self):
        flowers = []
        arr = [510, 520, 530, 540, 510, 520, 530, 540,510, 520, 530, 540, 303, 303]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.大四喜g(groups[0])
        should_be = ('大四喜', 88, ['三风刻', '碰碰和', '圈风刻', '门风刻', '幺九刻'])
        self.assertEqual(test, should_be)

        flowers = []
        arr = [510, 520, 530, 540, 510, 520, 530, 540,510, 520, 530, 303, 303, 303]
        tiles = Rule.convert_arr_to_tiles(arr)
        calc = Calc(flowers=flowers, by_self=True, concealed=tiles, exposed=[])
        groups = calc.get_mahjong_combins_by_suit_group(True)
        test = calc.大四喜g(groups[0])
        should_be = False
        self.assertEqual(test, should_be)

def main():
    unittest.main()


if __name__ == '__main__':
    main()
