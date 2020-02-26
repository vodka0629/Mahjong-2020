#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/14 10:07
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: player_ai_pro.py
# @Software: Mahjong II
# @Blog    :


from random import choice
from time import time

from mahjong.mj_math import MjMath
from mahjong.mj_set import MjSet
from mahjong.player_ai import PlayerAi
from mahjong.rule import Rule
from mahjong.tile import Tile


class PlayerAiPro(PlayerAi):
    def decide_discard(self) -> Tile:
        # discard the orphan tile
        start = time()
        tile = self.decide_discard_by_loneliest_orphan()
        duration = time() - start
        self.record_strategies_time('decide_discard_by_loneliest_orphan', duration)
        if tile:
            self.record_strategies('decide_discard_by_loneliest_orphan')
            return tile

        # check for ready chance
        test = self._concealed[:-1]
        is_ready = Rule.is_ready(test)

        if not is_ready:
            start = time()
            tile = self.decide_discard_by_remove_melds()
            duration = time() - start
            self.record_strategies_time('decide_discard_by_remove_melds', duration)
            if tile:
                self.record_strategies('decide_discard_by_remove_melds')
                return tile

        if is_ready:
            start = time()
            tile = self.decide_discard_by_is_ready()
            duration = time() - start
            self.record_strategies_time('decide_discard_by_is_ready', duration)
            if tile:
                self.record_strategies('decide_discard_by_is_ready')
                return tile

        # finally, decide by random
        start = time()
        tile = self.decide_discard_random()
        duration = time() - start
        self.record_strategies_time('decide_discard_random', duration)
        self.record_strategies('decide_discard_random')
        return tile

    def decide_discard_by_loneliest_orphan(self, keep_one_orphan: bool = False):
        arr = Rule.convert_tiles_to_arr(self.concealed)
        orphans_arr = MjMath.get_orphans(arr)
        if keep_one_orphan:
            if len(orphans_arr) <= 1:
                return None
        else:
            if len(orphans_arr) <= 0:
                return None
        loneliest_arr = MjMath.get_loneliest_from_arr(orphans_arr)
        if not loneliest_arr:
            return None
        one = choice(loneliest_arr)
        tile = Rule.convert_key_to_tile(one)
        return tile

    def decide_discard_by_is_ready(self):
        arr = Rule.convert_tiles_to_arr(self.concealed)
        arr_sorted = arr[:]
        arr_sorted.sort()
        candidates = dict()
        for x in arr_sorted:
            test = arr_sorted[:]
            test.remove(x)
            result = MjMath.is_ready(test)
            if result[0]:  # is_ready!
                if x not in candidates:
                    candidates[x] = set()
                    candidates[x] = set(result[1])
                else:
                    continue

        if not candidates:
            return None

        arr_len = [len(candidates[x]) for x in candidates]
        max_len = max(arr_len)

        best_choices = []
        for x in candidates:
            if len(candidates[x]) == max_len:
                best_choices.append(x)

        one = choice(best_choices)
        tile = Rule.convert_key_to_tile(one)
        return tile

    def decide_discard_by_remove_melds(self):
        arr = Rule.convert_tiles_to_arr(self.concealed)
        combins = MjMath.get_best_meld_combins_from_arr(arr)
        if not combins:
            return None
        remain_combins = []
        for combin in combins:
            arr_completed = []
            for meld in combin:
                arr_completed += meld
            arr_remain = MjMath.list_sub(arr, arr_completed)
            arr_remain.sort()
            remain_combins.append(arr_remain)

        loneliest_arrs = []
        for combin in remain_combins:
            loneliest_arr = MjMath.get_loneliest_from_arr(combin)
            loneliest_arrs.append(loneliest_arr)

        # select orphans from loneliest_arrs
        orphans = []
        for arr in loneliest_arrs:
            orphans += arr
        test = list(set(orphans))
        test.sort()
        orphans = MjMath.get_orphans(test)
        if orphans:
            one = choice(orphans)
            tile = Rule.convert_key_to_tile(one)
            return tile

        # select one from loneliest_arrs by distance
        loneliest_candidates = MjMath.get_loneliest_from_arr(test)
        if not loneliest_candidates:
            raise LookupError(f"loneliest_candidates of {test} is empty! I can't believe that!")
        one = choice(loneliest_candidates)
        tile = Rule.convert_key_to_tile(one)
        return tile


def main():
    test_hand()
    # test_decide_discard_by_remove_melds()


def test_decide_discard_by_remove_melds():
    mj_set = MjSet()
    ai = PlayerAiPro("bot01")
    for _ in range(3):
        ai.draw(mj_set)
    mj_set.shuffle()
    for _ in range(11):
        ai.draw(mj_set)
    ai.decide_discard_by_remove_melds()


def test_hand():
    mj_set = MjSet()
    mj_set.shuffle()
    # ai = PlayerAiPro("bot02")
    ai = PlayerAiPro("bot02")
    for _ in range(13):
        ai.draw(mj_set)
    ai.sort_concealed()
    print("concealed: " + Rule.convert_tiles_to_str(ai.concealed))

    mj_set.shuffle()
    for _ in range(100):
        tile = ai.draw(mj_set)
        print(f"draw: {tile}")
        if Rule.is_mahjong(ai.concealed):
            print("Mahjong!!!")
            break
        tile = ai.decide_discard()
        print(f"discard: {tile}")
        ai.discard(tile)
        ai.sort_concealed()

    print("concealed: " + Rule.convert_tiles_to_str(ai.concealed))
    print("discarded: " + Rule.convert_tiles_to_str(ai.discarded))
    print(f"strategies: {ai.strategies}")
    print(f"strategies_time: {ai.strategies_time}")
    print("draw count: " + str(ai.draw_count))


if __name__ == '__main__':
    main()
