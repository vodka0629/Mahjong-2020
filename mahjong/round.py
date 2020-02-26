#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:57
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: round.py
# @Software: Mahjong II
# @Blog    :

from random import shuffle
from transitions import Machine
from mahjong.mj_set import MjSet
from mahjong.player import Player


class RoundStateMachine(object):
    pass


class Round(object):
    # In each round at least four hands are played, with each player taking the position of dealer.
    hands_limit = 4

    __slots__ = ("_state_machine", "_machine", "_states", "_transitions",
                 "_mj_set", "_players", "_dealer",
                 "_prevailing_wind"
                 )

    @property
    def state(self):
        return self._state_machine.state

    @property
    def players(self):
        return self._players

    @property
    def dealer(self):
        return self._dealer

    @players.setter
    def players(self, arr: list):
        count = len(arr)
        if count < 1 or 4 < count:
            raise ValueError("players count error: [1:4]")
        self._players = arr

    def __init__(self, prevailing_wind: str = '东'):
        self._dealer = None
        self._prevailing_wind = prevailing_wind

        # state machine
        self._state_machine = RoundStateMachine()
        self._states = ["begin", "in progress", "end"]
        self._transitions = [
            {'trigger': 'prepare', 'source': 'begin', 'dest': 'in progress'},
            {'trigger': 'calc_hand_wind', 'source': 'in progress', 'dest': 'end'},
        ]
        Machine(model=self._state_machine, states=self._states, transitions=self._transitions, initial='begin')

    def prepare(self):
        self._mj_set = MjSet()
        self.choice_dealer()


        self._state_machine.prepare()

    def choice_dealer(self):
        shuffle(self._players)
        self._dealer = None
        top = -1
        dealer_index = -1
        for index, player in enumerate(self._players):
            dice = player.throw_two_dice()
            if top < sum(dice):
                self._dealer = player
                top = sum(dice)
                dealer_index = index
        new_position = []
        count = len(self._players)
        for i in range(count):
            new_position.append(self._players[(dealer_index + i) % count])
        self._players = new_position
        self._dealer = self._players[0]



def main():
    round = Round()
    print(round.state)
    round.players = [
        Player('Eric'),
        Player('Nana'),
        Player('Sister'),
        Player('Brother'),
    ]
    round.prepare()
    print(round.dealer)
    print([f'{x} ' for x in round.players])
    print(round.state)


if __name__ == '__main__':
    main()
