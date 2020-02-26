#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:45
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: mj_value.py
# @Software: Mahjong II
# @Blog    :

class MjValue(object):
    __slots__ = ("meld", "orphan",
                 "is_ready", "listening", "mahjong_chance",
                 "count_down", "waiting", "waiting_chance")

    def __init__(self,
                 meld: int = 0,
                 orphan: int = 0,
                 is_ready: bool = False,
                 listening=None,
                 mahjong_chance=0,
                 count_down: int = 0,
                 waiting=None,
                 waiting_chance=0
                 ):
        self.meld = meld
        self.orphan = orphan
        self.is_ready = is_ready
        self.listening = listening
        self.mahjong_chance = mahjong_chance
        self.count_down = count_down
        self.waiting = waiting
        self.waiting_chance = waiting_chance

    def __str__(self):
        waiting = "None"
        if self.waiting:
            waiting = "".join(["\n" + str(x) for x in self.waiting])
        listening = "None"
        if self.listening:
            listening = "".join(["\n" + str(x) for x in self.listening])
        text = f"""meld = {self.meld}, 
orphan = {self.orphan}, 
is_read = {self.is_ready},
listening = {listening}, 
mahjong_chance = {self.mahjong_chance}, 
count_down = {self.count_down},
waiting = {waiting}
waiting_chance = {self.waiting_chance}
"""
        return text
