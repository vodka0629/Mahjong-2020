#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:46
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: hand_s.py
# @Software: Mahjong II
# @Blog    :
from random import choice

import pygame

from color import *
from mahjong.calc import Calc
from mahjong.error import OutOfTilesError, HaveWinnerError
from mahjong.hand import Hand
from mahjong.mj_math import MjMath
from mahjong.player_ai_adv import PlayerAiAdv
from mahjong.rule import Rule
from mahjong.suit import Suit
from setting import Setting
from sprite import Sprite


class HandS(Hand):
    __slots__ = ("_screen", "_clock", "_font",
                 "_player",
                 "_info_group", "_hand_name",
                 "_background_img_group", "_background_music",

                 "_sound_discard", "_sound_draw_stack",
                 "_sound_kong", "_sound_chow", "_sound_pong",
                 "_sound_hu", "_sound_self_hu",)

    def __init__(self, players: list = None,
                 prevailing_wind: str = '东', number: int = 1,
                 flower=False,
                 screen=None, clock=None, viewer=None):
        if not screen:
            raise ValueError("need a screen!")
        if not clock:
            raise ValueError("need a clock!")
        if not viewer:
            raise ValueError("must set a viewer!")
        self._screen = screen
        self._clock = clock
        self._player = viewer
        self._font = pygame.font.Font(Setting.font, 20)
        self._background_img_group = pygame.sprite.Group()
        self._info_group = pygame.sprite.Group()
        self._hand_name = pygame.sprite.Group()

        hand_name = prevailing_wind + " " + str(number) + ' 局'
        print("hand_name:", hand_name)
        font = pygame.font.Font(Setting.font, Setting.small_font_size)
        image = font.render(hand_name, True, Color.WHITE)
        sprite = pygame.sprite.Sprite()
        sprite.image = image
        sprite.rect = image.get_rect()
        sprite.rect.top = Setting.hand_name_top
        sprite.rect.left = Setting.hand_name_left
        self._hand_name.add(sprite)
        self._hand_name.draw(self.screen)

        self._background_music = Setting.background_music
        if self._background_music:
            music = choice(self._background_music)
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)

        background_img = pygame.image.load(Setting.background_img)
        background_img = pygame.transform.scale(background_img, (Setting.win_w, Setting.win_h))
        rect = background_img.get_rect()
        sprite = pygame.sprite.Sprite()
        sprite.image = background_img
        sprite.rect = rect
        self._background_img_group.add(sprite)
        self.draw_background()

        self._sound_discard = pygame.mixer.Sound(Setting.sound_base + Setting.sound_discard)
        self._sound_draw_stack = pygame.mixer.Sound(Setting.sound_base + Setting.sound_draw_stack)

        self._sound_chow = pygame.mixer.Sound(Setting.sound_base + Setting.sound_chow)
        self._sound_pong = pygame.mixer.Sound(Setting.sound_base + Setting.sound_pong)
        self._sound_kong = pygame.mixer.Sound(Setting.sound_base + Setting.sound_kong)

        self._sound_hu = pygame.mixer.Sound(Setting.sound_base + Setting.sound_hu)
        self._sound_self_hu = pygame.mixer.Sound(Setting.sound_base + Setting.sound_self_hu)

        if players:
            viewer = None
            for index, player in enumerate(players):
                player.position = Suit.get_wind_by_index(index)
                player.screen = self.screen
                player.clock = self._clock
                if player.is_viewer:
                    viewer = player
                    player.hand = self
            for player in players:
                player.viewer_position = viewer.position
            # draw the position
            if viewer:
                font = pygame.font.Font(Setting.font, Setting.normal_font_size)
                small = pygame.font.Font(Setting.font, Setting.small_font_size)
                for index, player in enumerate(players):
                    suit = Suit.get_wind_by_index(index)
                    # image = font.render(suit + ":" + player.nick, True, Color.YELLOW)
                    image = font.render(suit, True, Color.YELLOW)
                    coin = None
                    if suit == Suit.get_next_wind(viewer.position):
                        angel = 90
                        image = pygame.transform.rotate(image, angel)
                        sprite = Sprite(image)
                        sprite.rect.centery = Setting.win_h // 2
                        sprite.rect.left = Setting.win_w // 2 + Setting.player_name_span
                        avatar = Sprite(player.avatar)
                        avatar.rect.top = 50
                        avatar.rect.right = Setting.win_w - Setting.concealed_bottom
                        coin_img = font.render(str(player.coin), True, Color.WHITE)
                        coin = Sprite(coin_img)
                        coin.rect.top = 50 + avatar.rect.h
                        coin.rect.centerx = Setting.win_w - Setting.concealed_bottom - avatar.rect.w // 2
                    elif suit == Suit.get_before_wind(viewer.position):
                        angel = 270
                        image = pygame.transform.rotate(image, angel)
                        sprite = Sprite(image)
                        sprite.rect.centery = Setting.win_h // 2
                        sprite.rect.right = Setting.win_w // 2 - Setting.player_name_span
                        avatar = Sprite(player.avatar)
                        avatar.rect.bottom = Setting.win_h - 50
                        avatar.rect.left = Setting.concealed_bottom
                        coin_img = font.render(str(player.coin), True, Color.WHITE)
                        coin = Sprite(coin_img)
                        coin.rect.bottom = Setting.win_h - 50 - avatar.rect.h
                        coin.rect.centerx = Setting.concealed_bottom + avatar.rect.w // 2
                    elif suit == Suit.get_opposition_wind(viewer.position):
                        angel = 180
                        image = pygame.transform.rotate(image, angel)
                        sprite = Sprite(image)
                        sprite.rect.bottom = Setting.win_h // 2 - Setting.player_name_span
                        sprite.rect.centerx = Setting.win_w // 2
                        avatar = Sprite(player.avatar)
                        avatar.rect.top = Setting.concealed_bottom
                        avatar.rect.right = Setting.win_w - 295
                        coin_img = font.render(str(player.coin), True, Color.WHITE)
                        coin = Sprite(coin_img)
                        coin.rect.bottom = Setting.concealed_bottom
                        coin.rect.centerx = Setting.win_w - 295 - avatar.rect.w // 2
                    else:
                        angel = 0
                        sprite = Sprite(image)
                        sprite.rect.top = Setting.win_h // 2 + Setting.player_name_span
                        sprite.rect.centerx = Setting.win_w // 2
                        avatar = Sprite(player.avatar)
                        avatar.rect.bottom = Setting.win_h - Setting.concealed_bottom
                        avatar.rect.left = 295
                        coin_img = font.render(str(player.coin), True, Color.WHITE)
                        coin = Sprite(coin_img)
                        coin.rect.top = Setting.win_h - Setting.concealed_bottom
                        coin.rect.centerx = 295 + avatar.rect.w // 2

                    self._hand_name.add(sprite)
                    self._hand_name.add(avatar)
                    if coin:
                        self._hand_name.add(coin)

        super().__init__(players=players, prevailing_wind=prevailing_wind, flower=flower)

    @property
    def screen(self):
        return self._screen

    def deal(self):
        for _ in range(max(MjMath.concealed_count) // 4):
            for player in self._players:
                player.draw_stack(self._mj_set)
                self.refresh_screen()
                self._sound_draw_stack.play()

        self.draw_start_screen()

        for player in self.players:
            player.draw(self._mj_set)
            player.sort_concealed()
            self.refresh_screen()

        self._state_machine.deal()

    def draw_background(self):
        self._background_img_group.draw(self.screen)
        self._hand_name.draw(self.screen)

    def refresh_screen(self, state: str = ''):

        # self._screen.fill(Color.WHITE)  # 填充白色
        self.draw_background()

        # 显示方位
        for player in self._players:
            if player != self._player:
                player.draw_screen(state=state)
        if self._player:
            self._player.draw_screen(state=state)

        text = self._font.render(u'%d' % len(self.mj_set.tiles), 1, Setting.info_color)
        sprite = pygame.sprite.Sprite()
        # sprite.img = text
        rect = text.get_rect()
        rect.centerx = Setting.win_w // 2
        rect.centery = Setting.win_h // 2
        sprite.image = text
        sprite.rect = rect
        info_group = pygame.sprite.Group()
        info_group.add(sprite)
        info_group.draw(self.screen)

        self._clock.tick(Setting.FPS)  # 别太快
        pygame.display.update()  # 显示

    def sound_discard(self):
        self._sound_discard.play()

    def play(self):
        current = self._dealer  # the current player
        player = current
        before = None  # the previous player
        current_discard = None  # discard tile by previous player

        for player in self._players:
            print(f'{player.position}: {player}')
        print("=" * 40)

        have_winner = False
        while not have_winner and not self.out_of_tiles:

            if current_discard:
                wind = current.position
                player = current
                for index in range(3):
                    # test for hu by other
                    if player.try_mahjong(current_discard):
                        player.concealed.append(current_discard)
                        print(f"winner is {player}, by {before}")
                        self._winner = player
                        self.firer = before
                        self._state_machine.mahjong()
                        have_winner = True
                        self.refresh_screen(state='mahjong')
                        break
                    wind = Suit.get_next_wind(wind)
                    player = self.positions[wind]

            if have_winner:
                break

            # interrupted by exposed kong / pong / chow
            interrupted = False
            if current_discard:

                # Melding another for current, +1, +2 players
                player = None

                # try kong ( must have tiles ):
                if self.mj_set.tiles:
                    wind = current.position
                    player = current
                    for index in range(3):
                        try:
                            if player.try_exposed_kong(tile=current_discard, owner=before, mj_set=self._mj_set):
                                self.refresh_screen('drawing')
                                # self._sound_kong.play()
                                interrupted = True
                                break
                        except OutOfTilesError as e:
                            self.withdraw()
                        except HaveWinnerError as e:
                            self._winner = player
                            self.mahjong_on_kong = True
                            self.firer = player
                            self._state_machine.mahjong()
                            have_winner = True
                            self.refresh_screen(state='mahjong')
                            break
                        wind = Suit.get_next_wind(wind)
                        player = self.positions[wind]
                    if self._winner:
                        break

                # try pong:
                if not interrupted:
                    wind = current.position
                    player = current
                    for index in range(3):
                        if player.try_exposed_pong(tile=current_discard, owner=before):
                            self.refresh_screen()
                            self._sound_pong.play()
                            interrupted = True
                            break
                        wind = Suit.get_next_wind(wind)
                        player = self.positions[wind]

                # try chow:
                if not interrupted:
                    # wind = current.position
                    player = current
                    if player.try_exposed_chow(current_discard, before):
                        self.refresh_screen()
                        self._sound_chow.play()
                        interrupted = True

                if not interrupted:
                    before.put_on_desk(current_discard)
                before.discarding = None
            # end if current_discard:

            if interrupted:
                current = player
            else:
                # test for out of tiles
                if not self.mj_set.tiles:
                    self.withdraw()
                    break

                # draw
                new_tile = current.draw(self._mj_set)
                if not new_tile:
                    self.withdraw()
                    break
                self.refresh_screen(state='drawing')

                # test for hu by self
                if current.try_mahjong(tile=None):
                    print(f"winner is {current}, by self!")
                    self._winner = current
                    self.firer = current
                    self._state_machine.mahjong()
                    self.refresh_screen(state='mahjong')
                    break

                # self kong
                try:
                    if current.try_conceal_kong(self.mj_set):
                        pass
                except OutOfTilesError as e:
                    self.withdraw()
                except HaveWinnerError as e:
                    self._winner = current
                    self.mahjong_on_kong = True
                    self.firer = current
                    self._state_machine.mahjong()
                    have_winner = True
                    self.refresh_screen(state='mahjong')
                    break
                if self.winner:
                    break

                # test for exposed kong from exposed pong
                result_of_try = False
                try:
                    result_of_try = current.try_exposed_kong_from_exposed_pong(mj_set=self.mj_set)
                except OutOfTilesError as e:
                    self.withdraw()
                except HaveWinnerError as e:
                    self._winner = current
                    self.mahjong_on_kong = True
                    self.firer = current
                    self._state_machine.mahjong()
                    have_winner = True
                    self.refresh_screen(state='mahjong')
                    break

                if self._winner:
                    break

                if result_of_try:
                    # try rob kong by others
                    self.refresh_screen()

                    # others try mahjong
                    player = None
                    wind = current.position
                    for index in range(3):
                        wind = Suit.get_next_wind(wind)
                        player = self.positions[wind]
                        if player.try_mahjong(tile=new_tile):
                            print(f"winner is {player}, by rob {current}!")
                            player.concealed.append(new_tile)
                            self._winner = player
                            self.firer = current
                            self._state_machine.mahjong()
                            self.refresh_screen(state='mahjong')
                            self.robbing_a_kong = True
                            break
                    if self._winner:
                        break

            if isinstance(current, PlayerAiAdv):
                wall = self._mj_set.tiles
                tile = current.decide_discard(players_count=len(self.players), wall=wall)
            else:
                tile = current.decide_discard()
            current.discard(tile)
            print(current, 'discard tile:', tile)
            current_discard = tile
            current.sort_concealed()

            # (f'{current} discard {tile}')
            # (Rule.convert_tiles_to_str(current.concealed))

            # next player
            next = self._get_next_player(current)
            before = current
            current = next

            self.refresh_screen()
            self.sound_discard()
        # end while

        self.refresh_screen(state='scoring')
        print("tiles left :", len(self.mj_set.tiles))
        for player in self.players:
            if player == self.winner:
                print(f"winner {player}: ", Rule.convert_tiles_to_str(player.concealed))
            else:
                print(f"{player}: ", Rule.convert_tiles_to_str(player.concealed))

        left = Rule.convert_tiles_to_arr(self.mj_set.tiles)
        left.sort()

    # end def play()

    def withdraw(self):
        print("out of tiles!")
        self._winner = None
        self.out_of_tiles = True
        self._state_machine.withdraw()

    def score(self):
        super().score()
        self.refresh_screen(state="scoring")
        result = ''
        if not self._winner:
            result = 'draw'
        elif self._winner == self._player:
            result = 'win'
        else:
            result = 'lose'

        sound = ''
        if self._winner:
            if self._winner == self._player:
                sound = 'player_win'
            elif self.firer == self._player:
                sound = 'player_fire'
            elif self.firer == self._winner:
                sound = 'girl_self_hu'
            else:
                sound = 'girl_hu'
        else:
            sound = 'withdraw'
        s = pygame.mixer.Sound(Setting.sound_base + Setting.girl_sound[sound])
        s.play()

        player_position = self._player.position
        text = ''
        if self._winner:
            if self._winner.position == player_position:
                text = 'self_win'
            elif self._winner.position == Suit.get_next_wind(player_position):
                text = 'next_win'
            elif self._winner.position == Suit.get_before_wind(player_position):
                text = 'before_win'
            else:
                text = 'opposite_win'
        else:
            text = 'draw'

        # show end screen
        self.draw_end_screen(result=result, text=text)

        # show scores board
        scores = []
        if not self._winner:
            # 流局
            self.screen.fill(Color.WHITE)
            self.draw_players(self.players, winner=None, score=0)
            self.waiting_return()
            return
        winner = self._winner
        by_self = False
        if self.winner == self.firer:
            by_self = True

        # 听绝张逻辑
        # total tiles
        left = self.mj_set.total
        # remove the desk tiles
        for p in self.players:
            left = MjMath.list_sub(left, p.desk)
        # remove the exposed tiles
        for p in self.players:
            if not p.exposed:
                continue
            for expose in p.exposed:
                if expose not in ['concealed kong']:
                    left = MjMath.list_sub(left, expose.all)
        # remove the concealed tiles
        if self._winner:
            left = MjMath.list_sub(left, self._winner.concealed)

        calculator = Calc(flowers=winner.flowers,
                          by_self=by_self, robbing_a_kong=self.robbing_a_kong,
                          mahjong_on_kong=self.mahjong_on_kong,
                          concealed=winner.concealed, exposed=winner.exposed,
                          winner_position=winner.position, prevailing_wind=self._prevailing_wind,
                          left=left
                          )
        scores = calculator.calc()
        print(scores)
        score = 0
        if scores:
            s = scores[len(scores) - 1]
            score = s[1]

        self.screen.fill(Color.WHITE)

        self.draw_players(self.players, self._winner, score, by_self=by_self, firer=self.firer)

        self.draw_score_screen(scores=scores,
                               concealed=winner.concealed, exposed=winner.exposed, flowers=winner.flowers)
        self.waiting_return()

    def draw_start_screen(self):
        start_group = pygame.sprite.Group()

        start_img = Setting.sprite_base + Setting.girl_img['start']
        image = pygame.image.load(start_img)
        rect = image.get_rect()
        rect.right = Setting.win_w // 2 - rect.w
        rect.centery = Setting.win_h // 2
        girl = pygame.sprite.Sprite()
        girl.image = image
        girl.rect = rect
        start_group.add(girl)

        start_img = Setting.sprite_base + Setting.btn_img['start']
        image = pygame.image.load(start_img)
        rect = image.get_rect()
        rect.centerx = Setting.win_w // 2
        rect.centery = Setting.win_h // 2
        btn = pygame.sprite.Sprite()
        btn.image = image
        btn.rect = rect
        start_group.add(btn)
        start_group.draw(self.screen)
        # self.draw_background()
        pygame.display.update()  # 显示

        self.waiting_return()

    def draw_end_screen(self, result: str = 'win', text: str = ''):
        score_group = pygame.sprite.Group()

        if result not in ['win', 'lose', 'draw']:
            raise ValueError(f"result:{result} not in ['win', 'lose', 'draw']")

        girl_face = result
        girl_img = Setting.sprite_base + Setting.girl_img[girl_face]
        image = pygame.image.load(girl_img)
        rect = image.get_rect()
        rect.right = Setting.win_w // 2 - rect.w
        rect.centery = Setting.win_h // 2
        girl = pygame.sprite.Sprite()
        girl.image = image
        girl.rect = rect
        score_group.add(girl)

        # hand result
        file = Setting.sprite_base + text + ".png"
        image = pygame.image.load(file)
        end_btn = Sprite(image)
        end_btn.rect.centerx = Setting.win_w // 2
        end_btn.rect.bottom = Setting.win_h // 2 - 100
        score_group.add(end_btn)

        # winner avatar
        if self.winner:
            file = Setting.avatar_base + self.winner.nick + ".png"
            image = pygame.image.load(file)
            avatar = Sprite(image)
            avatar.rect.centerx = Setting.win_w // 2
            avatar.rect.top = Setting.win_h // 2 + 80
            score_group.add(avatar)

        # end btn
        btn_img = Setting.sprite_base + Setting.btn_img['end']
        image = pygame.image.load(btn_img)
        rect = image.get_rect()
        rect.centerx = Setting.win_w // 2
        rect.centery = Setting.win_h // 2
        btn = pygame.sprite.Sprite()
        btn.image = image
        btn.rect = rect
        score_group.add(btn)
        score_group.draw(self.screen)
        # self.draw_background()
        pygame.display.update()  # 显示

        self.waiting_return()

    def draw_score_screen(self, scores, concealed, exposed, flowers):
        score_group = pygame.sprite.Group()

        if concealed:
            left = Setting.score_board_concealed_left
            bottom = Setting.score_board_concealed_bottom
            index = 0
            for tile in concealed:
                sprite = pygame.sprite.Sprite()
                image = pygame.image.load(Setting.tile_img_path + tile.img)
                rect = image.get_rect()
                sprite.image = image
                sprite.rect = rect
                sprite.rect.left = left
                sprite.rect.bottom = bottom
                left += rect.w
                if index == len(concealed) - 2:
                    left += rect.w
                index += 1
                score_group.add(sprite)

        if exposed:
            left = Setting.score_board_exposed_left
            bottom = Setting.score_board_exposed_bottom
            index = 0
            for expose in exposed:
                i2 = 0
                for tile in expose.all:
                    sprite = pygame.sprite.Sprite()
                    image = pygame.image.load(Setting.tile_img_path + tile.img)
                    rect = image.get_rect()
                    sprite.image = image
                    sprite.rect = rect
                    sprite.rect.left = left
                    sprite.rect.bottom = bottom
                    left += rect.w
                    index += 1
                    i2 += 1
                    score_group.add(sprite)
                left += rect.w

        girl_face = Setting.girl_img['start']
        girl_img = Setting.sprite_base + girl_face
        image = pygame.image.load(girl_img)
        rect = image.get_rect()
        rect.left = Setting.score_board_girl_left
        rect.top = Setting.score_board_girl_top
        girl = pygame.sprite.Sprite()
        girl.image = image
        girl.rect = rect
        score_group.add(girl)

        if flowers:
            left = Setting.score_board_flower_left
            top = Setting.score_board_girl_top + girl.rect.h + Setting.score_board_flower_y_span
            for index, tile in enumerate(flowers):
                if index != 0 and index % 6 == 0:
                    left = Setting.score_board_flower_left
                    top += rect.h + Setting.score_board_flower_y_span
                sprite = pygame.sprite.Sprite()
                image = pygame.image.load(Setting.tile_img_path + tile.img)
                rect = image.get_rect()
                sprite.image = image
                sprite.rect = rect
                sprite.rect.left = left
                sprite.rect.top = top
                left += rect.w
                score_group.add(sprite)

        # points
        font = pygame.font.Font(Setting.font, Setting.big_font_size)
        if scores:
            left = Setting.score_board_left
            bottom = Setting.score_board_bottom
            index = 0
            for score in scores[::-1]:
                # name
                # self.screen.blit(font.render(score[0], True, (0, 0, 0)), (left, bottom))
                image = font.render(score[0], True, Color.BLACK)
                rect = image.get_rect()
                rect.left, rect.bottom = left, bottom
                sprite = pygame.sprite.Sprite()
                sprite.image = image
                sprite.rect = rect
                score_group.add(sprite)

                # points
                if score[1]:
                    points = str(score[1]) + ' 番'
                else:
                    points = ''
                if index != 0:
                    image = font.render(points, True, Color.BLACK)
                else:
                    image = font.render(points, True, Color.RED)
                rect = image.get_rect()
                rect.right, rect.bottom = left + Setting.score_board_score_width, bottom
                sprite = pygame.sprite.Sprite()
                sprite.image = image
                sprite.rect = rect
                score_group.add(sprite)

                index += 1
                if index % 2 == 1:
                    left = Setting.score_board_left + Setting.score_board_score_width + Setting.score_board_score_x_span
                    bottom += 0
                else:
                    left = Setting.score_board_left
                    bottom += Setting.score_board_score_y_span

        score_group.draw(self.screen)
        pygame.display.update()  # 显示

    def waiting_return(self):
        allowed_cmd = ['discard']
        if not self._player:
            return
        self._player.waiting_4_cmd(allowed_cmd=allowed_cmd, draw_screen=False)

    def draw_players(self, players, winner, score, by_self=False, firer=None):
        if not players:
            raise ValueError("need players")

        players_group = pygame.sprite.Group()

        font = pygame.font.Font(Setting.font, Setting.normal_font_size)
        left = Setting.score_board_player_left
        bottom = Setting.win_h - Setting.score_board_player_bottom

        if not winner:
            winner = None
            bottom = Setting.win_h // 2
        if not score:
            score = 0

        for player in players:
            text = player.nick + ": " + str(player.coin)
            if player == winner:
                image = font.render(text, True, Color.RED)
            else:
                image = font.render(text, True, Color.BLACK)
            rect = image.get_rect()
            rect.left, rect.bottom = left, bottom
            sprite = pygame.sprite.Sprite()
            sprite.image = image
            sprite.rect = rect
            players_group.add(sprite)
            left += rect.w + 10
            if player == winner:
                if by_self:
                    text = "+ " + str((8 + score) * 3)
                else:
                    text = "+ " + str(8 * 3 + score)
                image = font.render(text, True, Color.RED)
            else:
                if by_self:
                    text = "- " + str(score + 8)
                elif player == firer:
                    text = "- " + str(score + 8)
                else:
                    text = "- " + str(8)
                image = font.render(text, True, Color.GREEN)
            rect = image.get_rect()
            rect.left, rect.bottom = left, bottom
            sprite = pygame.sprite.Sprite()
            sprite.image = image
            sprite.rect = rect
            players_group.add(sprite)

            left += Setting.score_board_player_x_span

        if by_self:
            for player in players:
                if player == winner:
                    player.coin += (8 + score) * 3
                else:
                    player.coin -= 8 + score
        else:
            for player in players:
                if player == winner:
                    player.coin += 8 * 3 + score
                elif player == firer:
                    player.coin -= 8 + score
                else:
                    player.coin -= 8

        players_group.draw(self.screen)
        pygame.display.update()  # 显示
