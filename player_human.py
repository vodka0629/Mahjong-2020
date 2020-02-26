#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:45
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: player_human.py
# @Software: Mahjong II
# @Blog    :

import sys

import pygame

from mahjong.mj_math import MjMath
from mahjong.mj_set import MjSet
from mahjong.player import Player
from mahjong.rule import Rule
from mahjong.tile import Tile
from setting import Setting


class PlayerHuman(Player):
    __slots__ = ('cmd', 'hand', 'waiting_group', 'waiting_cmd')

    def __init__(self, nick="Eric", coin: int = 0,
                 is_viewer: bool = False, viewer_position: str = '东',
                 screen=None, clock=None):
        super().__init__(nick=nick, coin=coin,
                         is_viewer=is_viewer, viewer_position=viewer_position,
                         screen=screen, clock=clock)
        self.cmd = ''
        self.waiting_cmd = []
        self.waiting_group = pygame.sprite.Group()

    def draw(self, mj_set: MjSet):
        return super().draw(mj_set)

    def decide_discard(self) -> Tile:
        self.current_index = len(self._concealed) - 1
        choices = [[index] for index, tile in enumerate(self._concealed)]
        self.current_tiles = choices[self.current_index]
        if self.hand:
            self.hand.refresh_screen()
        allowed_cmd = ['discard']
        self.waiting_4_cmd(allowed_cmd=allowed_cmd, choices=choices, allow_sort=True)
        tile = self._concealed[self.current_index]
        self.current_tiles = []
        # self.sort_concealed()
        return tile

    def draw_waiting_cmd(self):
        self.waiting_group.empty()
        if not self.waiting_cmd:
            return
        left = Setting.concealed_bottom
        bottom = Setting.win_h - Setting.concealed_bottom
        for cmd in self.waiting_cmd:
            if cmd not in Setting.waiting_img:
                continue
            cmd_img = Setting.sprite_base + Setting.waiting_img[cmd]
            image = pygame.image.load(cmd_img)
            rect = image.get_rect()
            rect.left = left
            rect.bottom = bottom
            sprite = pygame.sprite.Sprite()
            sprite.image = image
            sprite.rect = rect
            self.waiting_group.add(sprite)
            left += rect.w + Setting.waiting_img_span

    def draw_screen(self, state: str = ''):
        super().draw_screen(state=state)
        if self.screen:
            self.draw_waiting_cmd()
            self.waiting_group.draw(self.screen)

    def try_mahjong(self, tile=None) -> bool:
        test = self.concealed[:]
        if tile:
            test.append(tile)
        if Rule.is_mahjong(test):
            choices = []
            allowed_cmd = ['hu', 'cancel']
            cmd = self.waiting_4_cmd(allowed_cmd=allowed_cmd, choices=choices)
            if cmd == 'cancel':
                return False
            elif cmd == 'hu':
                return True
            else:
                raise ValueError("exposed pong error cmd:", cmd)

        return False

    def try_exposed_pong(self, tile: Tile, owner) -> bool:
        count = 0
        arr = []
        for index, test in enumerate(self._concealed):
            if tile.key == test.key:
                count += 1
                arr.append(index)
                if count >= 2:
                    break
        if count < 2:
            # no chance for pong
            return False

        choices = [arr]
        allowed_cmd = ['pong', 'cancel']
        cmd = self.waiting_4_cmd(allowed_cmd=allowed_cmd, choices=choices)
        if cmd == 'cancel':
            return False
        elif cmd == 'pong':
            self.exposed_pong(tile, owner=owner)
            return True
        else:
            raise ValueError("exposed pong error cmd:", cmd)

    def try_conceal_kong(self, mj_set: MjSet) -> bool:
        if not self.concealed:
            return False
        if not mj_set.tiles:
            return False
        test_tiles = list(set(self.concealed))
        choices = []
        for x in test_tiles:
            choice = []
            if self.concealed.count(x) < 4:
                continue
            count = 0
            for index, y in enumerate(self.concealed):
                if x.key == y.key:
                    choice.append(index)
                    count += 1
                    if count >= 4:
                        break
            choices.append(choice)

        if not choices:
            return False

        allowed_cmd = ['kong', 'cancel']
        self.current_index = 0
        cmd = self.waiting_4_cmd(allowed_cmd=allowed_cmd, choices=choices)
        if cmd == 'cancel':
            return False
        elif cmd == 'kong':
            print("self.current_index:", self.current_index)
            print("choices:", choices)
            tile_index = choices[self.current_index][0]
            tile = self.concealed[tile_index]
            self.concealed_kong(tile=tile, mj_set=mj_set)
            return True
        else:
            raise ValueError("concealed kong error cmd:", cmd)

    def try_exposed_kong_from_exposed_pong(self, mj_set: MjSet) -> bool:
        tile = self.concealed[-1]
        if not mj_set.tiles:
            return False
        if not self.exposed:
            return False
        for expose in self.exposed:
            if expose.expose_type == 'exposed pong' and expose.outer.key == tile.key:
                print("human player's try_exposed_kong_from_exposed_pong")
                print("tile:", tile)
                print("expose:", expose)
                allowed_cmd = ['kong', 'cancel']
                self.current_index = 0
                choices = [[len(self.concealed) - 1]]
                cmd = self.waiting_4_cmd(allowed_cmd=allowed_cmd, choices=choices)
                if cmd == 'cancel':
                    return False
                elif cmd == 'kong':
                    self.exposed_kong_from_exposed_pong(tile=tile, expose=expose, mj_set=mj_set)
                    return True
        return False

    def try_exposed_kong(self, tile: Tile, owner, mj_set: MjSet) -> bool:
        count = 0
        arr = []
        for index, test in enumerate(self._concealed):
            if tile.key == test.key:
                count += 1
                arr.append(index)
                if count >= 3:
                    break
        if count < 3:
            # no chance for kong
            return False

        choices = [arr]
        allowed_cmd = ['kong', 'cancel']
        cmd = self.waiting_4_cmd(allowed_cmd=allowed_cmd, choices=choices)
        if cmd == 'cancel':
            return False
        elif cmd == 'kong':
            self.exposed_kong(tile, owner=owner, mj_set=mj_set)
            return True
        else:
            raise ValueError("exposed kong error cmd:", cmd)

    def try_exposed_chow(self, tile: Tile, owner) -> bool:
        arr = Rule.convert_tiles_to_arr(self.concealed)
        outer = tile.key

        combins = MjMath.get_chow_combins_from_arr(arr=arr, outer=outer)
        if not combins:
            return False

        # convert combins to index arrays
        choices = []
        for combin in combins:
            choice = []
            for x in combin:
                index = arr.index(x)
                choice.append(index)
            choices.append(choice)

        allowed_cmd = ['chow', 'cancel']
        cmd = self.waiting_4_cmd(allowed_cmd=allowed_cmd, choices=choices)
        if cmd == 'cancel':
            return False
        elif cmd == 'chow':
            arr = choices[self.current_index]
            inners = []
            for index in arr:
                inners.append(self._concealed[index])
            super().exposed_chow(inners=inners, tile=tile, owner=owner)
            return True
        else:
            raise ValueError("exposed chow error cmd:", cmd)

    def waiting_4_cmd(self, allowed_cmd=[], choices=[], allow_sort=False, draw_screen=True):
        if not allowed_cmd:
            raise ValueError("need at least one allowed_cmd:", allowed_cmd)
        default_cmd = allowed_cmd[0]

        if choices:
            if self.current_index < 0 or (len(choices) - 1) < self.current_index:
                self.current_index = 0
            self.current_tiles = choices[self.current_index]

        # refresh the screen
        self.waiting_cmd = allowed_cmd
        # self.waiting_cmd = ['hu', 'cancel']  # test for cmd buttons
        if draw_screen:
            self.draw_screen()
            if self.hand:
                self.hand.refresh_screen()

        cmd = ''
        step = 0
        while not cmd or cmd not in allowed_cmd:
            step += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 判断当前事件是否为点击右上角退出键
                    pygame.quit()
                    sys.exit()

            # 使用键盘提供的方法获取键盘按键 - 按键元组
            keys_pressed = pygame.key.get_pressed()

            changed = False
            if keys_pressed[pygame.K_s]:
                changed = True
                self.sort_concealed()
            if keys_pressed[pygame.K_c]:
                changed = True
                cmd = "chow"
            if keys_pressed[pygame.K_p]:
                changed = True
                cmd = "pong"
            if keys_pressed[pygame.K_k]:
                changed = True
                cmd = "kong"
            if keys_pressed[pygame.K_h]:
                changed = True
                cmd = "hu"
            if keys_pressed[pygame.K_SPACE]:
                changed = True
                cmd = "draw"
            if keys_pressed[pygame.K_ESCAPE]:
                changed = True
                cmd = "cancel"
            if keys_pressed[pygame.K_RETURN] or keys_pressed[pygame.K_KP_ENTER]:
                changed = True
                cmd = default_cmd
            if keys_pressed[pygame.K_LEFT]:
                if choices:
                    changed = True
                    self.current_index -= 1
                    if self.current_index < 0:
                        self.current_index = len(choices) - 1
                    self.current_tiles = choices[self.current_index]
            if keys_pressed[pygame.K_RIGHT]:
                if choices:
                    changed = True
                    self.current_index += 1
                    if self.current_index >= len(choices):
                        self.current_index = 0
                    self.current_tiles = choices[self.current_index]
            if cmd not in allowed_cmd:
                cmd = ''

            self.clock.tick(Setting.cmd_FPS)

            # if self.hand and changed:
            if hasattr(self, 'hand') and changed:
                self.hand.refresh_screen()

        self.waiting_cmd = []
        self.draw_screen()
        # if self.hand:
        if hasattr(self, 'hand'):
            self.hand.refresh_screen()

        return cmd
