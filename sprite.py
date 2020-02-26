#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:46
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: sprite.py
# @Software: Mahjong II
# @Blog    :

import pygame

class Sprite(pygame.sprite.Sprite):

    def __init__(self, image, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = image.get_rect()