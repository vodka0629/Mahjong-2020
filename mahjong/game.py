#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:44
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: game.py
# @Software: Mahjong II
# @Blog    :
import json
import time
from random import shuffle

import pygame

from color import Color
from hand_s import HandS
from mahjong.player_ai import PlayerAi
from mahjong.suit import Suit
from player_human import PlayerHuman
from setting import Setting
from sprite import Sprite


class Game(object):
    __slots__ = ('flowers', 'circles', 'start_coin', 'stop_at_broken', 'opposites', 'player', 'players',
                 'screen', 'clock')

    def __init__(self, screen, clock):
        self.flowers = Setting.game_flowers
        self.circles = Setting.game_circles
        self.start_coin = Setting.game_start_coin
        self.stop_at_broken = Setting.game_stop_at_broken
        girls = Setting.game_opposites[:]
        shuffle(girls)
        self.opposites = girls[0:3]
        self.player = PlayerHuman(Setting.game_player_name, coin=self.start_coin, is_viewer=True, clock=clock)
        self.players = list()
        self.screen = screen
        self.clock = clock

    def prepare(self):
        self.players.append(self.player)
        for name in self.opposites:
            ai = PlayerAi(name, coin=self.start_coin)
            self.players.append(ai)

    def play(self):
        shuffle(self.players)
        for _ in range(self.circles):
            index = _ % 4
            prevailing_wind = Suit.get_wind_by_index(index)
            self.circle(prevailing_wind=prevailing_wind)

    def circle(self, prevailing_wind):
        # a circle contains 4 hands
        for index in range(4):
            hand = HandS(players=self.players, viewer=self.player,
                         number=index + 1,
                         flower=self.flowers, prevailing_wind=prevailing_wind,
                         screen=self.screen, clock=self.clock,
                         )
            hand.prepare()
            hand.deal()

            #########################
            # for test propose only! 平和
            #########################
            # tester = self.players[0]
            # tester._concealed = []
            # arr = [101, 102, 103, 104, 105, 106,
            #        107, 108, 109, 202, 203, 204,
            #        303]
            # tiles = Rule.convert_arr_to_tiles(arr)
            # tester._concealed = tiles
            # first = Rule.convert_key_to_tile(303)
            # hand.mj_set.tiles.append(first)
            # hand.refresh_screen()

            #########################
            # for test propose only! 流局
            #########################
            # length = len(hand.mj_set.tiles)
            # for _ in range(length - 2):
            #     hand.mj_set.draw()
            # hand.refresh_screen()

            #########################
            # for test propose only! robbing_a_kong
            #########################
            # tester = self.players[0]
            # player1 = self.players[1]
            # player3 = self.players[3]
            # tester._concealed = []
            # arr = [101, 103, 105, 204, 206, 208,
            #        301, 305, 308, 520]
            # tiles = Rule.convert_arr_to_tiles(arr)
            # tester._concealed = tiles
            # arr = [201, 201]
            # inners = Rule.convert_arr_to_tiles(arr)
            # outer = Rule.convert_key_to_tile(201)
            # expose = Expose(inners = inners, outer = outer, outer_owner=player1, expose_type='exposed pong')
            # tester._exposed = [expose]
            # first = Rule.convert_key_to_tile(201)
            # hand.mj_set.tiles.append(first)
            #
            # arr = [202, 203,
            #        205, 206, 207,
            #        205, 206, 207,
            #        209, 209, 209,
            #        420, 420]
            # tiles = Rule.convert_arr_to_tiles(arr)
            # player3._concealed = tiles
            # arr = [610, 620, 630, 640, 610, 620, 630, 640, 610, 620, 630, 640, 610, 620, 630, 640, ]
            # flowers = Rule.convert_arr_to_tiles(arr)
            # player3.flowers = flowers
            # hand.refresh_screen()

            #########################
            # for test propose only! mahjong on exposed kong
            #########################
            # tester = self.players[0]
            # player1 = self.players[1]
            # player3 = self.players[3]
            # tester._concealed = []
            # arr = [101, 102, 102, 204, 204, 205,
            #        301, 301, 302, 302]
            # tiles = Rule.convert_arr_to_tiles(arr)
            # tester._concealed = tiles
            # arr = [201, 201]
            # inners = Rule.convert_arr_to_tiles(arr)
            # outer = Rule.convert_key_to_tile(201)
            # expose = Expose(inners=inners, outer=outer, outer_owner=player1, expose_type='exposed pong')
            # tester._exposed = [expose]
            # first = Rule.convert_key_to_tile(510)
            # hand.mj_set.tiles.append(first)
            #
            # arr = [202, 202,
            #        205, 206, 207,
            #        205, 206, 207,
            #        510, 510, 510,
            #        420, 420]
            # tiles = Rule.convert_arr_to_tiles(arr)
            # player3._concealed = tiles
            # arr = []
            # flowers = Rule.convert_arr_to_tiles(arr)
            # player3.flowers = flowers
            # last = Rule.convert_key_to_tile(420)
            # hand.mj_set.tiles.insert(0, last)
            # hand.refresh_screen()

            #########################
            # for test propose only! mahjong on concealed kong
            #########################
            # tester = self.players[0]
            # player1 = self.players[1]
            # player3 = self.players[3]
            # tester._concealed = []
            # arr = [101, 101, 101,
            #        204, 205,
            #        301, 301, 301,
            #        302, 302, 302,
            #        410, 410
            #        ]
            # tiles = Rule.convert_arr_to_tiles(arr)
            # tester._concealed = tiles
            # first = Rule.convert_key_to_tile(101)
            # hand.mj_set.tiles.append(first)
            # last = Rule.convert_key_to_tile(203)
            # hand.mj_set.tiles.insert(0, last)
            # hand.refresh_screen()

            #########################
            # for test propose only! mahjong on 'exposed kong on exposed gang'
            #########################
            # tester = self.players[0]
            # player1 = self.players[1]
            # tester._concealed = []
            # arr = [204, 205,
            #        301, 301, 301,
            #        302, 302, 302,
            #        410, 410
            #        ]
            # tiles = Rule.convert_arr_to_tiles(arr)
            # tester._concealed = tiles
            # arr = [101, 101]
            # inners = Rule.convert_arr_to_tiles(arr)
            # outer = Rule.convert_key_to_tile(101)
            # expose = Expose(inners=inners, outer=outer, outer_owner=player1, expose_type='exposed pong')
            # tester._exposed = [expose]
            # first = Rule.convert_key_to_tile(101)
            # hand.mj_set.tiles.append(first)
            # last = Rule.convert_key_to_tile(203)
            # hand.mj_set.tiles.insert(0, last)
            # hand.refresh_screen()

            hand.play()
            hand.score()
            pygame.display.update()  # 刷新屏幕

            print("left tiles:", len(hand.mj_set.tiles))
            print("player count:", len(self.players))
            print("winner:", hand.winner)

    def end(self):
        end_group = pygame.sprite.Group()
        img = pygame.image.load(Setting.sprite_base + Setting.end_left)
        left = Sprite(img)
        left.rect.top = 0
        left.rect.left = 0

        img = pygame.image.load(Setting.sprite_base + Setting.end_right)
        right = Sprite(img)
        right.rect.top = 0
        right.rect.right = Setting.win_w

        img = pygame.image.load(Setting.sprite_base + Setting.girl_img['start'])
        girl = Sprite(img)
        girl.rect.centery = Setting.win_h // 2
        girl.rect.left = 0

        font = pygame.font.Font(Setting.font, Setting.small_font_size)
        the_end = 'Game Over'
        img = font.render(the_end, True, Color.BLACK)
        sprite = Sprite(img)
        sprite.rect.top = Setting.end_top
        sprite.rect.centerx = Setting.win_w // 2

        font = pygame.font.Font(Setting.font, Setting.huge_font_size)
        the_end = '完'
        img = font.render(the_end, True, Color.BLACK)
        sprite2 = Sprite(img)
        sprite2.rect.top = Setting.end_top + sprite.rect.h
        sprite2.rect.centerx = Setting.win_w // 2

        end_group.add(left)
        end_group.add(right)
        end_group.add(girl)
        end_group.add(sprite)
        end_group.add(sprite2)

        # player 成绩的持久化
        filename = Setting.history
        history = None
        try:
            with open(filename, "r", encoding="utf-8") as file:
                history = json.load(file)
        except UnicodeDecodeError as e:
            print("Unicode Decode Error Found:", e)
        except FileNotFoundError as e:
            print("File Not Found: ", e)

        for x in history:
            x['current'] = False
        record = {
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'coin': self.player.coin,
            'current': True,
        }
        if not history:
            history = []
        history.append(record)
        def coin(record):
            return record['coin']
        history.sort(key=coin, reverse=True)
        if len(history) > 10:
            history = history[0:10]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)

        font = pygame.font.Font(Setting.font, Setting.normal_font_size)
        left = Setting.history_left
        right = Setting.history_right
        top = Setting.history_top
        for record in history:
            str_time = record['time']
            coin = record['coin']
            color = Color.BLACK
            if record['current']:
                color = Color.RED
            img = font.render(str_time, True, color)
            sprite = Sprite(img)
            sprite.rect.left = Setting.win_w // 2 - left
            sprite.rect.top = top
            end_group.add(sprite)
            img = font.render(str(coin), True, color)
            sprite = Sprite(img)
            sprite.rect.right = Setting.win_w // 2 + right
            sprite.rect.top = top
            end_group.add(sprite)
            top += Setting.history_y_span

        self.screen.fill(Color.WHITE)  # 填充白色
        end_group.draw(self.screen)
        pygame.display.update()

        if self.player:
            allowed_cmd = ['discard']
            self.player.waiting_4_cmd(allowed_cmd=allowed_cmd, draw_screen=False)

        print("Game End...")
        exit(0)


def main():
    game = Game(screen=None, clock=None)
    game.play()


if __name__ == '__main__':
    main()
