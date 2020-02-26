#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/15 9:47
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: player_ai_adv.py
# @Software: Mahjong II
# @Blog    :


import sys
from random import choice
from time import time

from mahjong.mj_math import MjMath
from mahjong.mj_set import MjSet
from mahjong.player_ai_pro import PlayerAiPro
from mahjong.rule import Rule
from mahjong.tile import Tile


class PlayerAiAdv(PlayerAiPro):

    def decide_discard(self, players_count: int = 4, wall: list = []) -> Tile:
        start = time()
        if len(self._concealed) <= 5:
            tiles = self.decide_discard_by_value(wall=None, players_count=players_count, deep=2)
            duration = time() - start
            self.record_strategies_time('decide_discard_by_value_2_last', duration)
            self.record_strategies('decide_discard_by_value_2_last')
            if tiles:
                return choice(tiles)

        # discard the orphan tile
        # check for ready chance
        # discard the orphan tile
        start = time()
        test = self._concealed[:-1]
        is_ready = Rule.is_ready(test)
        if is_ready:
            tile = self.decide_discard_by_loneliest_orphan(keep_one_orphan=True)
        else:
            tile = self.decide_discard_by_loneliest_orphan(keep_one_orphan=False)
        duration = time() - start
        self.record_strategies('decide_discard_by_loneliest_orphan')
        self.record_strategies_time('decide_discard_by_loneliest_orphan', duration)
        if tile:
            return tile

        start = time()
        tiles = self.decide_discard_by_value(wall=wall, players_count=players_count, deep=1)
        duration = time() - start
        self.record_strategies_time('decide_discard_by_value_1', duration)
        self.record_strategies('decide_discard_by_value_1')
        if tiles:
            return choice(tiles)

        start = time()
        tiles = self.decide_discard_by_left_meld_and_eye()
        duration = time() - start
        self.record_strategies_time('decide_discard_by_left_meld_and_eye', duration)
        self.record_strategies('decide_discard_by_left_meld_and_eye')
        if tiles:
            return choice(tiles)

        start = time()
        arr = Rule.convert_tiles_to_arr(self.concealed)
        combins = MjMath.get_best_meld_combins_from_arr(arr)
        if combins and len(combins) > 0 and len(combins[0]) > 3:
            tiles = self.decide_discard_by_value(wall=None, players_count=players_count, deep=2)
            duration = time() - start
            self.record_strategies_time('decide_discard_by_value_2', duration)
            self.record_strategies('decide_discard_by_value_2')
            if tiles:
                return choice(tiles)

        # finally, decide by random
        start = time()
        tile = self.decide_discard_random()
        duration = time() - start
        self.record_strategies_time('decide_discard_random', duration)
        self.record_strategies('decide_discard_random')
        return tile

    def decide_discard_by_left_meld_and_eye(self):
        arr = Rule.convert_tiles_to_arr(self.concealed)
        arr.sort()
        keys = list(set(arr))
        candidates = dict()
        for key in keys:
            test = arr[:]
            test.remove(key)
            result = MjMath.count_of_melds_and_eys(test)
            count = result[0]
            if result[1]:  # has eye
                count += 1
            if count not in candidates:
                candidates[count] = []
            candidates[count].append(key)

        if not candidates:
            return None
        if len(candidates) == 1:
            return None

        len_arr = [key for key in candidates]
        max_len = max(len_arr)
        return Rule.convert_arr_to_tiles(candidates[max_len])

    def decide_discard_by_value(self, wall=None, players_count: int = 4, deep: int = 2):
        left = Rule.convert_tiles_to_arr(wall)
        arr = Rule.convert_tiles_to_arr(self.concealed)
        arr.sort()
        if deep == 1:
            # (arr)
            pass
        keys = list(set(arr))
        candidates = dict()
        self.sort_concealed()
        # ("self.concealed_str =", self.concealed_str)
        # ("self.concealed =", Rule.convert_tiles_to_arr(self.concealed))
        for key in keys:
            test = arr[:]
            test.remove(key)
            mj_value = MjMath.value_arr(test, left=left, players_count=players_count, deep=deep)
            value = MjMath.convert_mj_value_to_int(mj_value)
            # (value)
            if key not in candidates:
                candidates[key] = value
            else:
                raise LookupError(f"duplicate key: {key}")

        max_chance = 0
        # find max_chance
        for key in candidates:
            if candidates[key] == 0:
                # don't care about candidate who have no chance
                continue
            if max_chance < candidates[key]:
                max_chance = candidates[key]
        if not max_chance:
            return None

        # find candidate who have the min chance
        temp = []
        for key in candidates:
            if candidates[key] == max_chance:
                temp.append(key)
        if not temp:
            return None

        tiles = Rule.convert_arr_to_tiles(temp)
        return tiles


def main():
    test_hand()
    # test_decide_discard_by_value()
    # test_decide_discard_by_left_meld_and_eye()


def test_decide_discard_by_left_meld_and_eye():
    mj_set = MjSet()
    ai = PlayerAiAdv("bot02")
    for _ in range(3):
        ai.draw(mj_set)
    mj_set.shuffle()
    for _ in range(11):
        ai.draw(mj_set)
    ai.sort_concealed()
    print("ai.concealed_str =", ai.concealed_str)
    result = ai.decide_discard_by_left_meld_and_eye()
    for x in result:
        print(x, Rule.convert_tiles_to_str(Rule.convert_arr_to_tiles(result[x])))


def test_decide_discard_by_value():
    mj_set = MjSet()
    ai = PlayerAiAdv("bot02")
    for _ in range(3):
        ai.draw(mj_set)
    mj_set.shuffle()
    for _ in range(11):
        ai.draw(mj_set)
    ai.decide_discard_by_value(wall=mj_set)


def test_hand():
    mj_set = MjSet()
    mj_set.shuffle()
    # ai = PlayerAiPro("bot02")
    ai = PlayerAiAdv("bot02")
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
