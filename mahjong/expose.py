#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:44
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: expose.py
# @Software: Mahjong II
# @Blog    :

from mahjong.tile import Tile
from mahjong.rule import Rule


class Expose(object):
    __slots__ = ("_outer", "_outer_owner", "_inners", "_all", 'expose_type')

    def __init__(self, expose_type: str, inners: list, outer=None, outer_owner=None):
        self.expose_type = expose_type
        self._inners = inners
        self._outer = outer
        self._outer_owner = outer_owner
        self._all: list = self._inners[:]
        if outer:
            self._all.append(outer)
            Rule.sort(self._all)

    def __str__(self):
        _str = ','.join([f'{x}' for x in self._inners])
        if self._outer:
            _str += f",{self._outer}"
            if self._outer_owner:
                _str += f"({self._outer_owner})"
        return _str

    @property
    def inners(self):
        return self._inners

    @property
    def outer(self):
        return self._outer

    @property
    def outer_owner(self):
        return self._outer_owner

    @property
    def all(self):
        return self._all
