#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:44
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: calc.py
# @Software: Mahjong II
# @Blog    :

import copy

from mahjong.expose import Expose
from mahjong.mj_math import MjMath
from mahjong.mj_set import MjSet
from mahjong.rule import Rule
from mahjong.suit import Suit


class Calc(object):
    __slots__ = ("concealed", "exposed", "flowers", "winner_position", "prevailing_wind",
                 "by_self", "robbing_a_kong", "mahjong_on_kong",
                 "best_group", "left")

    def __init__(self, concealed=None, exposed=None, flowers=None,
                 winner_position: str = '', prevailing_wind: str = '',
                 by_self: bool = False, robbing_a_kong: bool = False, mahjong_on_kong: bool = False,
                 left=None):
        self.concealed = []
        if concealed:
            self.concealed = concealed[:]
        self.exposed = exposed
        self.flowers = flowers

        self.winner_position = winner_position
        self.prevailing_wind = prevailing_wind

        self.by_self = by_self
        self.robbing_a_kong = robbing_a_kong
        self.mahjong_on_kong = mahjong_on_kong
        self.left = left

        self.best_group = []

    def calc(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        print("arr:", arr)

        scores = []
        # 不需分组就能判定的分数 scores don't depend on meld
        # 1 番
        scores.append(self.自摸())
        scores.append(self.无字())
        scores.append(self.缺一门())
        scores.append(self.明杠())
        # 2 番
        scores.append(self.断幺())
        scores.append(self.暗杠())
        scores.append(self.四归一())
        scores.append(self.门前清())
        scores.append(self.门风刻())
        scores.append(self.圈风刻())
        scores.append(self.箭刻())
        # 4 番
        scores.append(self.和绝张())
        scores.append(self.双明杠())
        scores.append(self.不求人())
        # 6 番
        scores.append(self.双暗杠())
        scores.append(self.全求人())
        # 8 番
        scores.append(self.抢杠和())
        scores.append(self.杠上开花())
        scores.append(self.海底捞月())
        scores.append(self.妙手回春())
        scores.append(self.推不倒())
        # 12 番
        scores.append(self.三风刻())
        scores.append(self.小于五())
        scores.append(self.大于五())
        scores.append(self.组合龙())
        scores.append(self.全不靠())
        # 24 番
        scores.append(self.全小())
        scores.append(self.全中())
        scores.append(self.全大())
        scores.append(self.七星不靠())
        # 32 番
        scores.append(self.三杠())
        # 64 番
        scores.append(self.四暗刻())
        # 88 番
        scores.append(self.连七对())
        scores.append(self.十三幺())
        scores.append(self.四杠())
        scores.append(self.九莲宝灯())
        scores.append(self.绿一色())

        groups = self.get_mahjong_combins_by_suit_group(with_exposed=True)
        if groups:
            g_scores = dict()
            for index, g in enumerate(groups):
                g_score = []
                # 1 番
                g_score.append(self.单钓g(g))
                g_score.append(self.坎张g(g))
                g_score.append(self.边张g(g))
                g_score.append(self.幺九刻g(g))
                g_score.append(self.老少副g(g))
                g_score.append(self.连六g(g))
                g_score.append(self.喜相逢g(g))
                g_score.append(self.一般高g(g))
                # 2 番
                g_score.append(self.双暗刻g(g))
                g_score.append(self.双同刻g(g))
                g_score.append(self.平和g(g))
                # 4 番
                g_score.append(self.全带幺g(g))
                # 6 番
                g_score.append(self.双箭刻g(g))
                g_score.append(self.五门齐g(g))
                g_score.append(self.三色三步高g(g))
                g_score.append(self.混一色g(g))
                g_score.append(self.碰碰和g(g))
                # 8 番
                g_score.append(self.三色三节高g(g))
                g_score.append(self.三色三同顺g(g))
                g_score.append(self.花龙g(g))
                # 16 番
                g_score.append(self.三暗刻g(g))
                g_score.append(self.三同刻g(g))
                g_score.append(self.全带五g(g))
                g_score.append(self.一色三步高g(g))
                g_score.append(self.三色双龙会g(g))
                g_score.append(self.清龙g(g))
                # 24 番
                g_score.append(self.一色三节高g(g))
                g_score.append(self.一色三同顺g(g))
                g_score.append(self.清一色g(g))
                # 32 番
                g_score.append(self.混幺九g(g))
                g_score.append(self.一色四步高g(g))
                # 48 番
                g_score.append(self.一色四节高g(g))
                g_score.append(self.一色四同顺g(g))
                # 64 番
                g_score.append(self.一色双龙会g(g))
                g_score.append(self.字一色g(g))
                g_score.append(self.小三元g(g))
                g_score.append(self.小四喜g(g))
                g_score.append(self.清幺九g(g))
                # 88 番
                g_score.append(self.大三元g(g))
                g_score.append(self.大四喜g(g))

                forbids = []
                for score in g_score[::-1]:
                    if not score:
                        g_score.remove(score)
                        continue
                    forbid = score[2]
                    if forbid:
                        forbids += forbid
                if forbids:
                    for score in g_score[::-1]:
                        if score in forbids:
                            g_score.remove(score)

                g_scores[index] = g_score
            # end for groups
            # ("g_scores:", g_scores)

            # select the best group
            max_index = -1
            maximum = -1
            for index in g_scores:
                total = 0
                for score in g_scores[index]:
                    if not score:
                        continue
                    total += score[1]
                if maximum < total:
                    maximum = total
                    max_index = index

            # add the group score to total score
            if maximum > -1:
                scores += g_scores[max_index]
                self.best_group = groups[max_index]

        forbids = []
        for score in scores[::-1]:
            if not score:
                scores.remove(score)
                continue
            forbid = score[2]
            if forbid:
                forbids += forbid

        if forbids:
            for score in scores[::-1]:
                if score[0] in forbids:
                    scores.remove(score)
                    continue

        # 无番和
        if not scores:
            scores.append(('无番和', 8, []))
        # 1 番
        flowers = self.花牌()
        if flowers:
            scores.append(flowers)
        # sum all as total
        total = 0
        if scores:
            for score in scores:
                total += score[1]
        scores.append(('', '', []))
        scores.append(('总计', total, []))

        return scores

    def get_mahjong_combins_by_suit_group(self, with_exposed: bool = True):
        combins = self.get_mahjong_combins(with_exposed=with_exposed)
        if not combins:
            return []
        groups = []
        for combin in combins:
            group = {}
            for meld in combin:
                suit = meld[0] // 100 * 100
                meld_value = []
                for x in meld:
                    value = x % 100
                    meld_value.append(value)
                if suit not in group:
                    group[suit] = []
                group[suit].append(meld_value)
            groups.append(group)
        return groups

    def get_mahjong_combins(self, with_exposed: bool = True):
        tiles = self.concealed[:]
        arr = Rule.convert_tiles_to_arr(tiles)
        arr.sort()

        combins = MjMath.get_best_meld_combins_from_arr(arr)
        candidates = []

        if combins:
            for combin in combins:
                candidate = []
                long = []
                for meld in combin:
                    if not meld:
                        continue
                    candidate.append(meld)
                    long += meld
                left = MjMath.list_sub(arr, long)
                eyes = MjMath.get_pair_keys(left)
                if not eyes or len(eyes) != 1:
                    continue
                else:
                    eye = eyes[0]
                    candidate.append([eye, eye])
                candidates.append(candidate)
            # end for
        else:
            eyes = MjMath.get_pair_keys(arr)
            if not eyes or len(eyes) != 1:
                pass
            candidate = []
            eye = eyes[0]
            candidate.append([eye, eye])
            candidates.append(candidate)

        if not candidates:
            return []

        if with_exposed and self.exposed:
            for expose in self.exposed:
                meld = expose.all
                meld_arr = Rule.convert_tiles_to_arr(meld)
                meld_arr.sort()
                for candidate in candidates:
                    candidate.append(meld_arr)

        return candidates

    def convert_tiles_to_arr(self, with_exposed: bool = True):
        arr = Rule.convert_tiles_to_arr(self.concealed)
        if with_exposed and self.exposed:
            for expose in self.exposed:
                arr += [x.key for x in expose.all]
        return arr

    # 81、花牌：每花计1番。不计在起和番内，和牌后才能计番。花牌补花成和计自摸，不计杠上开花。
    def 花牌(self):
        if self.flowers:
            count = len(self.flowers)
            return ('花牌', count, [])
        return False

    # 80、自摸：自己摸进牌成和牌。
    def 自摸(self):
        if self.by_self:
            return ('自摸', 1, [])
        return False

    # 79、单钓：钓单张牌做将牌成基本和牌型，且整手牌只听这一种牌。
    def 单钓g(self, g: list):
        arr = self.convert_tiles_to_arr(with_exposed=False)
        last = arr.pop()

        group = copy.deepcopy(g)
        for s in group:
            for meld in group[s]:
                if len(meld) == 2:
                    if last != s + meld[0]:
                        return False

        # only waiting for 'last'
        if arr.count(last) < 1:
            return False
        is_ready = MjMath.is_ready(arr)
        if not is_ready[0]:
            return False
        if len(is_ready[1]) > 1:
            return False
        return ('单钓', 1, [])

    # 坎（嵌）张：听顺子中间的一张牌成基本和牌型，且整手牌只听这一种牌。
    def 坎张g(self, g: list):
        arr = self.convert_tiles_to_arr(with_exposed=False)
        last = arr.pop()

        group = copy.deepcopy(g)
        bingo = False
        for s in group:
            for meld in group[s]:
                if MjMath.is_123(meld):
                    if last == s + meld[1]:
                        bingo = True

        if not bingo:
            return False

        # only waiting for 'last'
        is_ready = MjMath.is_ready(arr)
        if not is_ready[0]:
            return False
        if len(is_ready[1]) > 1:
            return False

        return ('坎张', 1, [])

    # 77、边张：听顺子123的3或者789的7成基本和牌型，且整手牌只听这一种牌。
    def 边张g(self, g: list):
        arr = self.convert_tiles_to_arr(with_exposed=False)
        last = arr.pop()
        value = last % 100
        if value not in (3, 7):
            return False

        group = copy.deepcopy(g)
        bingo = False
        for s in group:
            for meld in group[s]:
                if MjMath.is_123(meld):
                    meld.sort()
                    if last == s + 3 and value == meld[2]:
                        bingo = True
                    if last == s + 7 and value == meld[0]:
                        bingo = True

        if not bingo:
            return False

        # only waiting for 'last'
        is_ready = MjMath.is_ready(arr)
        if not is_ready[0]:
            return False
        if len(is_ready[1]) > 1:
            return False

        return ('边张', 1, [])

    # 76、无字：和牌中没有字牌。
    def 无字(self):
        tiles = self.concealed[:]

        if self.exposed:
            for expose in self.exposed:
                tiles += expose.all

        test = set(tiles)
        for x in test:
            if x.suit in "字风":
                return False
        return ('无字', 1, [])

    # 75、缺一门：和牌中只包含两种花色序数牌。
    def 缺一门(self):
        tiles = self.concealed[:]
        if self.exposed:
            for expose in self.exposed:
                tiles += expose.all

        suits = set([tile.suit for tile in tiles])
        test = suits & {'万', '饼', '条'}
        if len(test) == 2:
            return ('缺一门', 1, [])

        return False

    # 74、明杠：手中有暗刻，他家打出一张与之相同的牌开杠，或者有碰出的刻子，摸进一张与之相同的牌开杠。
    def 明杠(self):
        if not self.exposed:
            return False

        count = 0
        for x in self.exposed:
            if x.expose_type in ['exposed kong', 'exposed kong from exposed pong']:
                count += 1

        if not count:
            return False
        return ('明杠', count, [])

    # 73、幺九刻：由幺九牌组成的刻子（杠），每副计1番。
    def 幺九刻g(self, g: dict):
        group = copy.deepcopy(g)
        count = 0
        prevailing_wind_key = -1
        winner_position_key = -1
        if self.prevailing_wind:
            prevailing_wind_key = Suit.Wind[self.prevailing_wind]['value']
        if self.winner_position:
            winner_position_key = Suit.Wind[self.winner_position]['value']

        for suit in group:
            if suit == 400:
                continue
            for meld in group[suit]:
                if not MjMath.is_111(meld) and not MjMath.is_1111(meld):
                    continue
                if len(meld) == 2:
                    continue
                if meld[0] in (prevailing_wind_key, winner_position_key):
                    continue
                if (meld[0] % 100) in (1, 9, 10, 20, 30, 40):
                    count += 1

        if not count:
            return False
        return ('幺九刻', count, [])

    # 72、老少副：同一种花色的123、789两副顺子。可复计。
    def 老少副g(self, g: dict):
        group = copy.deepcopy(g)
        count = 0
        need = [[1, 2, 3], [7, 8, 9]]
        for suit in group:
            # most contains 2 need group
            melds = group[suit]
            if need[0] not in melds or need[1] not in melds:
                continue
            count += 1
            melds = MjMath.list_sub(melds, need)
            if need[0] not in melds or need[1] not in melds:
                continue
            count += 1

        if not count:
            return False
        return ('老少副', count, [])

    # 71、连六：同一种花色序数相连6张牌组成的两副顺子。可复计。
    def 连六g(self, g: dict):
        group = copy.deepcopy(g)
        count = 0
        for suit in group:
            melds = group[suit]
            for test in melds[::-1]:
                if not MjMath.is_123(test):
                    melds.remove(test)
            if len(melds) < 2:
                continue
            test = melds[0]
            test_next = [test[0] + 3, test[1] + 3, test[2] + 3]
            if test_next in melds:
                count += 1
                melds.remove(test)
                melds.remove(test_next)
            if len(melds) < 2:
                continue
            test = melds[0]
            test_next = [test[0] + 3, test[1] + 3, test[2] + 3]
            if test_next in melds:
                count += 1

        if not count:
            return False
        return ('连六', count, [])

    # 70、喜相逢：两种花色序数相同的两副顺子。可复计。
    def 喜相逢g(self, g: dict):
        group = copy.deepcopy(g)
        count = 0
        for suit in group:
            melds = group[suit]
            if not melds:
                continue
            melds_unique = []
            for x in melds:
                if x not in melds_unique:
                    melds_unique.append(x)
            for meld in melds_unique:
                if not MjMath.is_123(meld):
                    continue
                for suit_test in group:
                    if suit == suit_test:
                        continue
                    melds_test = group[suit_test]
                    if meld in melds_test:
                        count += 1
                        break

        if not count:
            return False
        count = count // 2
        if count == 0:
            return False
        return ('喜相逢', count, [])

    # 69、一般高：同一种花色两副相同的顺子。可复计。
    def 一般高g(self, g: dict):
        group = copy.deepcopy(g)
        count = 0
        for suit in group:
            melds = group[suit]
            if not melds:
                continue
            melds_unique = []
            for x in melds:
                if not MjMath.is_123(x):
                    continue
                if x not in melds_unique:
                    melds_unique.append(x)
            for meld in melds_unique:
                if melds.count(meld) > 1:
                    count += 1

        if count == 0:
            return False
        return ('一般高', count, [])

    # 68、断幺：和牌中没有序数牌1、9及字牌。不计无字。
    def 断幺(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        for x in arr:
            test = x % 100
            if test not in range(2, 8 + 1):
                return False
        return ('断幺', 2, ['无字'])

    # 67、暗杠：4张相同的牌都是自己所摸，开杠即为暗杠。
    def 暗杠(self):
        if not self.exposed:
            return False
        count = 0
        for expose in self.exposed:
            if expose.expose_type in ['concealed kong']:
                count += 1
        if not count:
            return False
        return ('暗杠', count * 2, [])

    # 66、双暗刻：两个暗刻（暗杠）。
    def 双暗刻g(self, g):
        group = copy.deepcopy(g)
        count = 0
        for suit in group:
            melds = group[suit]
            if not melds:
                continue
            for meld in melds:
                if MjMath.is_111(meld) or MjMath.is_1111(meld):
                    count += 1

        if self.exposed:
            for expose in self.exposed:
                if expose.expose_type in ['exposed kong', 'exposed pong', ['exposed kong on exposed pong']]:
                    count -= 1
        if count < 2:
            return False
        return ('双暗刻', 2, [])

    # 65、双同刻：两种花色序数相同的两副刻子。可复计。
    def 双同刻g(self, g: dict):
        group = copy.deepcopy(g)
        all = {100, 200, 300}
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        if not group:
            return False

        if len(group) < 2:
            return False

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) < 3:
                    group[suit].remove(meld)
                    continue
                elif MjMath.is_123(meld):
                    group[suit].remove(meld)
                    continue

        if not group:
            return False

        mins = dict()
        # test by meld's min number
        for suit in group:
            melds = group[suit]
            mins[suit] = []
            for meld in melds:
                mins[suit].append(min(meld))

        for x in all:
            if x not in mins:
                mins[x] = []

        count = 0
        for suit in mins:
            tests = mins[suit]
            for test in tests:
                others = copy.deepcopy(all)
                others.remove(suit)
                arr = list(others)
                suit_b = arr[0]
                suit_c = arr[1]
                if (test) in mins[suit_b] or (test) in mins[suit_c]:
                    count += 1
        if not count:
            return False
        return ('双同刻', count, [])

    # 64、四归一：四张相同且未开杠的牌。可复计。
    def 四归一(self):
        arr = Rule.convert_tiles_to_arr(self.concealed)
        uniq = list(set(arr))
        count = 0
        for x in uniq:
            if arr.count(x) >= 4:
                count += 1
        if not count:
            return False
        return ('四归一', count * 2, [])

    # 63、平和：四副顺子、一对序数牌做将的基本和牌型。不计无字。
    def 平和g(self, g: dict):
        group = copy.deepcopy(g)
        for suit in group:
            melds = group[suit]
            for meld in melds:
                if len(meld) == 2:
                    # eyes should be [1..9]
                    if meld[0] not in range(1, 9 + 1):
                        return False
                    continue
                if not MjMath.is_123(meld):
                    return False
        return ('平和', 2, ['无字'])

    # 62、门前清：基本和牌型没有吃、碰、明杠，和他家打出的牌。
    def 门前清(self):
        if self.by_self:
            return False

        if not self.exposed:
            return ('门前清', 2, [])

        for expose in self.exposed:
            if expose.expose_type not in ['concealed kong']:
                return False
        return ('门前清', 2, [])

    # 61、门风刻：与自家本局门风相同的风牌刻子（杠），计2番。这副刻子不计幺九刻。
    def 门风刻(self):
        winner_position_key = -1
        if self.winner_position:
            winner_position_key = Suit.Suit['风']['base'] + Suit.Wind[self.winner_position]['value']
        arr = self.convert_tiles_to_arr(with_exposed=True)
        if arr.count(winner_position_key) >= 3:
            return ('门风刻', 2, [])
        return False

    # 60、圈风刻：与圈风相同的风牌刻子（杠）。这副刻子不计幺九刻。
    def 圈风刻(self):
        prevailing_wind_key = -1
        if self.prevailing_wind:
            prevailing_wind_key = Suit.Suit['风']['base'] + Suit.Wind[self.prevailing_wind]['value']
        arr = self.convert_tiles_to_arr(with_exposed=True)
        if arr.count(prevailing_wind_key) >= 3:
            return ('圈风刻', 2, [])
        return False

    # 59、箭刻：箭牌中、发、白的刻子（杠）。这副刻子不计幺九刻。
    def 箭刻(self):
        base = Suit.Suit['字']['base']
        targets = []
        for wind in Suit.Wind:
            key = base + Suit.Wind[wind]['value']
            targets.append(key)
        arr = self.convert_tiles_to_arr(with_exposed=True)
        count = 0
        for key in targets:
            if arr.count(key) >= 3:
                count += 1
        if count:
            return ('箭刻', count * 2, [])
        return False

    # 58、和绝张：牌池、桌面已亮明的3张牌，和所剩的最后一张牌。
    def 和绝张(self):
        if not self.left:
            return False
        if not self.concealed:
            return False
        test = self.concealed[:]
        tile = test.pop()
        test_key = tile.key
        arr = Rule.convert_tiles_to_arr(self.left)
        if test_key not in arr:
            return ('和绝张', 4, [])

    # 57、双明杠：2个明杠。
    def 双明杠(self):
        if not self.exposed:
            return False
        count = 0
        for expose in self.exposed:
            if expose.expose_type in ['exposed kong', 'exposed kong from exposed pong']:
                count += 1
        if count >= 2:
            return ('双明杠', 4, [])
        return False

    # 56、不求人：基本和牌型没有吃、碰、明杠，自摸和牌。不计自摸。
    def 不求人(self):
        if not self.by_self:
            return False

        if self.exposed:
            count = 0
            for expose in self.exposed:
                if expose.expose_type not in ['concealed kong']:
                    return False
        return ('不求人', 4, ['自摸'])

    # 55、全带幺：每副顺子、刻子、将牌都有幺九牌。
    def 全带幺g(self, group):
        for suit in group:
            melds = group[suit]
            for meld in melds:
                need = {1, 9, 10, 20, 30, 40}
                meld_set = set(meld)
                test = need & meld_set
                if not test:
                    return False
                    # ("meld fail:", meld)
        return ('全带幺', 4, [])

    # 54、双箭刻：和牌中，有箭牌的两副刻子（杠）。不计箭刻，组成双箭刻的两副刻子不计幺九刻。
    def 双箭刻g(self, group):
        count = 0
        for suit in group:
            if suit != 400:
                continue
            melds = group[suit]
            for meld in group[suit][::-1]:
                if len(meld) == 2:
                    group[suit].remove(meld)
            if len(melds) >= 2:
                return ('双箭刻', 6, ['箭刻'])

        return False

    # 53、双暗杠：和牌中，有两副暗杠。
    def 双暗杠(self):
        if not self.exposed:
            return False
        count = 0
        for expose in self.exposed:
            if expose.expose_type == 'concealed kong':
                count += 1
        if count >= 2:
            return ('双暗杠', 6, [])
        return False

    # 52、全求人：吃、碰、明杠四次，和他家打出的牌。不计单钓将。
    def 全求人(self):
        if len(self.concealed) > 2:
            return False
        for expose in self.exposed:
            if expose.expose_type == 'concealed kong':
                return False
        return ('全求人', 6, ['单钓'])

    # 51、五门齐：和牌中条、饼、万、风牌、箭牌齐全。
    def 五门齐g(self, group):
        suits = [suit for suit in group]
        if len(suits) >= 5:
            return ('五门齐', 6, [])
        return False

    # 50、三色三步高：三种花色序数依次递增1的三副顺子。
    def 三色三步高g(self, g: dict):
        group = copy.deepcopy(g)
        all = {100, 200, 300}
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        if not group:
            return False

        if len(group) < 3:
            return False

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) != 3:
                    group[suit].remove(meld)
                    continue
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                    continue
                else:
                    group[suit].sort()

        if not group:
            return False

        mins = dict()
        # test by meld's min number
        for suit in group:
            melds = group[suit]
            mins[suit] = []
            for meld in melds:
                mins[suit].append(min(meld))

        for suit in mins:
            tests = mins[suit]
            for test in tests:
                others = copy.deepcopy(all)
                others.remove(suit)
                arr = list(others)
                suit_b = arr[0]
                suit_c = arr[1]
                if (test + 1) in mins[suit_b] and (test + 2) in mins[suit_c]:
                    # (test + 1, suit_b, test + 2, suit_c)
                    return ('三色三步高', 6, [])
                if (test + 1) in mins[suit_c] and (test + 2) in mins[suit_b]:
                    # (test + 1, suit_c, test + 2, suit_b)
                    return ('三色三步高', 6, [])

        return False

    # 49、混一色：由一种花色的序数牌及字牌组成的和牌。
    def 混一色g(self, g):
        need_one = {100, 200, 300}
        need_any = {400, 500}

        arr = [suit for suit in g]
        suits = set(arr)
        test_one = suits & need_one
        if len(test_one) != 1:
            return False
        test_any = suits & need_any
        if len(test_any) == 0:
            return False
        return ('混一色', 6, [])

    # 48、碰碰和：由四副刻子（杠）、将牌组成的和牌。
    def 碰碰和g(self, g):
        for suit in g:
            for meld in g[suit]:
                if len(meld) == 2:
                    continue
                if not MjMath.is_111(meld) and not MjMath.is_1111(meld):
                    return False
        return ('碰碰和', 6, [])

    # 47、抢杠和：和他家明刻加杠的那张牌。不计和绝张
    def 抢杠和(self):
        if self.robbing_a_kong:
            return ('抢杠和', 8, ['和绝张'])
        return False

    # 46、杠上开花：和开杠后摸进的那张牌。不计自摸，杠来花牌再补花成和，不计杠上开花。
    def 杠上开花(self):
        if self.mahjong_on_kong:
            return ('杠上开花', 8, ['自摸'])
        return False

    # 45、海底捞月：牌墙已摸完，和本局打出的最后一张牌。
    def 海底捞月(self):
        if self.left:
            return False
        if self.by_self:
            return False
        return ('海底捞月', 8, [])

    # 44、妙手回春：摸牌墙上最后一张牌成自摸和。不计自摸。
    def 妙手回春(self):
        if self.left:
            return False
        if not self.by_self:
            return False
        return ('妙手回春', 8, [])

    # 42、三色三节高：三种花色序数依次递增1的三副刻子（杠）。
    def 三色三节高g(self, g: dict):
        group = copy.deepcopy(g)
        all = {100, 200, 300}
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        if not group:
            return False

        if len(group) < 3:
            return False

        # don't need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) != 3:
                    group[suit].remove(meld)
                    continue
                elif MjMath.is_123(meld):
                    group[suit].remove(meld)
                    continue

        if not group:
            return False

        mins = dict()
        # test by meld's min number
        for suit in group:
            melds = group[suit]
            mins[suit] = []
            for meld in melds:
                mins[suit].append(min(meld))

        for suit in mins:
            tests = mins[suit]
            for test in tests:
                others = copy.deepcopy(all)
                others.remove(suit)
                arr = list(others)
                suit_b = arr[0]
                suit_c = arr[1]
                if (test + 1) in mins[suit_b] and (test + 2) in mins[suit_c]:
                    # (test + 1, suit_b, test + 2, suit_c)
                    return ('三色三节高', 8, [])
                if (test + 1) in mins[suit_c] and (test + 2) in mins[suit_b]:
                    # (test + 1, suit_c, test + 2, suit_b)
                    return ('三色三节高', 8, [])

        return False

    # 41、三色三同顺：三种花色序数相同的三副顺子。不计喜相逢。
    def 三色三同顺g(self, g: dict):
        group = copy.deepcopy(g)
        all = {100, 200, 300}
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        if not group:
            return False

        if len(group) < 3:
            return False

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) != 3:
                    group[suit].remove(meld)
                    continue
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                    continue
                else:
                    group[suit].sort()

        if not group:
            return False

        mins = dict()
        # test by meld's min number
        for suit in group:
            melds = group[suit]
            mins[suit] = []
            for meld in melds:
                mins[suit].append(min(meld))

        for suit in mins:
            tests = mins[suit]
            for test in tests:
                others = copy.deepcopy(all)
                others.remove(suit)
                arr = list(others)
                suit_b = arr[0]
                suit_c = arr[1]
                if (test) in mins[suit_b] and (test) in mins[suit_c]:
                    return ('三色三同顺', 8, ['喜相逢'])

        return False

    # 40、推不倒：由牌面图形没有上下区别的牌组成的和牌。这些牌包括1234589饼、245689条、白板。不计缺一门。
    def 推不倒(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        test = set(arr)
        allowed = {201, 202, 203, 204, 205, 208, 209,
                   302, 304, 305, 306, 308, 309,
                   430, }
        remain = test - allowed
        if remain:
            return False
        return ('推不倒', 8, ['缺一门'])

    # 39、花龙：一种花色的123、另一种花色的456、第三种花色的789三副顺子。
    def 花龙g(self, g: dict):
        group = copy.deepcopy(g)
        all = {100, 200, 300}
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        if not group:
            return False

        if len(group) < 3:
            return False

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) != 3:
                    group[suit].remove(meld)
                    continue
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                    continue
                else:
                    group[suit].sort()

        if not group:
            return False

        mins = dict()
        # test by meld's min number
        for suit in group:
            melds = group[suit]
            mins[suit] = []
            for meld in melds:
                mins[suit].append(min(meld))

        for suit in mins:
            tests = mins[suit]
            for test in tests:
                others = copy.deepcopy(all)
                others.remove(suit)
                arr = list(others)
                suit_b = arr[0]
                suit_c = arr[1]
                if (test + 3) in mins[suit_b] and (test + 6) in mins[suit_c]:
                    return ('花龙', 8, [])
                if (test + 3) in mins[suit_c] and (test + 6) in mins[suit_b]:
                    return ('花龙', 8, [])

        return False

    # 38、三风刻：和牌中，有三副风刻（杠）。组成三风刻的三副刻子不计幺九刻。
    def 三风刻(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        arr_set = set(arr)
        need = {510, 520, 530, 540, }
        test = arr_set & need
        if len(test) == 3:
            return ('三风刻', 12, ['幺九刻'])
        return False

    # 37、小于五：由序数牌1234组成的和牌。不计无字。
    def 小于五(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        arr = list(set(arr))
        for x in arr:
            if x % 100 >= 5:
                return False
        return ('小于五', 12, ['无字'])

    # 36、大于五：由序数牌6789组成的和牌。不计无字。
    def 大于五(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        arr = list(set(arr))
        for x in arr:
            if x % 100 <= 5:
                return False
            if x % 100 >= 10:
                return False
        return ('大于五', 12, ['无字'])

    # 35、组合龙：一种花色的147、另一种花色的258、第三种花色的369（可视为三副特殊顺子）。
    def 组合龙(self):
        tiles = self.concealed[:]
        if self.exposed:
            for expose in self.exposed:
                if expose.expose_type in ['exposed chow']:
                    tiles += expose.all

        arr = Rule.convert_tiles_to_arr(tiles)
        test = MjMath.is_组合龙(arr)
        if test:
            return ('组合龙', 12, [])
        return False

    # 34、全不靠：由一种花色的147、另一种花色的258、第三种花色的369
    # 及东、南、西、北、中、发、白中的任何14张单张牌组成的特殊和牌型。
    # 不计五门齐、不求人、门前清。
    def 全不靠(self):
        arr = self.convert_tiles_to_arr(with_exposed=False)
        test = MjMath.is_全不靠(arr)
        if test:
            return ('全不靠', 12, ['五门齐', '不求人', '门前清'])
        return False

    # 33、三暗刻：三副暗刻（暗杠）
    def 三暗刻g(self, g):
        group = copy.deepcopy(g)
        count = 0
        for suit in group:
            melds = group[suit]
            if not melds:
                continue
            for meld in melds:
                if MjMath.is_111(meld) or MjMath.is_1111(meld):
                    count += 1

        if self.exposed:
            for expose in self.exposed:
                if expose.expose_type in ['exposed kong', 'exposed pong']:
                    count -= 1
        if count < 3:
            return False
        return ('三暗刻', 16, ['双暗刻'])

    # 32、三同刻：三种花色序数相同的三副刻子（杠）。不计双同刻。
    def 三同刻g(self, g: dict):
        group = copy.deepcopy(g)
        all = {100, 200, 300}
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        if not group:
            return False

        if len(group) < 3:
            return False

        # don't need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) < 3:
                    group[suit].remove(meld)
                    continue
                elif MjMath.is_123(meld):
                    group[suit].remove(meld)
                    continue

        if not group:
            return False

        mins = dict()
        # test by meld's min number
        for suit in group:
            melds = group[suit]
            mins[suit] = []
            for meld in melds:
                mins[suit].append(min(meld))

        for suit in mins:
            tests = mins[suit]
            for test in tests:
                others = copy.deepcopy(all)
                others.remove(suit)
                arr = list(others)
                suit_b = arr[0]
                suit_c = arr[1]
                if (test) in mins[suit_b] and (test) in mins[suit_c]:
                    return ('三同刻', 16, ['双同刻'])
        return False

    # 31、全带五：每副顺子、刻子、将牌都有序数牌5，计16番。不计断幺、无字。
    def 全带五g(self, g: dict):
        need = 5
        group = copy.deepcopy(g)
        for suit in group:
            for meld in group[suit]:
                if need not in meld:
                    return False
        return ('全带五', 16, ['断幺', '无字'])

    # 30、一色三步高：同一种花色序数依次递增1或2的三副顺子。
    def 一色三步高g(self, g: dict):
        group = copy.deepcopy(g)
        all = {100, 200, 300}
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) < 3:
                    group[suit].remove(meld)
                    continue
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                    continue
                else:
                    meld.sort()

        for suit in all:
            if suit in group:
                if len(group[suit]) < 3:
                    group.pop(suit)

        if not group:
            return False
        for suit in group:
            min = 10
            for meld in group[suit]:
                if min > meld[0]:
                    min = meld[0]
            base = min - 1
            for meld in group[suit]:
                meld[0] -= base
                meld[1] -= base
                meld[2] -= base

        for suit in group:
            test = group[suit]
            if [1, 2, 3] in test and [2, 3, 4] in test and [3, 4, 5] in test:
                return ('一色三步高', 16, [])
            if [1, 2, 3] in test and [3, 4, 5] in test and [5, 6, 7] in test:
                return ('一色三步高', 16, [])

        return False

    # 29、三色双龙会：一种花色的123、789，另一种花色的123、789，第三种花色5做将牌的基本和牌型。
    # 不计 平和、老少副、喜相逢、无字。
    def 三色双龙会g(self, g: dict):
        group = copy.deepcopy(g)
        all = [100, 200, 300]
        removes = {400, 500}
        need = ([1, 2, 3], [7, 8, 9])

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # only need 123 meld
        # record eyes suit
        eyes_suit = 0
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) == 2:
                    if meld[0] != 5:
                        return False
                    eyes_suit = suit
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                else:
                    meld.sort()

        if len(group) < 3:
            return False
        if not eyes_suit:
            return False
        all.remove(eyes_suit)
        suit_a = all[0]
        suit_b = all[1]
        if need[0] in group[suit_a] and need[1] in group[suit_a] \
                and need[0] in group[suit_b] and need[1] in group[suit_b]:
            return ('三色双龙会', 16, ["平和", "老少副", "喜相逢", "无字"])

        return False

    # 28、清龙：同一种花色的123、456、789三副顺子。不计连六、老少副。
    def 清龙g(self, g: dict):
        group = copy.deepcopy(g)
        removes = {400, 500}
        need = ([1, 2, 3], [4, 5, 6], [7, 8, 9])

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) == 2:
                    group[suit].remove(meld)
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                else:
                    meld.sort()

        for suit in group:
            test = group[suit]
            if need[0] in test and need[1] in test and need[2] in test:
                return ('清龙', 16, ["连六", "老少副"])
        return False

    # 27、全小：由序数牌123组成的和牌。不计小于五、无字。
    def 全小(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        arr = list(set(arr))
        for x in arr:
            value = x % 100
            if value not in (1, 2, 3):
                return False
        return ('全小', 24, ['小于五', '无字'])

    # 26、全中：由序数牌456组成的和牌。不计断幺。
    def 全中(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        arr = list(set(arr))
        for x in arr:
            value = x % 100
            if value not in (4, 5, 6):
                return False
        return ('全中', 24, ['断幺'])

    # 25、全大：由序数牌789组成的和牌。不计大于五、无字。
    def 全大(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        arr = list(set(arr))
        for x in arr:
            value = x % 100
            if value not in (7, 8, 9):
                return False
        return ('全大', 24, ['大于五', '无字'])

    # 24、一色三节高：同一种花色三副序数依次递增1的刻子（杠）。不计一色三同顺。
    def 一色三节高g(self, g: dict):
        group = copy.deepcopy(g)
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # don't need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) == 2:
                    group[suit].remove(meld)
                elif MjMath.is_123(meld):
                    group[suit].remove(meld)

        values = dict()
        for suit in group:
            if suit not in values:
                values[suit] = []
            for meld in group[suit]:
                value = meld[0]
                values[suit].append(value)

        for suit in values:
            test = values[suit]
            for value in test:
                if (value + 1) in test and (value + 2) in test:
                    return ('一色三节高', 24, ['一色三同顺'])

        return False

    # 23、一色三同顺：同一种花色三副相同的顺子。不计一色三节高、一般高。
    def 一色三同顺g(self, g: dict):
        group = copy.deepcopy(g)
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) == 2:
                    group[suit].remove(meld)
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                else:
                    meld.sort()

        for suit in group:
            test = group[suit]
            for meld in test:
                if test.count(meld) >= 3:
                    return ('一色三同顺', 24, ['一色三节高'])

        return False

    # 22、清一色：由一种花色的序数牌组成的和牌。不计无字。
    def 清一色g(self, g: dict):
        group = copy.deepcopy(g)
        if len(group) == 1:
            return ('清一色', 24, ['无字'])
        return False

    # 21、全双刻：由双数序数牌（即2468）的刻子（杠）、将牌组成的基本和型。不计碰碰和、断幺、无字。
    def 全双刻g(self, g: dict):
        group = copy.deepcopy(g)
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # don't need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) == 2:
                    group[suit].remove(meld)
                elif MjMath.is_123(meld):
                    return False

        for suit in group:
            for meld in group[suit]:
                if meld[0] % 2 != 0:
                    return False

        return ('全双刻', 24, ['碰碰和', '断幺', '无字'])

    # 20、七星不靠：东、南、西、北、中、发、白各一张，
    # 加上一种花色的147、另一种花色的258、第三种花色的369中的七张牌组成的没有将牌的特殊和牌型。
    # 不计全不靠、五门齐、不求人、门前清。
    def 七星不靠(self):
        if self.exposed:
            return False
        arr = self.convert_tiles_to_arr(with_exposed=False)
        if MjMath.is_七星不靠(arr):
            return ('七星不靠', 24, ['全不靠', '五门齐', '不求人', '门前清'])
        return False

    # 19、七对：七个对子组成的特殊和牌型。不计不求人、门前清、单钓将。
    def 七对(self):
        if self.exposed:
            return False
        arr = self.convert_tiles_to_arr(with_exposed=True)
        if MjMath.is_七对(arr):
            return ('七对', 24, ['不求人', '门前清', '单钓'])
        return False

    # 18、混幺九：由字牌与序数牌1、9组成的和牌。不计碰碰和、全带幺、幺九刻。
    def 混幺九g(self, g: list):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        allowed = {1, 9, 10, 20, 30, 40, }
        for x in arr:
            value = x % 100
            if value not in allowed:
                return False

        return ('混幺九', 32, ['碰碰和', '全带幺', '幺九刻'])

    # 17、三杠：和牌中，有三副杠牌（暗杠加计）。
    def 三杠(self):
        count = 0
        if not self.exposed:
            return False
        for expose in self.exposed:
            if expose.expose_type in ['concealed kong', 'exposed kong', 'exposed kong on exposed pong']:
                count += 1

        if count >= 3:
            return ('三杠', 32, [])
        return False

    # 16、一色四步高：同一种花色四副依次递增1或2的顺子。不计一色三步高、连六、老少副。
    def 一色四步高g(self, g: dict):
        group = copy.deepcopy(g)
        all = {100, 200, 300}
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) < 3:
                    group[suit].remove(meld)
                    continue
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                    continue
                else:
                    meld.sort()

        for suit in all:
            if suit in group:
                if len(group[suit]) < 4:
                    group.pop(suit)

        if not group:
            return False
        for suit in group:
            min = 10
            for meld in group[suit]:
                if min > meld[0]:
                    min = meld[0]
            base = min - 1
            for meld in group[suit]:
                meld[0] -= base
                meld[1] -= base
                meld[2] -= base

        for suit in group:
            test = group[suit]
            if [1, 2, 3] in test and [2, 3, 4] in test and [3, 4, 5] in test and [4, 5, 6] in test:
                return ('一色四步高', 32, ['一色三步高', '连六', '老少副'])
            if [1, 2, 3] in test and [3, 4, 5] in test and [5, 6, 7] in test and [7, 8, 9] in test:
                return ('一色四步高', 32, ['一色三步高', '连六', '老少副'])

        return False

    # 15、一色四节高：同一种花色四副依次递增1的刻子（杠）。不计一色三同顺、一色三节高、碰碰和
    def 一色四节高g(self, g: dict):
        group = copy.deepcopy(g)
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # don't need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) == 2:
                    group[suit].remove(meld)
                elif MjMath.is_123(meld):
                    group[suit].remove(meld)

        values = dict()
        for suit in group:
            if suit not in values:
                values[suit] = []
            for meld in group[suit]:
                value = meld[0]
                values[suit].append(value)

        for suit in values:
            test = values[suit]
            for value in test:
                if (value + 1) in test and (value + 2) in test and (value + 3) in test:
                    return ('一色四节高', 48, ['一色三同顺', '一色三节高', '碰碰和'])

        return False

    # 14、一色四同顺：同一种花色四副相同顺子。不计一色三同顺、一色三节高、四归一、一般高。
    def 一色四同顺g(self, g: dict):
        group = copy.deepcopy(g)
        removes = {400, 500}

        # don't need winds and chars
        for remove in removes:
            if remove in group:
                group.pop(remove)

        # only need 123 meld
        for suit in group:
            for meld in group[suit][::-1]:
                if len(meld) == 2:
                    group[suit].remove(meld)
                elif not MjMath.is_123(meld):
                    group[suit].remove(meld)
                else:
                    meld.sort()

        for suit in group:
            test = group[suit]
            for meld in test:
                if test.count(meld) >= 4:
                    return ('一色四同顺', 48, ['一色三同顺', '一色三节高', '四归一', '一般高'])

        return False

    # 13、一色双龙会：同一种花色123、789各两副，本花色5做将牌的和牌。
    # 不计七对、清一色、平和、一般高、老少副、无字。
    def 一色双龙会g(self, g: dict):
        group = copy.deepcopy(g)

        for s in group:
            test = group[s]
            if test.count([1, 2, 3]) >= 2 and test.count([7, 8, 9]) >= 2 and test.count([5, 5]) >= 1:
                return ('一色双龙会', 64, ['七对', '清一色', '平和', '一般高', '老少副', '无字'])

        return False

    # 12、四暗刻：和牌中，有四副暗刻（暗杠）。不计碰碰和、不求人、门前清。
    def 四暗刻(self):
        if not self.exposed:
            return False

        count = 0
        for expose in self.exposed:
            if expose.expose_type in ['concealed kong']:
                count += 1

        if count >= 4:
            return ('四暗刻', 64, ['碰碰和', '不求人', '门前清'])

        return False

    # 11、字一色：由字牌组成的和牌。不计碰碰和、全带幺、幺九刻。
    def 字一色g(self, g: list):
        group = copy.deepcopy(g)

        allowed = {400, 500}
        for s in group:
            if s not in allowed:
                return False

        return ('字一色', 64, ['碰碰和', '全带幺', '幺九刻'])

    # 10、小三元：和牌中，有两副箭牌的刻子（杠）、第三种箭牌作将牌。
    # 不计双箭刻、箭刻，组成小三元的两副刻子不计幺九刻。
    def 小三元g(self, g: list):
        group = copy.deepcopy(g)
        allowed = {400}

        has_eyes = False
        count = 0
        for s in group:
            if s not in allowed:
                continue
            for meld in group[s]:
                if len(meld) == 2:
                    has_eyes = True
                    continue
                else:
                    count += 1

        if has_eyes and count >= 2:
            return ('小三元', 64, ['双箭刻', '箭刻'])

        return False

    # 9、小四喜：和牌中，有三副风牌的刻子（杠）、第四种风牌作将牌。不计三风刻、幺九刻。
    def 小四喜g(self, g: list):
        group = copy.deepcopy(g)
        allowed = {500}

        has_eyes = False
        count = 0
        for s in group:
            if s not in allowed:
                continue
            for meld in group[s]:
                if len(meld) == 2:
                    has_eyes = True
                    continue
                else:
                    count += 1

        if has_eyes and count >= 3:
            return ('小四喜', 64, ['三风刻', '幺九刻'])

        return False

    # 8、清幺九：由序数牌1、9组成的和牌。不计碰碰和、全带幺、双同刻、幺九刻、无字。
    def 清幺九g(self, g: list):
        group = copy.deepcopy(g)

        allowed = {1, 9}
        for s in group:
            for meld in group[s]:
                for x in meld:
                    if x not in allowed:
                        return False

        return ('清幺九', 64, ['碰碰和', '全带幺', '双同刻', '幺九刻', '无字'])

    # 7、十三幺：由三种序数牌的1、9牌，七种字牌及其中一对作将牌组成的特殊和牌。不计五门齐、不求人、门前清、单钓将。
    def 十三幺(self):
        if self.exposed:
            return False
        arr = self.convert_tiles_to_arr(with_exposed=False)
        test = MjMath.is_十三幺(arr)
        if test:
            return ('十三幺', 64, ['五门齐', '不求人', '门前清', '单钓'])
        return False

    # 6、连七对：由一种花色序数相连的七个对子组成的和牌。不计清一色、七对、不求人、门前清、无字、单钓将。
    def 连七对(self):
        if self.exposed:
            return False
        arr = self.convert_tiles_to_arr(with_exposed=False)
        if not MjMath.is_七对(arr):
            return False

        suits = []
        values = []
        for x in arr:
            value = x % 100
            suit = x - value
            if suit not in (100, 200, 300):
                return False
            suits.append(suit)
            values.append(value)
        suits = list(set(suits))
        if len(suits) != 1:
            return False
        values = list(set(values))
        if len(values) != 7:
            return False
        if min(values) + 6 != max(values):
            return False

        return ('连七对', 88, ['清一色', '七对', '不求人', '门前清', '无字', '单钓'])

    # 5、四杠：和牌中，有四副杠牌。不计碰碰和、单钓将。
    def 四杠(self):
        if not self.exposed:
            return False
        count = 0
        for expose in self.exposed:
            if expose.expose_type in ['concealed kong', 'exposed kong', 'exposed kong on exposed pong']:
                count += 1
        if count >= 4:
            return ('四杠', 88, ['碰碰和', '单钓'])
        return False

    # 4、九莲宝灯：立牌为同一种花色的1112345678999，见本花色任何1张牌成和。不计清一色、不求人、门前清、无字、幺九刻×1。
    def 九莲宝灯(self):
        arr = self.convert_tiles_to_arr(with_exposed=False)
        if not MjMath.is_good_concealed(arr):
            return False

        arr.pop()
        if len(arr) != 13:
            return False

        suits = set()
        values = []
        for x in arr:
            value = x % 100
            suit = x - value
            if suit not in suits:
                suits.add(suit)
            values.append(value)
        if len(suits) > 1:
            return False
        values.sort()
        if values == [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9]:
            return ('九莲宝灯', 88, ['清一色', '不求人', '门前清', '无字', '幺九刻'])
        return False

    # 3、绿一色：由“23468条”及“发”之中的任何牌组成的和牌。不计混一色。如无“发”，可计清一色。
    def 绿一色(self):
        arr = self.convert_tiles_to_arr(with_exposed=True)
        allowed = [302, 303, 304, 306, 308, 420]
        for x in arr:
            if x not in allowed:
                return False
        return ('绿一色', 88, ['混一色'])

    # 2、大三元：和牌中，有中、发、白三副刻子（杠）。不计双箭刻、箭刻，组成大三元的三副刻子不计幺九刻。
    def 大三元g(self, g: list):
        group = copy.deepcopy(g)
        allowed = {400}
        for s in group:
            if s not in allowed:
                continue
            for meld in group[s][::-1]:
                if len(meld) == 2:
                    group[s].remove(meld)
            if len(group[s]) >= 3:
                return ('大三元', 88, ['双箭刻', '箭刻'])
        return False

    # 1、大四喜：和牌中，有东、南、西、北四副刻子（杠）。不计三风刻、碰碰和、圈风刻、门风刻、幺九刻。
    def 大四喜g(self, g: list):
        group = copy.deepcopy(g)
        allowed = {500}
        for s in group:
            if s not in allowed:
                continue
            for meld in group[s][::-1]:
                if len(meld) == 2:
                    group[s].remove(meld)
            if len(group[s]) >= 4:
                return ('大四喜', 88, ['三风刻', '碰碰和', '圈风刻', '门风刻', '幺九刻'])
        return False


def test_calc():
    MjSet.generate_dictionary()
    flowers = []

    arr = [105, 106, 108, 109, 201, 202, 302, 307, 410, 420, 520, 530, 540, 420]
    concealed = Rule.convert_arr_to_tiles(arr)

    # arr = [201, 202, 203, ]
    # inners = Rule.convert_arr_to_tiles(arr)
    # expose1 = Expose(inners=inners, expose_type='exposed chow')
    # arr = [102, 103, 104, ]
    # inners = Rule.convert_arr_to_tiles(arr)
    # expose2 = Expose(inners=inners, expose_type='exposed chow')
    # arr = [203, 204, 205, ]
    # inners = Rule.convert_arr_to_tiles(arr)
    # expose3 = Expose(inners=inners, expose_type='exposed chow')
    # calc = Calc(flowers=flowers, by_self=False, concealed=concealed, exposed=[expose1, expose2, expose3])
    calc = Calc(flowers=flowers, by_self=False, concealed=concealed, exposed=[])
    # test = calc.calc()
    test = calc.三风刻()
    print("test:", test)


def main():
    test_calc()
    pass


if __name__ == '__main__':
    main()
