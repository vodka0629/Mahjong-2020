#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 15:57
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: hand.py
# @Software: Mahjong II
# @Blog    :

from itertools import cycle

from transitions import Machine

from mahjong.mj_math import MjMath
from mahjong.mj_set import MjSet
from mahjong.player import Player
from mahjong.player_ai import PlayerAi
from mahjong.player_ai_adv import PlayerAiAdv
from mahjong.rule import Rule
from mahjong.suit import Suit


class HandStateMachine(object):
    pass


class Hand(object):
    __slots__ = ("_state_machine", "_machine", "_states", "_transitions",
                 "_mj_set", "_players", "_prevailing_wind", "_dealer", '_positions',
                 '_winner', 'firer', 'out_of_tiles', 'robbing_a_kong', 'mahjong_on_kong'
                 )

    def __init__(self, players: list = None, prevailing_wind: str = '东', flower=False):
        if not players:
            raise ValueError("mahjong needs player!")
        self._mj_set = MjSet(flower)
        self.out_of_tiles = False
        self.robbing_a_kong = False
        self.mahjong_on_kong = False
        self._players = players
        self._positions = dict()
        for index, player in enumerate(self._players):
            wind = Suit.get_wind_by_index(index)
            player.position = wind
            self._positions[wind] = player
        self._dealer: Player = self._players[0]
        self._prevailing_wind = prevailing_wind
        self._winner = None
        self.firer = None

        # state machine
        self._state_machine = HandStateMachine()
        self._states = ["begin", "prepared", "playing", "scoring", "end"]
        self._transitions = [
            {'trigger': 'prepare', 'source': 'begin', 'dest': 'prepared'},  # 准备
            {'trigger': 'deal', 'source': 'prepared', 'dest': 'playing'},  # 拿四张
            {'trigger': 'mahjong', 'source': 'playing', 'dest': 'scoring'},  # 胡牌
            {'trigger': 'withdraw', 'source': 'playing', 'dest': 'scoring'},  # 流局
            {'trigger': 'score', 'source': 'scoring', 'dest': 'end'},  # 算分
        ]
        Machine(model=self._state_machine, states=self._states, transitions=self._transitions, initial='begin')
        # print(self.state)

    def __str__(self):
        return '\r\n'.join([f'{x.position}:{x}' for x in self._players])

    @property
    def state(self):
        return self._state_machine.state

    @property
    def players(self):
        return self._players

    @property
    def mj_set(self):
        return self._mj_set

    @property
    def dealer(self):
        return self._dealer

    @property
    def winner(self):
        return self._winner

    @property
    def positions(self):
        return self._positions

    def _shuffle(self):
        self._mj_set.shuffle()

    def _reset_players(self):
        for player in self._players:
            player.reset()

    def _get_next_player(self, current):
        bingo = False
        for player in cycle(self.players):
            if bingo:
                return player
            if current == player:
                bingo = True
        raise LookupError(f"can not find next player for {current}")

    def prepare(self):
        self._reset_players()
        self._state_machine.prepare()
        self._shuffle()

    def deal(self):
        for _ in range(max(MjMath.concealed_count) // 4):
            for player in self._players:
                player.draw_stack(self._mj_set)

        for player in self.players:
            player.draw(self._mj_set)
            player.sort_concealed()

        self._state_machine.deal()

    def play(self):

        current = self._dealer  # the current player
        player = current
        before = None  # the previous player
        current_discard = None  # discard tile by previous player

        for player in self._players:
            print(f'{player.position}: {player}')
        print("=" * 40)

        have_winner = False
        while not have_winner:

            if current_discard:
                wind = current.position
                player = current
                for index in range(3):
                    # test for hu by other
                    test = player.concealed[:]
                    test.append(current_discard)
                    if Rule.is_mahjong(test):
                        player.concealed.append(current_discard)
                        print(f"winner is {player}, by {before}")
                        self._winner = player
                        self._state_machine.mahjong()
                        have_winner = True
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
                        if player.try_exposed_kong(tile=current_discard, owner=before, mj_set=self._mj_set):
                            interrupted = True
                            break
                        wind = Suit.get_next_wind(wind)
                        player = self.positions[wind]

                # try pong:
                if not interrupted:
                    wind = current.position
                    player = current
                    for index in range(3):
                        if player.try_exposed_pong(tile=current_discard, owner=before):
                            interrupted = True
                            break
                        wind = Suit.get_next_wind(wind)
                        player = self.positions[wind]

                # try chow:
                if not interrupted:
                    wind = current.position
                    player = current
                    if player.try_exposed_chow(current_discard, before):
                        interrupted = True

                if not interrupted:
                    before.put_on_desk(current_discard)
            # end if current_discard:

            if interrupted:
                current = player
            else:
                # test for out of tiles
                if not self.mj_set.tiles:
                    print("out of tiles!")
                    self._winner = None
                    self._state_machine.withdraw()
                    break

                # draw
                current.draw(self._mj_set)
                # test for hu by self
                if Rule.is_mahjong(current.concealed):
                    print(f"winner is {current}, by self!")
                    self._winner = current
                    self._state_machine.mahjong()
                    break

                # self kong
                current.try_conceal_kong(self.mj_set)

            if isinstance(current, PlayerAiAdv):
                wall = self._mj_set.tiles
                tile = current.decide_discard(players_count=len(self.players), wall=wall)
            else:
                tile = current.decide_discard()
            print(current, 'discard:', tile)
            current.discard(tile)
            current.sort_concealed()
            current_discard = tile

            # (f'{current} discard {tile}')
            # (Rule.convert_tiles_to_str(current.concealed))

            # next player
            next = self._get_next_player(current)
            before = current
            current = next
        # end while

        print("tiles left :", len(self.mj_set.tiles))
        for player in self.players:
            if player == self.winner:
                print(f"winner {player}: ", Rule.convert_tiles_to_str(player.concealed))
            else:
                print(f"{player}: ", Rule.convert_tiles_to_str(player.concealed))

        left = Rule.convert_tiles_to_arr(self.mj_set.tiles)
        left.sort()
        print(self.players[0].strategies)
        print(self.players[0].strategies_time)

    # end def play()

    def score(self):
        # score the play result
        self._state_machine.score()
        pass


def main():
    test_play_once()
    # test_play_100()


def test_play_100():
    winners = {}
    for _ in range(100):
        nick = ""
        winner = test_play_once()
        if not winner:
            nick = "draw"
        else:
            nick = winner.nick
        if nick not in winners:
            winners[nick] = 0
        winners[nick] += 1
    print(winners)


def test_play_once():
    players = [
        PlayerAiAdv('Eric'),
        PlayerAi('Nana'),
        PlayerAi('Sister'),
        PlayerAi('Brother'),
    ]
    prevailing_wind = '东'
    hand = Hand(players=players, prevailing_wind=prevailing_wind)
    hand.prepare()
    hand.deal()
    hand.play()
    print(hand.winner)
    hand.score()
    return hand.winner


if __name__ == '__main__':
    main()
