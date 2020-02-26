#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:57
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: tile.py
# @Software: Mahjong II
# @Blog    :


class Tile(object):
    __slots__ = ('_suit', '_value', '_face', '_key', '_img')

    def __init__(self, suit: str, value: int, face: str, key: int, img: str = ''):
        self._suit = suit
        self._value = value
        self._face = face
        self._key = key
        self._img = img

    @property
    def face(self):
        return self._face

    @property
    def suit(self):
        return self._suit

    @property
    def value(self):
        return self._value

    @property
    def key(self):
        return self._key

    @property
    def img(self):
        return self._img

    def __str__(self):
        return f'[{self._face}]'

    def equal(self, other):
        if self._key == other.key:
            return True
        return False


def main():
    pass


if __name__ == '__main__':
    main()
