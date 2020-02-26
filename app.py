#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:46
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: app.py
# @Software: Mahjong II
# @Blog    :

import pygame

from color import *
from mahjong.game import Game
from setting import Setting

pygame.init()  # pygame 初始化，必须有，且必须在开头

clock = pygame.time.Clock()  # 用于控制循环刷新频率的对象
screen = pygame.display.set_mode((Setting.win_w, Setting.win_h))
screen.fill(Color.WHITE)
pygame.display.set_caption(Setting.game_name)
pygame.font.init()
pygame.mixer.init()



game = Game(screen=screen, clock=clock)
game.prepare()
game.play()
game.end()

# eric = PlayerHuman('Eric', is_viewer=True)
# players = [
#     eric,
#     PlayerAi('大乔'),
#     PlayerAi('貂蝉'),
#     PlayerAi('西施'),
# ]
# prevailing_wind = '东'
# hand = HandS(players=players, flower=True, prevailing_wind=prevailing_wind, screen=screen, clock=clock, viewer=eric)
# hand.prepare()
# hand.deal()

# for test propose only!
# tester = eric
# test_set = MjSet()
# test for winds
# tester._concealed = []

# 九宝莲灯
# arr = [101, 101, 101, 102, 103, 104, 105, 106, 107, 108, 109, 109, 109]

# 平胡
# arr = [101, 102, 103, 104, 105, 106,
#        107, 108, 109, 202, 203, 204,
#        303]
# tiles = Rule.convert_arr_to_tiles(arr)
# tester._concealed = tiles
# first = Rule.convert_key_to_tile(303)
# hand.mj_set.tiles.append(first)

# for _ in range(4):
#     for x in range(3):
#         tester.draw(test_set)
#     test_set.draw()
# tester.draw(test_set)

# test for kong
# arr = [510, 520, 530, 540]
# for x in arr:
#     arr = [x, x]
#     inners = Rule.convert_arr_to_tiles(arr)
#     outer = Rule.convert_key_to_tile(x)
#     expose = Expose(expose_type='exposed pong', inners=inners, outer=outer, outer_owner=nana)
#     eric.exposed.append(expose)
# eric._concealed = []
# eric.draw(hand.mj_set)
