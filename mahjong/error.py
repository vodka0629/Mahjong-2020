#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:44
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: error.py
# @Software: Mahjong II
# @Blog    :


class OutOfTilesError(Exception):
    def __init__(self, message='out of tiles', *args):
        self.args = args
        self.message = message


class HaveWinnerError(Exception):
    def __init__(self, winner=None, *args):
        self.args = args
        self.winner = winner
