#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:56
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: rule.py
# @Software: Mahjong II
# @Blog    :

from mahjong.tile import Tile
from mahjong.mj_math import MjMath
from mahjong.mj_set import MjSet


class Rule(object):

    @staticmethod
    def convert_key_to_tile(key: int):
        if not key:
            raise ValueError(f"key is 0")
        if key in MjSet.dictionary:
            return MjSet.dictionary[key]
        raise ValueError(f"can't convert {key} to tile")

    @staticmethod
    def convert_tiles_to_arr(tiles: list):
        if not tiles:
            return []
        return [tile.key for tile in tiles]

    @staticmethod
    def convert_arr_to_tiles(arr: list):
        if not arr:
            return []
        return [MjSet.dictionary[x] for x in arr]

    @staticmethod
    def convert_tiles_to_str(tiles):
        return ' '.join([f'{x}' for x in tiles])

    @staticmethod
    def split(tiles):
        tiles_set = {}
        for x in tiles:
            if x.suit not in tiles_set:
                tiles_set[x.suit] = []
            tiles_set[x.suit].append(x.value)
        return tiles_set

    @staticmethod
    def get_pair_tile_set(tiles):
        if not tiles:
            return None
        pairs = set()
        for index, x in enumerate(tiles):
            for y in range(index + 1, len(tiles)):
                other = tiles[y]
                if x.equal(other):
                    if not pairs:
                        pairs.add(x)
                    else:
                        found = False
                        for z in pairs:
                            if z.equal(x):
                                found = True
                        if not found:
                            pairs.add(x)
        return pairs

    @staticmethod
    def tiles_sub_pair(tiles, pair):
        if not tiles:
            return []

        remove = []
        for index, x in enumerate(tiles):
            if x.equal(pair):
                remove.append(index)
                if len(remove) >= 2:
                    break
        if len(remove) < 2:
            raise Exception(f'pair {pair} is not enough!')
        if len(remove) > 2:
            raise Exception(f'pair {pair} calculate error!')

        temp = tiles[:]
        for index in remove[::-1]:
            temp.pop(index)
        return temp

    @staticmethod
    def tile_key(tile: Tile):
        return tile.key

    @classmethod
    def sort(cls, tiles: list):
        tiles.sort(key=cls.tile_key)

    @classmethod
    def is_mahjong(cls, tiles):
        if not tiles:
            return False
        arr = cls.convert_tiles_to_arr(tiles)
        arr.sort()
        result = MjMath.is_mahjong(arr)
        return result

    @classmethod
    def is_flower(cls, tile):
        if tile.suit in '花季':
            return True
        return False

    @classmethod
    def is_ready(cls, tiles: list, left: list = None) -> bool:
        if not tiles:
            return False
        arr = cls.convert_tiles_to_arr(tiles)
        result = MjMath.is_ready(arr, left)
        return result[0]


def main():
    test_is_ready()


def test_is_ready():
    mj_set = MjSet()
    concealed = []
    for _ in range(4):
        concealed.append(mj_set.draw())
        concealed.append(mj_set.draw())
        concealed.append(mj_set.draw())
        mj_set.draw()
    concealed.append(mj_set.draw())
    print(Rule.convert_tiles_to_str(concealed))
    print(Rule.is_ready(concealed))


def test_convert():
    mj_set = MjSet()
    mj_set.shuffle()
    concealed = []
    for _ in range(13):
        concealed.append(mj_set.draw())
    print(Rule.convert_tiles_to_str(concealed))
    arr = Rule.convert_tiles_to_arr(concealed)
    print(arr)
    tiles = Rule.convert_arr_to_tiles(arr)
    print(Rule.convert_tiles_to_str(tiles))


if __name__ == '__main__':
    main()
