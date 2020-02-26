#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:57
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: player.py
# @Software: Mahjong II
# @Blog    :

from random import randint, choice

from mahjong.error import *
from mahjong.expose import Expose
from mahjong.mj_math import MjMath
from mahjong.mj_set import MjSet
from mahjong.rule import Rule
from mahjong.suit import Suit
from mahjong.tile import Tile
from setting import Setting
from sprite import *


class Player(object):
    __slots__ = ('_nick', '_concealed', '_exposed', '_discarded', '_desk', 'discarding', 'flowers',

                 '_state', '_position',
                 '_coin', '_is_viewer', '_viewer_position',

                 '_draw_count', '_discard_by_random_count',

                 # for pygame screen
                 "_screen", "_font", "clock",
                 'current_index', 'current_tiles',
                 "concealed_group", "discarded_group", "exposed_group", "flowers_group",
                 "info_group", 'avatar', "all_group",

                 # for sound
                 "_sound_discard", "_sound_draw_stack",
                 "_sound_kong", "_sound_chow", "_sound_pong",
                 "_sound_hu", "_sound_self_hu",
                 )

    def __init__(self, nick="Eric", coin: int = 0, is_viewer: bool = False, viewer_position: str = '东',
                 screen=None, clock=None):
        self._nick = nick
        self._concealed: list = []
        self._exposed: list = []
        self._discarded: list = []
        self._desk: list = []
        self.flowers: list = []
        self.discarding = None

        self._state: str = ''
        self._position: str = ''

        self._coin = coin
        self._is_viewer = is_viewer
        self._viewer_position = viewer_position

        self.info_group = pygame.sprite.Group()
        self.concealed_group = pygame.sprite.Group()
        self.exposed_group = pygame.sprite.Group()
        self.discarded_group = pygame.sprite.Group()
        self.flowers_group = pygame.sprite.Group()
        avatar = Setting.avatar_base + nick + ".png"
        img = pygame.image.load(avatar)
        self.avatar = pygame.transform.scale(img, (64, 64))
        self.all_group = pygame.sprite.Group()

        self._screen = screen
        self.clock = clock
        self.current_index = -1
        self.current_tiles = []
        # self._font = pygame.font.SysFont(Setting.font, 16)
        # self._font.set_bold(True)

        self._discard_by_random_count = 0
        self._draw_count = 0

        self._sound_discard = pygame.mixer.Sound(Setting.sound_base + Setting.sound_discard)
        self._sound_draw_stack = pygame.mixer.Sound(Setting.sound_base + Setting.sound_draw_stack)

        self._sound_chow = pygame.mixer.Sound(Setting.sound_base + Setting.sound_chow)
        self._sound_pong = pygame.mixer.Sound(Setting.sound_base + Setting.sound_pong)
        self._sound_kong = pygame.mixer.Sound(Setting.sound_base + Setting.sound_kong)

        self._sound_hu = pygame.mixer.Sound(Setting.sound_base + Setting.sound_hu)
        self._sound_self_hu = pygame.mixer.Sound(Setting.sound_base + Setting.sound_self_hu)

    def __str__(self):
        return self._nick

    @property
    def nick(self):
        return self._nick

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def concealed(self):
        return self._concealed

    @property
    def concealed_str(self):
        arr = [f'{x}' for x in self._concealed]
        text = ",".join(arr)
        return text

    @property
    def exposed(self):
        return self._exposed

    @property
    def exposed_str(self):
        arr = [f'={x}=' for x in self._exposed]
        return ','.join(arr)

    @property
    def discarded(self):
        return self._discarded

    @property
    def desk(self):
        return self._desk

    @property
    def desk_str(self):
        arr = [f'{x}' for x in self._desk]
        text = ",".join(arr)
        return text

    @property
    def discard_by_random_count(self):
        return self._discard_by_random_count

    @property
    def draw_count(self):
        return self._draw_count

    @property
    def is_viewer(self):
        return self._is_viewer

    @is_viewer.setter
    def is_viewer(self, value):
        self._is_viewer = value

    @property
    def viewer_position(self):
        return self._viewer_position

    @viewer_position.setter
    def viewer_position(self, value):
        self._viewer_position = value

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self._screen = value

    @property
    def coin(self):
        return self._coin

    @coin.setter
    def coin(self, value):
        self._coin = value

    def reset(self):
        self._concealed = []
        self._exposed = []
        self._discarded = []
        self.flowers = []
        self._desk = []
        self._discard_by_random_count = 0
        self.discarding = None
        self.current_index = -1
        self.current_tiles = []

    def draw(self, mj_set: MjSet):
        tile = mj_set.draw()
        if not tile:
            print("mj_set.draw() None")
            return None
        if not Rule.is_flower(tile):
            self.add(tile)
            self._draw_count += 1
            return tile

        print(self, 'get a flower:', tile)
        self.flowers.append(tile)
        tile = self.draw_from_back(mj_set)
        print("draw_from_back:", tile)
        return tile

    def draw_from_back(self, mj_set: MjSet):
        tile = mj_set.draw_from_back()
        if not tile:
            print("mj_set.draw_from_back() None")
            return None
        while Rule.is_flower(tile) and mj_set.tiles:
            # (self, 'get a flower from back:', tile)
            self.flowers.append(tile)
            self._draw_count += 1
            tile = mj_set.draw_from_back()
            if not tile:
                print("mj_set.draw_from_back() is_flower None")
                return None
        self.add(tile)
        return tile

    def draw_stack(self, mj_set: MjSet):
        for _ in range(4):
            self.draw(mj_set)

    def add(self, tile: Tile):
        self._concealed.append(tile)

    def put_on_desk(self, tile: Tile):
        self._desk.append(tile)

    def discard(self, tile: Tile):
        if tile not in self._concealed:
            raise LookupError(f"{self.nick} have not tile:{tile}")

        self._concealed.remove(tile)
        self._discarded.append(tile)
        self.discarding = tile
        return tile

    def decide_discard(self) -> Tile:
        return self.decide_discard_random()

    def decide_discard_random(self):
        if not self.concealed:
            raise ValueError(f"{self.nick} have no concealed tiles!")
        # finally, random discard one
        tile = choice(self.concealed)
        self._discard_by_random_count += 1
        return tile

    def decide_discard_by_random_orphan(self):
        arr = Rule.convert_tiles_to_arr(self.concealed)
        orphans_arr = MjMath.get_orphans(arr)
        if not orphans_arr:
            return None
        one = choice(orphans_arr)
        tile = Rule.convert_key_to_tile(one)
        return tile

    def sort_concealed(self):
        arr = Rule.convert_tiles_to_arr(self._concealed)
        arr.sort()
        self._concealed = Rule.convert_arr_to_tiles(arr)

    @staticmethod
    def throw_dice():
        return randint(1, 6)

    @staticmethod
    def throw_two_dice():
        return tuple((randint(1, 6), randint(1, 6)))

    def try_conceal_kong(self, mj_set: MjSet) -> bool:
        if not self.concealed:
            return False
        if not mj_set.tiles:
            return False
        test_tiles = list(set(self.concealed))
        for x in test_tiles:
            count = self.concealed.count(x)
            if count >= 4:
                # concealed kong when possible
                self.concealed_kong(tile=x, mj_set=mj_set)
                return True
        return False

    def concealed_kong(self, tile: Tile, mj_set: MjSet):
        self._sound_kong.play()
        count = 0
        inners = []
        for x in self.concealed[::-1]:
            if x.key == tile.key:
                count += 1
                inners.append(x)
                self.concealed.remove(x)
                if count >= 4:
                    break
        expose = Expose(expose_type='concealed kong', inners=inners, outer=None, outer_owner=None)
        self._exposed.append(expose)
        tile = self.draw_from_back(mj_set)
        if not tile:
            raise OutOfTilesError()
        # 杠上开花
        if self.try_mahjong():
            raise HaveWinnerError(winner=self)

    def try_mahjong(self, tile=None) -> bool:
        test = self.concealed[:]
        if tile:
            test.append(tile)
        if Rule.is_mahjong(test):
            return True
        return False

    def try_exposed_kong_from_exposed_pong(self, mj_set: MjSet) -> bool:
        tile = self.concealed[-1]
        if not mj_set.tiles:
            return False
        if not self.exposed:
            return False
        for expose in self.exposed:
            if expose.expose_type == 'exposed pong' and expose.outer.key == tile.key:
                # 有杠就杠
                return self.exposed_kong_from_exposed_pong(tile=tile, expose=expose, mj_set=mj_set)
        return False

    def exposed_kong_from_exposed_pong(self, tile: Tile, expose: Expose, mj_set: MjSet) -> bool:
        self._sound_kong.play()
        expose.expose_type = 'exposed kong from exposed pong'
        expose.inners.append(tile)
        expose.all.append(tile)
        self.concealed.pop()
        tile = self.draw_from_back(mj_set)
        if not tile:
            raise OutOfTilesError()
            # 杠上开花
        if self.try_mahjong():
            raise HaveWinnerError(winner=self)
        return True

    def try_exposed_kong(self, tile: Tile, owner, mj_set: MjSet) -> bool:
        count = 0
        for test in self._concealed:
            if tile.key == test.key:
                count += 1
        if count == 3:
            self.exposed_kong(tile=tile, owner=owner, mj_set=mj_set)
            return True
        return False

    def exposed_kong(self, tile: Tile, owner, mj_set: MjSet):
        count = 0
        inner = []
        for test in self._concealed[::-1]:
            if tile.key == test.key:
                inner.append(test)
                self._concealed.remove(test)
                count += 1
                if count == 3:
                    break
        if count < 3:
            raise ValueError(f"{self.nick} don't have enough {tile}!")
        expose = Expose('exposed kong', inners=inner, outer=tile, outer_owner=owner)
        self._exposed.append(expose)
        self._sound_kong.play()
        tile = self.draw_from_back(mj_set)
        if not tile:
            raise OutOfTilesError()
        # 杠上开花
        if self.try_mahjong():
            raise HaveWinnerError(winner=self)

    def try_exposed_pong(self, tile: Tile, owner) -> bool:
        count = 0
        for test in self._concealed:
            if tile.key == test.key:
                count += 1
        if count >= 2:
            self.exposed_pong(tile=tile, owner=owner)
            return True
        return False

    def exposed_pong(self, tile: Tile, owner):
        count = 0
        inner = []
        for test in self._concealed[::-1]:
            if tile.key == test.key:
                inner.append(test)
                self._concealed.remove(test)
                count += 1
                if count == 2:
                    break
        if count < 2:
            raise ValueError(f"{self.nick} don't have enough {tile}!")
        expose = Expose('exposed pong', inners=inner, outer=tile, outer_owner=owner)
        self._exposed.append(expose)

    def try_exposed_chow(self, tile: Tile, owner) -> bool:
        arr = Rule.convert_tiles_to_arr(self.concealed)
        outer = tile.key

        # 胡吃一气
        combins = MjMath.get_chow_combins_from_arr(arr=arr, outer=outer)
        if not combins:
            return False
        combin = choice(combins)
        inners = Rule.convert_arr_to_tiles(combin)
        self.exposed_chow(inners=inners, tile=tile, owner=owner)
        return True

    def exposed_chow(self, inners, tile, owner):
        if len(inners) != 2:
            raise ValueError(f"self_tiles length should be 2:{inners}")
        for x in inners:
            for test in self._concealed[::-1]:
                if x.key == test.key:
                    self._concealed.remove(test)
                    break

        expose = Expose('exposed chow', inners=inners, outer=tile, outer_owner=owner)
        self._exposed.append(expose)

    def draw_info(self):
        self.info_group.empty()

        centerx = Setting.win_w // 2
        bottom = Setting.win_h // 2 - 100
        # draw player's position
        # file_name = Setting.sprite_base + Suit.Wind[self.position]['eng'] + ".png"
        # image = pygame.image.load(file_name)
        # sprite = pygame.sprite.Sprite()
        # sprite.image = image
        # rect = image.get_rect()
        # rect.centerx = centerx
        # rect.bottom = bottom
        # sprite.rect = rect
        # self.info_group.add(sprite)

        # draw player's discarding tile
        if self.discarding:
            # centerx += sprite.rect.w
            file_name = Setting.tile_img_path + self.discarding.img
            image = pygame.image.load(file_name)
            sprite = pygame.sprite.Sprite()
            sprite.image = image
            rect = image.get_rect()
            rect.centerx = centerx
            rect.bottom = bottom
            sprite.rect = rect
            self.info_group.add(sprite)

    def draw_concealed(self, state: str = ''):
        self.concealed_group.empty()
        left = Setting.concealed_left
        bottom = Setting.concealed_bottom

        for index, tile in enumerate(self.concealed):
            sprite = pygame.sprite.Sprite()
            if self._is_viewer or state == 'scoring':
                image = pygame.image.load(Setting.tile_img_path + tile.img)
            else:
                image = pygame.image.load(Setting.tile_img_path + Setting.face_down_img)

            rect = image.get_rect()
            if not self._is_viewer:
                rect.w, rect.h = rect.w // 4 * 3, rect.h // 4 * 3
                image = pygame.transform.scale(image, (rect.w, rect.h))

            sprite.image = image
            sprite.rect = rect
            sprite.rect.left = left
            sprite.rect.bottom = bottom
            if self.is_viewer and index in self.current_tiles:
                sprite.rect.bottom += Setting.current_jump
            self.concealed_group.add(sprite)

            left += sprite.rect.width

    def draw_discard(self, state: str = ''):
        self.discarded_group.empty()
        left = Setting.discarded_left
        bottom = Setting.discarded_bottom

        for index, tile in enumerate(self.desk):
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(Setting.tile_img_path + tile.img)
            rect = image.get_rect()
            rect.w, rect.h = rect.w // 4 * 3, rect.h // 4 * 3
            image = pygame.transform.scale(image, (rect.w, rect.h))
            sprite.image = image
            sprite.rect = rect
            sprite.rect.left = left
            sprite.rect.bottom = bottom
            self.discarded_group.add(sprite)
            left += rect.width
            if index != 0 and (index + 1) % Setting.discarded_line_limit == 0:
                left += min(rect.width, rect.height)
            if index != 0 and (index + 1) % (Setting.discarded_line_limit * 2) == 0:
                left = Setting.discarded_left
                bottom += max(rect.w, rect.h) + 5

    def draw_flowers(self, state: str = ''):
        self.flowers_group.empty()

        left = Setting.flowers_left
        bottom = Setting.discarded_bottom

        for index, tile in enumerate(self.flowers):
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(Setting.tile_img_path + tile.img)
            rect = image.get_rect()
            rect.w, rect.h = rect.w // 2, rect.h // 2
            image = pygame.transform.scale(image, (rect.w, rect.h))
            sprite.image = image
            sprite.rect = rect
            sprite.rect.right = left
            sprite.rect.bottom = bottom
            self.flowers_group.add(sprite)
            left -= rect.width
            if index != 0 and (index + 1) % (Setting.flower_line_limit) == 0:
                left = Setting.flowers_left
                bottom += max(rect.w, rect.h) + 5

    def draw_exposed(self, state: str = ''):
        self.exposed_group.empty()
        left = Setting.exposed_left
        bottom = Setting.exposed_bottom

        for exposed in self.exposed:
            space_width = 0
            for i2, tile in enumerate(exposed.all):
                sprite = pygame.sprite.Sprite()
                adjust = 0  # adjust for exposed chow / pong / kong
                image = pygame.image.load(Setting.tile_img_path + tile.img)

                # lay down the tile for chow
                if exposed.expose_type == "exposed chow":
                    if tile == exposed.outer:
                        adjust = 90

                # lay down the tile for pong
                if exposed.expose_type == "exposed pong":
                    if exposed.outer_owner.position == Suit.get_before_wind(self.position):
                        if i2 == 0:
                            adjust = 90
                    if exposed.outer_owner.position == Suit.get_next_wind(self.position):
                        if i2 == 2:
                            adjust = 90
                    if exposed.outer_owner.position != Suit.get_before_wind(self.position) and \
                            exposed.outer_owner.position != Suit.get_next_wind(self.position):
                        if i2 == 1:
                            adjust = 90

                # lay down the tile for kong
                if exposed.expose_type in ["exposed kong", "exposed kong from exposed pong"]:
                    if exposed.outer_owner.position == Suit.get_before_wind(self.position):
                        if i2 == 0:
                            adjust = 90
                    if exposed.outer_owner.position == Suit.get_next_wind(self.position):
                        if i2 == 2:
                            adjust = 90
                    if exposed.outer_owner.position != Suit.get_before_wind(self.position) and \
                            exposed.outer_owner.position != Suit.get_next_wind(self.position):
                        if i2 == 3:
                            adjust = 90

                # cover the concealed kong
                if exposed.expose_type == "concealed kong" and state != 'scoring':
                    image = pygame.image.load(Setting.tile_img_path + Setting.face_down_img)
                    pass

                image = pygame.transform.rotate(image, adjust)
                rect = image.get_rect()
                rect.w, rect.h = rect.w // 4 * 3, rect.h // 4 * 3
                image = pygame.transform.scale(image, (rect.w, rect.h))
                sprite.image = image
                sprite.rect = rect
                sprite.rect.left = left
                sprite.rect.bottom = bottom
                self.exposed_group.add(sprite)

                left += sprite.rect.width
                space_width = min(sprite.rect.width, sprite.rect.height)
            # end for an expose

            left += space_width
            # end for exposed

    def adjust_screen_position_for_left_bottom(self):
        self.all_group.empty()
        for sprite in self.concealed_group:
            self.all_group.add(sprite)
        for sprite in self.exposed_group:
            self.all_group.add(sprite)
        for sprite in self.discarded_group:
            self.all_group.add(sprite)
        for sprite in self.flowers_group:
            self.all_group.add(sprite)

        for sprite in self.all_group:
            img_original = sprite.image
            rect_original = sprite.rect
            rotated = None
            rect = None
            left, bottom = rect_original.left, rect_original.bottom
            if self._is_viewer:
                left += Setting.win_w_h_half
                rotated = img_original
                rect = rect_original
                rect.left, rect.bottom = left, Setting.win_h - bottom
            elif self.position == Suit.get_next_wind(self._viewer_position):
                angel = 90
                rotated = pygame.transform.rotate(img_original, angel)
                rect = rotated.get_rect()
                rect.bottom, rect.right = Setting.win_h - left, Setting.win_w - bottom
            elif self.position == Suit.get_before_wind(self._viewer_position):
                angel = 270
                rotated = pygame.transform.rotate(img_original, angel)
                rect = rotated.get_rect()
                rect.top, rect.left = left, bottom
            elif self.position == Suit.get_opposition_wind(self._viewer_position):
                left += Setting.win_w_h_half
                angel = 180
                rotated = pygame.transform.rotate(img_original, angel)
                rect = rotated.get_rect()
                rect.right, rect.top = Setting.win_w - left, bottom
            else:
                sprite.kill()

            sprite.image = rotated
            sprite.rect = rect

    def adjust_screen_position_for_centerx_bottom(self):

        for sprite in self.info_group:
            img_original = sprite.image
            rect_original = sprite.rect
            rotated = None
            rect = None
            centerx, bottom = rect_original.centerx, rect_original.bottom
            if self._is_viewer:
                rotated = img_original
                rect = rect_original
                rect.centerx, rect.bottom = centerx, Setting.win_h - bottom
            elif self.position == Suit.get_next_wind(self._viewer_position):
                angel = 90
                rotated = pygame.transform.rotate(img_original, angel)
                rect = rotated.get_rect()
                rect.centery, rect.right = (Setting.win_h - Setting.win_w) // 2 + centerx, Setting.win_w - bottom
            elif self.position == Suit.get_before_wind(self._viewer_position):
                angel = 270
                rotated = pygame.transform.rotate(img_original, angel)
                rect = rotated.get_rect()
                rect.centery, rect.left = (Setting.win_h - Setting.win_w) // 2 + centerx, bottom
            elif self.position == Suit.get_opposition_wind(self._viewer_position):
                angel = 180
                rotated = pygame.transform.rotate(img_original, angel)
                rect = rotated.get_rect()
                rect.centerx, rect.top = centerx, bottom
            else:
                sprite.kill()

            sprite.image = rotated
            sprite.rect = rect

    def draw_screen(self, state: str = ''):

        if not self._screen:
            return

        self.draw_info()
        self.draw_concealed(state)
        self.draw_exposed(state)
        self.draw_discard()
        self.draw_flowers()

        self.adjust_screen_position_for_centerx_bottom()
        self.adjust_screen_position_for_left_bottom()
        self.info_group.draw(self._screen)
        self.all_group.draw(self._screen)


def test_exposed_chow():
    # mj_set = MjSet()
    # player = Player("Eric")
    # owner = Player("Nana")
    # for _ in range(2):
    #     for x in range(3):
    #         mj_set.draw_from_back()
    #     player.draw_from_back(mj_set)
    # for x in range(3):
    #     mj_set.draw_from_back()
    # sample = mj_set.draw_from_back()
    # for _ in range(3):
    #     for x in range(3):
    #         mj_set.draw_from_back()
    #     player.draw_from_back(mj_set)
    #
    # mj_set.shuffle()
    # for _ in range(6):
    #     player.draw(mj_set)
    # print(Rule.convert_tiles_to_str(player.concealed))
    # print(sample)
    # player.try_exposed_chow(sample, owner)
    # print(','.join([f'{x.expose_type}:{x}' for x in player.exposed]))
    print("test_exposed_chow")
    pass


def main():
    test_exposed_chow()
    pass


if __name__ == '__main__':
    main()
