#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:55
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: suit.py
# @Software: Mahjong II
# @Blog    :


class Suit(object):
    """
    Warning:
        - don't change the 'base' attr for suit
        - the 'value' attr should be in range(100)
        * MjMath class calculations depend on this rules
    """
    Suit = {
        '万': {
            'base': 100,
            'eng': 'character',
            'text': '万',
        },
        '饼': {
            'base': 200,
            'eng': 'dot',
            'text': '饼',
        },
        '条': {
            'base': 300,
            'eng': 'bamboo',
            'text': '条',
        },
        '字': {
            'base': 400,
            'eng': 'dragon',
            'text': '字',
        },
        '风': {
            'base': 500,
            'eng': 'wind',
            'text': '风',
        },
        '季': {
            'base': 600,
            'eng': 'season',
            'text': '季',
        },
        '花': {
            'base': 700,
            'eng': 'flower',
            'text': '花',
        }
    }

    Wind = {
        '东': {
            'value': 10,
            'eng': 'east',
            'text': '东',
        },
        '南': {
            'value': 20,
            'eng': 'south',
            'text': '南',
        },
        '西': {
            'value': 30,
            'eng': 'west',
            'text': '西',
        },
        '北': {
            'value': 40,
            'eng': 'north',
            'text': '北',
        },
    }

    Flower = {
        '梅': {
            'value': 10,
            'eng': 'plum',
            'text': '梅',
        },
        '兰': {
            'value': 20,
            'eng': 'orchid',
            'text': '兰',
        },
        '竹': {
            'value': 30,
            'eng': 'bamboo',
            'text': '竹',
        },
        '菊': {
            'value': 40,
            'eng': 'chrysanthemum',
            'text': '菊',
        },
    }

    Season = {
        '春': {
            'value': 10,
            'eng': 'spring',
            'text': '春',
        },
        '夏': {
            'value': 20,
            'eng': 'summer',
            'text': '夏',
        },
        '秋': {
            'value': 30,
            'eng': 'autumn',
            'text': '秋',
        },
        '冬': {
            'value': 40,
            'eng': 'winter',
            'text': '冬',
        },
    }

    Dragon = {
        '中': {
            'value': 10,
            'eng': 'red',
            'text': '中',
        },
        '发': {
            'value': 20,
            'eng': 'green',
            'text': '发',
        },
        '白': {
            'value': 30,
            'eng': 'white',
            'text': '白',
        },
    }

    @classmethod
    def get_wind_by_index(cls, index):
        index = index % 4
        keys = [key for key in cls.Wind]
        if index < 0 or len(keys) < (index - 1):
            raise ValueError(f"index {index} out of range of Wind")
        key = keys[index]
        return key

    @classmethod
    def get_next_wind(cls, wind: str):
        if not wind:
            wind = '东'
        if wind not in cls.Wind:
            raise ValueError(f'{wind} not in Wind Enum')
        if wind == '北':
            return '东'
        bingo = False
        for test in cls.Wind:
            if bingo:
                return test
            if test == wind:
                bingo = True

    @classmethod
    def get_before_wind(cls, wind: str):
        if not wind:
            wind = '东'
        if wind not in cls.Wind:
            raise ValueError(f'{wind} not in Wind Enum')
        if wind == '东':
            return '北'
        bingo = False
        winds = [key for key in cls.Wind]
        for test in winds[::-1]:
            if bingo:
                return test
            if test == wind:
                bingo = True

    @classmethod
    def get_opposition_wind(cls, wind:str):
        return cls.get_next_wind(cls.get_next_wind(wind))


def test_wind():
    pass


def main():
    test_wind()
    pass
    

if __name__ == '__main__':
    main()
    