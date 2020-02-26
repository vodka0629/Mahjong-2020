#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:56
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: player_ai.py
# @Software: Mahjong II
# @Blog    :

from random import choice
from mahjong.mj_math import MjMath
from mahjong.rule import Rule
from mahjong.player import Player
from mahjong.tile import Tile


class PlayerAi(Player):
    __slots__ = ("_strategies", "_strategies_time")

    def __init__(self, nick="Eric", coin: int = 0, is_viewer: bool = False, viewer_position: str = '东', screen=None):
        super().__init__(nick=nick, coin=coin, is_viewer=is_viewer, viewer_position=viewer_position, screen=screen)
        self._strategies = dict()
        self._strategies_time = dict()

    @property
    def strategies(self):
        return self._strategies

    @property
    def strategies_time(self):
        return self._strategies_time

    def record_strategies(self, strategy: str):
        if strategy not in self._strategies:
            self._strategies[strategy] = 1
        else:
            self._strategies[strategy] += 1

    def record_strategies_time(self, strategy: str, time: float = 0):
        if strategy not in self._strategies_time:
            self._strategies_time[strategy] = time
        else:
            self._strategies_time[strategy] += time

    def decide_discard(self) -> Tile:
        # discard the orphan tile
        tile = self.decide_discard_by_random_orphan()
        self.record_strategies('decide_discard_by_random_orphan')
        if tile:
            return tile

        # discard the tile not in pair / triplet / kong / sequence
        tile = self.decide_discard_by_not_in_meld()
        self.record_strategies('decide_discard_by_not_in_meld')
        if tile:
            return tile

        # finally, decide by random
        tile = self.decide_discard_random()
        self.record_strategies('decide_discard_random')
        return tile

    def decide_discard_by_not_in_meld(self):
        arr = Rule.convert_tiles_to_arr(self.concealed)
        not_123 = MjMath.get_not_in_123(arr)
        not_pair = MjMath.get_not_in_pair(arr)
        if (not not_123) and (not not_pair):
            return None
        loneliest = not_123 & not_pair
        key = 0
        if loneliest:
            key = choice(list(loneliest))
        if not_pair:
            key = choice(list(not_pair))
        if not_123:
            key = choice(list(not_123))
        if key:
            return Rule.convert_key_to_tile(key)
        return None


def main():
    pass


# def test_hand():
#     mj_set = MjSet()
#     ai = PlayerAi("bot01")
#     mj_set.shuffle()
#     for _ in range(13):
#         ai.draw(mj_set)
#     ai.sort_concealed()
#     print("concealed: " + Rule.convert_tiles_to_str(ai.concealed))
#
#     mj_set.shuffle()
#     for _ in range(100):
#         tile = ai.draw(mj_set)
#         print(f"draw: {tile}")
#         if Rule.is_mahjong(ai.concealed):
#             print("Mahjong!!!")
#             break
#         tile = ai.decide_discard()
#         print(f"discard: {tile}")
#         ai.discard(tile)
#         ai.sort_concealed()
#
#     print("concealed: " + Rule.convert_tiles_to_str(ai.concealed))
#     print("discarded: " + Rule.convert_tiles_to_str(ai.discarded))
#     print(f"discard by random count: {ai.discard_by_random_count}")
#     print(f"strategies: {ai.strategies}")
#     print(f"strategies_time: {ai.strategies_time}")
#     print("draw count: " + str(ai.draw_count))

if __name__ == '__main__':
    main()
