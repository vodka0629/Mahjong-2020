#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:57
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: mj_set.py
# @Software: Mahjong II
# @Blog    :

from mahjong.tile import Tile
from mahjong.suit import Suit
from random import shuffle


class MjSet(object):
    dictionary = None  # dictionary for tile sample

    @classmethod
    def generate_dictionary(cls):
        if cls.dictionary:
            return
        cls.dictionary = dict()
        suit_name: str
        for suit_name in Suit.Suit:
            suit = Suit.Suit[suit_name]

            if suit_name in '万饼条':
                for value in range(1, 9 + 1):
                    key: int = suit['base'] + value
                    face = str(value) + suit_name
                    if face == '1条':
                        face = '幺鸡'
                    # img for bamboo(条), man(万), pin(饼)
                    img: str = suit['eng'] + str(value) + '.png'
                    tile = Tile(suit=suit_name, value=value, face=face, key=key, img=img)
                    cls.dictionary[key] = tile  # tile sample

            if suit_name in '字风花季':
                if suit_name == '字':
                    dictionary = Suit.Dragon
                elif suit_name == '风':
                    dictionary = Suit.Wind
                elif suit_name == '花':
                    dictionary = Suit.Flower
                elif suit_name == '季':
                    dictionary = Suit.Season
                else:
                    raise LookupError(f"suit_name error: {suit_name}")
                for text in dictionary:
                    character = dictionary[text]
                    key: int = suit['base'] + character['value']
                    value: int = character['value']
                    face: str = text
                    img: str = suit['eng'] + "-" + character['eng'] + '.png'
                    tile = Tile(suit=suit_name, value=value, face=face, key=key, img=img)
                    cls.dictionary[key] = tile  # tile sample

        # end of generate_dictionary()
        return

    __slots__ = ('_tiles', '_total')

    def __init__(self, flower=False):
        MjSet.generate_dictionary()
        self._tiles = []

        for key in MjSet.dictionary:
            tile = MjSet.dictionary[key]
            if tile.suit in '万饼条风字':
                for _ in range(4):
                    self._tiles.append(tile)
            if flower and tile.suit in '花季':
                self._tiles.append(tile)

        self._total = self._tiles[:]

    def __str__(self):
        arr = [f'{x}' for x in self._tiles]
        text = ' '.join(arr)
        return text

    @property
    def tiles(self):
        return self._tiles

    @property
    def total(self):
        return self._total

    def shuffle(self):
        shuffle(self._tiles)

    def draw(self) -> Tile:
        if not self._tiles:
            return None
        tile = self._tiles.pop()
        return tile

    def draw_from_back(self) -> Tile:
        if not self._tiles:
            return None
        tile = self._tiles.pop(0)
        return tile


def main():
    mj_set = MjSet(flower=True)
    # mj_set.shuffle()
    print(f'{mj_set}')
    print(len(mj_set.tiles))


if __name__ == '__main__':
    main()
