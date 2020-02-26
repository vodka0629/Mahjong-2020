import unittest
from mahjong.mj_math import *
from mahjong.rule import Rule


class MjMathTestCase(unittest.TestCase):
    def test_mj_math(self):
        arr = [5, 5, 5]
        test = MjMath.is_111(arr)
        self.assertTrue(test)

        arr = [4, 4, 5]
        test = MjMath.is_111(arr)
        self.assertFalse(test)

        arr = [3, 4, 5]
        test = MjMath.is_123(arr)
        self.assertTrue(test)

        arr = [3, 3, 5]
        test = MjMath.is_123(arr)
        self.assertFalse(test)

        arr = [3, 3, 3, 3]
        test = MjMath.is_1111(arr)
        self.assertTrue(test)

        arr = [3, 3, 3]
        test = MjMath.is_1111(arr)
        self.assertFalse(test)

        arr = [3, 3, 3, 2]
        test = MjMath.is_1111(arr)
        self.assertFalse(test)

    def test_list_sub(self):
        list1 = [1, 2, 3, 2, 3, 4]
        list2 = [2, 4]
        arr = MjMath.list_sub(list1, list2)
        self.assertEqual(arr, [1, 3, 2, 3])

    def test_is_good_meld_arr(self):
        arr = [1, 2, 3,
               2, 3, 4,
               3, 4, 5,
               8, 8, 8]
        arr.sort()
        test = MjMath.is_good_meld_arr(arr)
        self.assertTrue(test)

        arr = [1, 2, 3,
               2, 3, 4,
               2, 3, 4,
               4, 5, 6]
        arr.sort()
        test = MjMath.is_good_meld_arr(arr)
        self.assertTrue(test)

        arr = [1, 2, 3,
               3, 4, 5,
               2, 3, 4,
               5, 6, 7]
        arr.sort()
        test = MjMath.is_good_meld_arr(arr)
        self.assertTrue(test)

        arr = [1, 2, 3,
               2, 3, 4,
               3, 4, 5,
               6, 6, 7]
        arr.sort()
        test = MjMath.is_good_meld_arr(arr)
        self.assertFalse(test)

        arr = [1, 2, 3,
               4, 5, 6,
               7, 8, 9,
               2, 2, 2]
        arr.sort()
        test = MjMath.is_good_meld_arr(arr)
        self.assertTrue(test)

    def test_remove_pair(self):
        arr = [1, 2, 3,
               2, 3, 4,
               3, 4, 5,
               8, 8, 8]
        pair_keys = MjMath.get_pair_keys(arr)
        self.assertEqual(pair_keys, [2, 3, 4, 8])
        arr.sort()
        for x in pair_keys:
            remain = MjMath.remove_pair_from_arr(arr, x)
            test = [x, x] + remain
            test.sort()
            self.assertEqual(test, arr)

    def test_get_pair_key(self):
        arr = [1, 2, 3,
               2, 3, 4,
               3, 4, 5,
               8, 8, 8]
        pair_keys = MjMath.get_pair_keys(arr)
        self.assertEqual(pair_keys, [2, 3, 4, 8])

    def test_is_good_hand(self):
        arr = [1, 2, 3,
               2, 3, 4,
               3, 4, 5,
               8, 8, 8,
               9, 9]
        arr.sort()
        test = MjMath.is_good_concealed(arr)
        self.assertTrue(test)

    def test_not_in_pair(self):
        arr = [1, 2, 2, 4, 3, 1, 7, 9]
        test = MjMath.get_not_in_pair(arr)
        self.assertEqual(test, {9, 3, 4, 7})

    def test_get_melds_from_arr(self):
        arr = [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9]  # 九宝莲灯
        combins = MjMath.get_best_meld_combins_from_arr(arr)
        should_be = '''[[], [1, 1, 1], [3, 4, 5], [6, 7, 8], [9, 9, 9]]
[[], [1, 1, 1], [2, 3, 4], [5, 6, 7], [9, 9, 9]]
[[], [1, 1, 1], [2, 3, 4], [6, 7, 8], [9, 9, 9]]'''
        test = "\n".join([f'{x}' for x in combins])
        self.assertEqual(test, should_be)

        arr = [50, 50, 50, 60, 60, 60, 70, 70, 70, 80, 80]  # 小四喜
        combins = MjMath.get_best_meld_combins_from_arr(arr)
        should_be = """[[], [50, 50, 50], [60, 60, 60], [70, 70, 70]]"""
        test = "\n".join([f'{x}' for x in combins])
        self.assertEqual(test, should_be)

        # 随机牌组
        mj_set = MjSet()
        mj_set.shuffle()
        tiles = []
        for _ in range(13):
            tiles.append(mj_set.draw())
        arr = Rule.convert_tiles_to_arr(tiles)
        melds = MjMath.get_best_meld_combins_from_arr(arr)
        test = "\n".join([f'{x}' for x in melds])
        self.assertTrue(test.index('[[]') == 0)

    def test_get_loneliest_from_arr(self):
        arr = [101, 103, 202, 205, 209, 308, 309]
        test = MjMath.get_loneliest_from_arr(arr)
        self.assertEqual(test, [209])

    def test_get_most_melds_length_from_arr(self):
        arr = [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9]  # 九宝莲灯
        length = MjMath.get_most_melds_length_from_arr(arr)
        self.assertEqual(length, 5)

        arr = [50, 50, 50, 60, 60, 60, 70, 70, 70, 80, 80]  # 小四喜
        length = MjMath.get_most_melds_length_from_arr(arr)
        self.assertEqual(length, 4)

    def test_get_melds_tree_from_arr(self):
        arr = [1, 2, 3, 4, 5, 4, 4]
        tree = Tree()
        identifier = 'root'
        tree.create_node([], identifier)
        tree = MjMath.get_melds_tree_from_sorted_arr(arr, tree, identifier)
        should_be = """
[]
├── [1, 2, 3]
│   └── [4, 4, 4]
├── [2, 3, 4]
├── [3, 4, 5]
└── [4, 4, 4]
    └── [1, 2, 3]"""
        self.assertEqual(len(tree.leaves()), 4)

    def test_factorial(self):
        x = 5
        f = MjMath.factorial(x)
        self.assertEqual(f, 120)

        x = 1
        f = MjMath.factorial(x)
        self.assertEqual(f, 1)

    def test_choose(self):
        test = MjMath.choose(from_n=1, sample_k=1)
        self.assertTrue(test, 1)

        test = MjMath.choose(from_n=10, sample_k=3)
        self.assertTrue(test, 120)

        test = MjMath.choose(from_n=10, sample_k=5)
        self.assertTrue(test, 252)

        test = MjMath.choose(from_n=20, sample_k=5)
        self.assertTrue(test, 15504)

        test = MjMath.choose(from_n=138, sample_k=14)  # largest possibility for mahjong
        self.assertTrue(test, 5268572441742348288)

    def test_chance(self):
        arr = [510, 520, 530, 540, 101, 101, 102, 103, 104, 105]
        total = []
        for _ in range(1):
            total += arr
        need = [510, 101]
        chance1 = MjMath.chance_of_combin_and_wall(arr, need, 4)
        need = [510, 102]
        chance2 = MjMath.chance_of_combin_and_wall(arr, need, 4)
        need = [510, 103, 105]
        chance3 = MjMath.chance_of_combin_and_wall(arr, need, 4)
        self.assertEqual((chance1, chance2, chance3), (0.109375, 0.0625, 0.015625))

    def test_has_orphans(self):
        arr = [1, 3, 5, 8, 8, 21, 20, 21, 510, 510, 400]
        test = MjMath.has_orphan(arr)
        self.assertTrue(test)

        arr = [1, 3, 5, 8, 8, 21, 20, 21, 510, 510]
        test = MjMath.has_orphan(arr)
        self.assertFalse(test)

        # begin = time()
        # for _ in range(100 * 1000):
        #     MjMath.has_orphan(arr)
        # duration = time() - begin
        # print("duration = ", duration)

    def test_get_orphans(self):
        arr = [1, 3, 5, 8, 101, 302, 8, 501, 502, 400]
        test = MjMath.get_orphans(arr)
        should_be = [101, 302, 400]
        self.assertEqual(test, should_be)

        arr = [101, 102, 3, 5, 12, 103, 103, 103, 501, 405, 104, 106, 107, 107, 107, 108, 108, 109]
        test = MjMath.get_orphans(arr)
        should_be = [12, 405, 501]
        self.assertEqual(test, should_be)

        # begin = time()
        # for _ in range(100 * 1000):
        #     MjMath.get_orphans(arr)
        # duration = time() - begin
        # self.assertTrue(duration < 2)

    def test_组合龙(self):
        arr = [201, 204, 207, 105, 108, 102, 303, 306, 309, 202, 203, 204, 510, 510]
        test = MjMath.is_组合龙(arr)
        should_be = True
        self.assertEqual(test, should_be)

    def test_全不靠(self):
        arr = [201, 204, 207, 105, 108, 102, 303, 306, 309, 510, 520, 530, 540, 410]
        test = MjMath.is_全不靠(arr)
        should_be = True
        self.assertEqual(test, should_be)

        arr = [201, 204, 207, 105, 108, 102, 303, 306, 309, 510, 520, 530, 540, 510]
        test = MjMath.is_全不靠(arr)
        should_be = False
        self.assertEqual(test, should_be)

        arr = [201, 204, 207, 105, 108, 102, 303, 306, 309, 510, 520, 530, 540, 301]
        test = MjMath.is_全不靠(arr)
        should_be = False
        self.assertEqual(test, should_be)

        arr = [201, 204, 207, 105, 108, 102, 303, 306, 309, 510, 520, 530, 540, 410, 410]
        test = MjMath.is_全不靠(arr)
        should_be = False
        self.assertEqual(test, should_be)

    def test_is_七星不靠(self):
        arr = [510, 520, 530, 540, 410, 420, 430, 301, 304, 307, 202, 205, 103, 109]
        test = MjMath.is_七星不靠(arr)
        should_be = True
        self.assertEqual(test, should_be)

        arr = [520, 530, 540, 410, 420, 430, 301, 304, 307, 202, 205, 103, 109, 106]
        test = MjMath.is_七星不靠(arr)
        should_be = False
        self.assertEqual(test, should_be)

        arr = [510, 520, 530, 540, 410, 420, 430, 301, 304, 307, 202, 205, 103, 106]
        test = MjMath.is_七星不靠(arr)
        should_be = True
        self.assertEqual(test, should_be)

        arr = [510, 520, 530, 540, 410, 420, 430, 301, 304, 307, 202, 205, 103, 106, 109]
        test = MjMath.is_七星不靠(arr)
        should_be = False
        self.assertEqual(test, should_be)

    def test_is_七对(self):
        arr = [510, 520, 530, 540, 410, 420, 430, 510, 520, 530, 540, 410, 420, 430, ]
        test = MjMath.is_七对(arr)
        should_be = True
        self.assertEqual(test, should_be)

        arr = [510, 520, 530, 540, 410, 420, 430, 510, 520, 530, 540, 410, 420, 410, ]
        test = MjMath.is_七对(arr)
        should_be = False
        self.assertEqual(test, should_be)

    def test_is_十三幺(self):
        arr = [101, 109, 201, 209, 301, 309, 410, 420, 430, 510, 520, 530, 540, 540 ]
        test = MjMath.is_十三幺(arr)
        should_be = True
        self.assertEqual(test, should_be)

        arr = [101, 109, 201, 209, 301, 309, 410, 420, 430, 510, 520, 530, 540, 101]
        test = MjMath.is_十三幺(arr)
        should_be = True
        self.assertEqual(test, should_be)

        arr = [101, 109, 201, 209, 301, 309, 410, 420, 430, 510, 520, 530, 540, ]
        test = MjMath.is_十三幺(arr)
        should_be = False
        self.assertEqual(test, should_be)

        arr = [101, 109, 201, 209, 301, 309, 410, 420, 430, 510, 520, 530, 540, 102 ]
        test = MjMath.is_十三幺(arr)
        should_be = False
        self.assertEqual(test, should_be)

        arr = [102, 103, 103, 106, 109, 204, 205, 207, 208, 209, 301, 302, 510, 104]
        test = MjMath.is_十三幺(arr)
        should_be = False
        self.assertEqual(test, should_be)

def main():
    unittest.main()


if __name__ == '__main__':
    main()
