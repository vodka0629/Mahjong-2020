#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:56
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: mj_math.py
# @Software: Mahjong II
# @Blog    :

from itertools import combinations
from random import random
from time import time

from treelib import Tree

from mahjong.mj_set import MjSet
from mahjong.mj_value import MjValue


class MjMath(object):
    test = False  # 调试状态 debug mod
    concealed_count = [1, 4, 7, 10, 13]  # 允许的手牌张数 correct tiles count for player's concealed tiles

    def __init__(self):
        pass

    @classmethod
    # 顺子 is sequence
    def is_123(cls, arr):
        if len(arr) != 3:
            return False
        if arr[0] + 1 == arr[1] and arr[0] + 2 == arr[2]:
            return True
        return False

    @classmethod
    # 刻子 is triplet
    def is_111(cls, arr):
        if len(arr) != 3:
            return False
        if arr[0] == arr[1] and arr[0] == arr[2]:
            return True
        return False

    @classmethod
    # 扛 is kong
    def is_1111(cls, arr):
        if len(arr) != 4:
            return False
        if arr[0] == arr[1] and arr[0] == arr[2] and arr[0] == arr[3]:
            return True
        return False

    @classmethod
    # 从 list1 中减掉 list2，剩下了什么？ list1 - list2 = ?
    def list_sub(cls, list1, list2):
        arr = list1[:]
        for ix, x in enumerate(list2):
            for iy, y in enumerate(arr):
                if x == y:
                    arr.pop(iy)
                    break
        return arr

    @classmethod
    # 数组中，不是刻子，就是顺子 is well-meld arr
    def is_good_meld_arr(cls, arr):
        if cls.is_111(arr) or cls.is_123(arr):
            return True

        for x in combinations(arr, 3):
            if (not cls.is_111(x)) and (not cls.is_123(x)):
                continue
            remain = cls.list_sub(arr, x)
            if cls.is_good_meld_arr(remain):
                return True
            if cls.is_111(remain) or cls.is_123(remain):
                return True

        return False

    @classmethod
    # 手牌是完整的 is well-meld arr + 1 pair of eyes
    def is_good_concealed(cls, arr):
        if not arr:
            cls.debug('not hand')
            return False

        count = len(arr)
        count -= 1
        if count not in cls.concealed_count:
            cls.debug('count error')
            return False

        pair_keys = cls.get_pair_keys(arr)
        for key in pair_keys:
            test = cls.remove_pair_from_arr(arr, key)
            if not test:
                # only have one pair
                return True
            if cls.is_good_meld_arr(test):
                return True
        return False

    @classmethod
    def debug(cls, text):
        if cls.test:
            print(text)

    @classmethod
    def get_pair_keys(cls, arr):
        keys = dict()
        for x in arr:
            if x not in keys:
                keys[x] = 0
            keys[x] += 1
        pair_keys = [x for x in keys if keys[x] > 1]
        return pair_keys

    @classmethod
    def remove_pair_from_arr(cls, arr, key):
        result = []
        count = 0

        for x in arr:
            if x == key and count < 2:
                count += 1
            else:
                result.append(x)

        if count < 2:
            raise ValueError(f"{arr} 内 {key} 的数量不足 2")

        return result

    @staticmethod
    def has_orphan(arr):
        if not arr:
            return False
        if len(arr) == 1:
            return True

        temp = arr[:]
        temp.sort()

        orphans = []
        count = len(temp)
        for index, x in enumerate(temp):
            if index == 0:
                if x < temp[index + 1] - 2:
                    return True
                continue
            if index == count - 1:
                if temp[index - 1] + 2 < x:
                    return True
                continue
            if temp[index - 1] + 2 < x < temp[index + 1] - 2:
                return True
        return False

    @staticmethod
    def get_orphans(arr):
        if not arr:
            return None
        if len(arr) == 1:
            return arr

        temp = arr[:]
        temp.sort()

        orphans = []
        count = len(temp)
        for index, x in enumerate(temp):
            if index == 0:
                if x < temp[index + 1] - 2:
                    orphans.append(x)
                continue
            if index == count - 1:
                if temp[index - 1] + 2 < x:
                    orphans.append(x)
                continue
            if temp[index - 1] + 2 < x < temp[index + 1] - 2:
                orphans.append(x)

        return orphans

    @staticmethod
    def get_not_in_pair(arr) -> set:
        not_in_pair = set()
        if not arr:
            return not_in_pair
        keys = dict()
        for x in arr:
            if x not in keys:
                keys[x] = 0
            keys[x] += 1

        for key in keys:
            if keys[key] < 2:
                not_in_pair.add(key)
        return not_in_pair

    @staticmethod
    def get_not_in_123(arr) -> set:
        not_in_123 = set()
        if not arr:
            return not_in_123
        unique = list(set(arr))
        for x in unique:
            if ((x + 1) in unique) and ((x - 1) in unique):
                continue
            if ((x + 1) in unique) and ((x + 2) in unique):
                continue
            if ((x - 1) in unique) and ((x - 2) in unique):
                continue
            not_in_123.add(x)

        return not_in_123

    @classmethod
    def is_ready(cls, arr: list, left: list = None):

        # block error parameter
        if not arr:
            raise ValueError("arr is empty")
        length = len(arr)
        if length not in cls.concealed_count:
            raise ValueError(f"concealed length error: {length}")

        if left:
            # left tiles set
            keys = left
        else:
            # total mj set
            MjSet.generate_dictionary()
            keys = [key for key in MjSet.dictionary]

        # need 1 tile
        candidates = []
        for key in keys:
            test = arr + [key]
            test.sort()
            if cls.is_good_concealed(test):
                candidates.append(key)

        if candidates:
            return tuple((True, candidates))
        return tuple((False, []))

    @classmethod
    def countdown_of_ready(cls, concealed: list, left: list = None, deep: int = 2):
        arr = concealed[:]
        arr.sort()
        # block error parameter
        if left is None:
            left = []
        if not arr:
            raise ValueError("arr is empty")
        length = len(arr)
        if length not in cls.concealed_count:
            raise ValueError(f"concealed length error: {length}")
        if deep < 1 or 4 < deep:
            raise ValueError(f"deep {deep}, should be in [1,2,3,4,5]")

        if left:
            # left tiles set
            keys = left
        else:
            # total mj set
            MjSet.generate_dictionary()
            keys = [key for key in MjSet.dictionary]

        # remove the keys that not relative to 'arr' elements
        for key in keys[::-1]:
            if key not in arr \
                    and key + 1 not in arr \
                    and key - 1 not in arr:
                keys.remove(key)

        # need how many tiles?
        candidates = []
        countdown = []

        # best combinations for arr
        combins = MjMath.get_best_meld_combins_from_arr(arr)
        for combin in combins:
            completed = []
            for meld in combin:
                completed = completed + meld
            shorter = MjMath.list_sub(arr, completed)
            shorter_len = len(shorter)
            if shorter_len >= 11:
                return (999, None)
            for drop in range(1, deep + 1):
                if drop >= shorter_len:
                    continue
                for remove in combinations(shorter, drop):
                    remains = MjMath.list_sub(shorter, list(remove))
                    for add in combinations(keys, drop + 1):
                        test = remains + list(add)
                        more = list(add)
                        more.sort()
                        if more in candidates:
                            continue
                        if MjMath.has_orphan(test):
                            continue
                        if len(set(test)) == len(test):
                            continue
                        test.sort()
                        if cls.is_good_concealed(test):
                            candidates.append(more)
                            countdown.append(drop + 1)

        if candidates:
            return tuple((min(countdown), candidates))

        # default
        return tuple((999, None))

    @classmethod
    def get_melds_tree_from_sorted_arr(cls, arr, tree=None, parent=None) -> Tree:
        removes = set()
        for remove in combinations(arr, 3):
            if remove not in removes:
                removes.add(remove)

        for remove in removes:
            meld = list(remove)
            if not cls.is_111(meld) and not cls.is_123(meld):
                continue
            shorter = MjMath.list_sub(arr, meld)
            identifier = f'{meld}' + str(random())
            tree.create_node(meld, identifier, parent=parent)
            cls.get_melds_tree_from_sorted_arr(shorter, tree, identifier)
        return tree

    @classmethod
    def get_best_meld_combins_from_arr(cls, arr: list) -> list:
        sorted_arr = arr[:]
        sorted_arr.sort()
        tree = Tree()
        identifier = 'root'
        tree.create_node([], identifier)
        MjMath.get_melds_tree_from_sorted_arr(sorted_arr, tree, identifier)
        paths = tree.paths_to_leaves()
        _combinations = []
        for path in paths:
            _combin = []
            for identifier in path:
                meld = tree.get_node(identifier).tag
                _combin.append(meld)
            _combin.sort()
            if _combin not in _combinations:
                _combinations.append(_combin)

        len_arr = [len(x) for x in _combinations]
        max_len = max(len_arr)
        best_combinations = []
        for _combin in _combinations:
            if len(_combin) == max_len:
                best_combinations.append(_combin)

        return best_combinations

    @classmethod
    def get_most_melds_length_from_arr(cls, arr: list) -> int:
        best_meld_combins = cls.get_best_meld_combins_from_arr(arr)
        if not best_meld_combins:
            return 0
        return len(best_meld_combins[0])

    @classmethod
    def get_loneliest_from_arr(cls, arr: list) -> list:
        if not arr:
            return []

        # sort
        _arr_sorted = arr[:]
        _arr_sorted.sort()
        # arr group by difference suit
        _dict = dict()
        for x in _arr_sorted:
            key = x // 100
            if key not in _dict:
                _dict[key] = []
            _dict[key].append(x)

        _candidates = dict()
        for key in _dict:
            _arr_suit = _dict[key]
            _len = len(_arr_suit)
            for index, x in enumerate(_arr_suit):
                _distance = 100
                if len(_arr_suit) == 1:
                    _distance = 100
                elif index == 0:
                    _distance = _arr_suit[index + 1] - x
                elif 0 < index < _len - 1:
                    _distance1 = _arr_suit[index + 1] - x
                    _distance2 = x - _arr_suit[index - 1]
                    _distance = min(_distance1, _distance2)
                elif index == _len - 1:
                    _distance = x - _arr_suit[index - 1]
                else:
                    raise LookupError(f"I can't believe that! {x} is so strange!")

                if x not in _candidates:
                    _candidates[x] = _distance
                else:
                    _candidates[x] = min(_candidates[x], _distance)
            # end for
        # end for

        _loneliest = dict()
        for x in _candidates:
            _distance = _candidates[x]
            if _distance not in _loneliest:
                _loneliest[_distance] = []
            _loneliest[_distance].append(x)

        _distances = [x for x in _loneliest]
        _loneliest_dist = max(_distances)
        _loneliest_arr = _loneliest[_loneliest_dist]

        return _loneliest_arr

    @classmethod
    def get_chow_combins_from_arr(cls, arr: list, outer: int) -> list:
        if not outer:
            raise ValueError(f"need an outer:{outer}")
        candidates = []
        for x in arr:
            if outer - 2 <= x <= outer + 2:
                candidates.append(x)
        if not candidates:
            return []
        combins = []
        fails = []
        for combin in combinations(candidates, 2):
            test = list(combin)
            test.sort()
            chow = test[:]
            chow.append(outer)
            chow.sort()
            if test in combins or test in fails:
                continue
            if MjMath.is_123(chow):
                combins.append(test)
            else:
                fails.append(test)
        return combins

    @classmethod
    # quickly value the mahjong arr
    def value_arr(cls, arr: list, left=None, players_count: int = 1, deep: int = 2) -> MjValue:
        if not arr:
            value = MjValue(meld=0, orphan=0, count_down=0, is_ready=False, waiting=[])
            return value

        if not left:
            # total tile types, same chance
            MjSet.generate_dictionary()
            left = [key for key in MjSet.dictionary]
        count_all = len(left)

        # basic info
        melds_count = cls.get_most_melds_length_from_arr(arr)
        orphans_arr = cls.get_orphans(arr)
        orphans_count = len(orphans_arr)
        result = MjValue(meld=melds_count, orphan=orphans_count)

        # is ready test
        ready_info = cls.is_ready(arr)
        is_ready = ready_info[0]
        if is_ready:
            combins = ready_info[1]
            if not combins:
                combins = []
            waiting = []
            fail_chance = 1
            for x in combins:
                chance = cls.chance_of_combin_and_wall(wall=left, combin=[x], players_count=players_count)
                fail_chance *= 1 - chance
                value = 1
                w = ([x], chance, value)
                waiting.append(w)
            total_chance = 1 - fail_chance
            result.is_ready = is_ready
            result.listening = waiting
            result.mahjong_chance = total_chance

        # count down test
        begin = time()
        count_down_result = cls.countdown_of_ready(arr, left=left, deep=deep)
        # ("count_down duration = %0.2f" % (time() - begin))
        # ("count_down_result =", count_down_result)
        count_down = count_down_result[0]
        result.count_down = count_down
        if count_down > max(cls.concealed_count):
            return result
        combins = count_down_result[1]
        waiting = []
        value = 1
        total_chance = 0
        if count_down <= 3 and len(combins) > 0:
            for combin in combins:
                chance = cls.chance_of_combin_and_wall(wall=left, combin=combin, players_count=players_count)
                total_chance += chance
                w = (combin, chance, value)
                waiting.append(w)
        result.waiting = waiting
        result.waiting_chance = total_chance
        return result

    @staticmethod
    def factorial(x):
        if x < 0:
            raise ValueError(f"factorial: {x} <= 0!")
        if not x:
            return 1
        f = 1
        for a in range(1, x + 1):
            f *= a
        return f

    @classmethod
    def choose(cls, from_n, sample_k):
        if not from_n:
            raise ValueError(f"need sample_k and from_n")
        if sample_k > from_n:
            raise ValueError(f"sample_k {sample_k} > from_n {from_n}")
        if sample_k == 0:
            return 1
        if sample_k == from_n:
            return 1
        # C(k,n) = n! / (k! * (n-k)!)
        result = round(cls.factorial(from_n) / (cls.factorial(sample_k) * cls.factorial(from_n - sample_k)))
        return result

    @classmethod
    def chance_of_combin_and_wall(cls, wall: list, combin: list, players_count: int):
        if not combin:
            return 0
        arr = wall[:]
        one_success_chance = 1 / players_count
        one_fail_chance = 1 - one_success_chance
        player_chance = 1
        for x in combin:
            count = arr.count(x)
            if not count:
                return 0
            arr.remove(x)
            chance = 1 - (one_fail_chance ** count)
            player_chance *= chance
        return player_chance

    @classmethod
    def convert_mj_value_to_int(cls, value: MjValue):
        total = 0

        mahjong_chance_factor = 1000
        waiting_chance_factor = 1

        if value.is_ready and value.mahjong_chance > 0:
            total += value.mahjong_chance * mahjong_chance_factor

        total += value.waiting_chance * waiting_chance_factor

        # orphan_chance_factor = 1000
        # if value.orphan > 1:
        #     total -= (value.orphan - 1) * orphan_chance_factor

        return total

    @classmethod
    def count_of_melds_and_eys(cls, arr: list) -> tuple:
        temp = arr[:]
        count = 0
        has_eye = False
        combins = cls.get_best_meld_combins_from_arr(arr)
        if combins:
            count = len(combins[0]) - 1
            for combin in combins:
                completed = []
                for meld in combin:
                    completed += meld
                remain = cls.list_sub(temp, completed)
                pairs = cls.get_pair_keys(remain)
                if pairs:
                    has_eye = True
        else:
            pairs = cls.get_pair_keys(temp)
            if pairs:
                has_eye = True
        return (count, has_eye)

    @classmethod
    def is_组合龙(cls, arr: list) -> bool:
        if len(arr) != 14:
            return False
        array = list(set(arr))
        group = dict()
        need_suit = [100, 200, 300]
        need_meld = ({1, 4, 7}, {2, 5, 8}, {3, 6, 9})
        for x in array:
            suit = x - (x % 100)
            value = x % 100
            if suit not in need_suit:
                continue
            if suit not in group:
                group[suit] = set()
            if value not in group[suit]:
                group[suit].add(value)
        if len(group) < 3:
            return False

        bingo = False
        combin = []
        for suit in group:
            if not need_meld[0].issubset(group[suit]):
                continue
            all = need_suit[:]
            all.remove(suit)
            suit_b = all[0]
            suit_c = all[1]
            if need_meld[1].issubset(group[suit_b]) and need_meld[2].issubset(group[suit_c]):
                bingo = True
                combin = [suit, suit_b, suit_c]
            elif need_meld[2].issubset(group[suit_b]) and need_meld[1].issubset(group[suit_c]):
                bingo = True
                combin = [suit, suit_c, suit_b]
            if bingo:
                break

        if not bingo:
            return False
        # ("combin:", combin)
        dragon = []
        for index, suit in enumerate(combin):
            meld = need_meld[index]
            for value in meld:
                dragon.append(suit + value)
        # ("dragon:", dragon)
        temp = arr[:]
        remain = MjMath.list_sub(temp, dragon)
        # ("remain:", remain)
        is_mahjong = MjMath.is_good_concealed(remain)
        return is_mahjong

    @classmethod
    def is_全不靠(cls, arr: list) -> bool:
        if len(arr) != 14:
            return False
        array = list(set(arr))
        group = dict()
        need_suit = [100, 200, 300]
        need_meld = ({1, 4, 7}, {2, 5, 8}, {3, 6, 9})
        for x in array:
            suit = x - (x % 100)
            value = x % 100
            if suit not in need_suit:
                continue
            if suit not in group:
                group[suit] = set()
            if value not in group[suit]:
                group[suit].add(value)
        if len(group) < 3:
            return False

        bingo = False
        combin = []
        for suit in group:
            if not need_meld[0].issubset(group[suit]):
                continue
            all = need_suit[:]
            all.remove(suit)
            suit_b = all[0]
            suit_c = all[1]
            if need_meld[1].issubset(group[suit_b]) and need_meld[2].issubset(group[suit_c]):
                bingo = True
                combin = [suit, suit_b, suit_c]
            elif need_meld[2].issubset(group[suit_b]) and need_meld[1].issubset(group[suit_c]):
                bingo = True
                combin = [suit, suit_c, suit_b]
            if bingo:
                break

        if not bingo:
            return False
        # ("combin:", combin)
        dragon = []
        for index, suit in enumerate(combin):
            meld = need_meld[index]
            for value in meld:
                dragon.append(suit + value)
        # ("dragon:", dragon)
        temp = arr[:]
        remain = MjMath.list_sub(temp, dragon)
        test_set = set(remain)
        if len(test_set) != 5:
            return False
        allow = {410, 420, 430, 510, 520, 530, 540}
        test = test_set - allow
        if test:
            return False
        return True

    @classmethod
    # 20、七星不靠：东、南、西、北、中、发、白各一张，
    # 加上一种花色的147、另一种花色的258、第三种花色的369中的七张牌组成的没有将牌的特殊和牌型。
    # 不计全不靠、五门齐、不求人、门前清。
    def is_七星不靠(cls, arr: list) -> bool:
        if len(arr) != 14:
            return False
        group = {}
        for x in arr:
            value = x % 100
            suit = x - value
            if suit not in group:
                group[suit] = []
            group[suit].append(value)
        need = {
            400: {10, 20, 30},
            500: {10, 20, 30, 40}
        }
        allowed = [
            {1, 4, 7},
            {2, 5, 8},
            {3, 6, 9},
        ]
        # confirm 中发白东南西北
        for s in need:
            if s not in group:
                return False
            if need[s] != set(group[s]):
                return False
            group.pop(s)

        # confirm no duplicated
        test = []
        for s in group:
            for x in group[s]:
                test.append(x)
        if len(test) != len(list(set(test))):
            return False

        suits = [s for s in group]
        for a in allowed:
            for s in group:
                if not group[s]:
                    return False
                if a >= set(group[s]):
                    # bingo 1
                    others = allowed[:]
                    others.remove(a)
                    suits.remove(s)
                    if others[0] >= set(group[suits[0]]) and others[1] >= set(group[suits[1]]):
                        return True
                    if others[0] >= set(group[suits[1]]) and others[0] >= set(group[suits[1]]):
                        return True
        return False

    @classmethod
    # 19、七对：七个对子组成的特殊和牌型。不计不求人、门前清、单钓将。
    def is_七对(cls, arr: list) -> bool:
        if len(arr) != 14:
            return False
        array = arr[:]
        keys = list(set(array))
        for x in keys:
            if array.count(x) != 2:
                return False
        return True

    @classmethod
    # 7、十三幺：由三种序数牌的1、9牌，七种字牌及其中一对作将牌组成的特殊和牌。不计五门齐、不求人、门前清、单钓将。
    def is_十三幺(cls, arr: list) -> bool:
        if len(arr) != 14:
            return False
        array = arr[:]
        keys = set(array)
        if len(keys) + 1 != 14:
            return False
        allowed = {101, 109, 201, 209, 301, 309, 410, 420, 430, 510, 520, 530, 540}
        if keys == allowed:
            return True
        return False

    @classmethod
    def is_mahjong(cls, arr: list) -> bool:
        if cls.is_十三幺(arr):
            print("is_十三幺")
            return True
        if cls.is_七对(arr):
            print("is_七对")
            return True
        if cls.is_七星不靠(arr):
            print("is_七星不靠")
            return True
        if cls.is_全不靠(arr):
            print("is_全不靠")
            return True
        if cls.is_组合龙(arr):
            print("is_组合龙")
            return True
        return cls.is_good_concealed(arr)


def test_value_arr():
    arr = [105, 107, 201, 203, 205, 302, 304, 304, 306, 410, 410, 520, 520]
    arr = [105, 106, 107, 108, 108, 108, 302, 304, 304, 306, 410, 410, 520]
    arr = [103, 105, 106, 108, 201, 203, 301, 303, 303, 306, 306, 307, 530, 530]
    arr = [104, 106, 107, 204, 205, 206, 301, 302, 304, 305, 306, 306, 308, 308]
    for x in arr:
        temp = arr[:]
        temp.remove(x)
        mj_value = MjMath.value_arr(temp, left=None, players_count=4, deep=1)
        value = MjMath.convert_mj_value_to_int(mj_value)
        # (x, value)
    # value = MjMath.countdown_of_ready(arr)

    pass


def test_count_of_melds_and_eys():
    arr = [105, 106, 107, 201, 205, 302, 303, 304, 306, 410, 410, 520, 520]
    arr = [101, 101, 101, 102, 103, 104, 105, 106, 107, 108, 109, 109, 109]
    count = MjMath.count_of_melds_and_eys(arr)
    # (count)


def test_is_mahjong():
    arr = [510, 510]
    # (MjMath.is_good_concealed(arr))


def main():
    # test_value_arr()
    # test_count_of_melds_and_eys()
    # test_is_mahjong()
    test_value_arr()
    pass


if __name__ == '__main__':
    main()
