#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from builtins import zip
from builtins import range
import unittest
from ..roulette import board as bd
from ..roulette import players as ply
from ..roulette import bin_builder as bb


class test_Outcome_Class(unittest.TestCase):

    def setUp(self):
        self.outcome1 = bd.Outcome('name1', 8)
        self.outcome2 = bd.Outcome('name1', 8)
        self.outcome3 = bd.Outcome('name2', 9)

    def test_comparisons(self):
        self.assertEqual(self.outcome1, self.outcome2)
        self.assertNotEqual(self.outcome2, self.outcome3)

    def test_hash(self):
        self.assertTrue(hash(self.outcome1) == hash(self.outcome2))
        self.assertFalse(hash(self.outcome2) == hash(self.outcome3))

    def test_winAmount(self):
        self.assertEqual(self.outcome1.winAmount(5), 40)

    def tearDown(self):
        del self.outcome1
        del self.outcome2
        del self.outcome3


class test_Bin(unittest.TestCase):

    def test_Bin_init(self):
        five = bd.Outcome("00-0-1-2-3", 6)
        outcome1 = bd.Outcome("00-0-1-2-3", 6)
        outcome2 = bd.Outcome("0", 35)
        outcome3 = bd.Outcome("00", 35)
        zero = bd.Bin([outcome2, five])
        zerozero = bd.Bin([outcome2, five])
        bin1 = bd.Bin({outcome1, outcome2, outcome3})
        self.assertIsInstance(zero, bd.Bin)
        self.assertIsInstance(zerozero, bd.Bin)
        self.assertIsInstance(bin1, bd.Bin)


class test_Wheel(unittest.TestCase):

    def setUp(self):
        self.wheel = bd.Wheel()

    def test_rng_internal(self):
        first_ten = [8, 36, 4, 16, 7, 31, 28, 30, 24, 13]
        self.wheel.rng.seed(1)  # fixed seed
        self.assertEqual([self.wheel.rng.randint(0, 37)
                          for _ in range(10)], first_ten)

    def test_getOutcome(self):
        """results depends on successful binBuilder"""
        bb.BinBuilder.buildBins(self.wheel)
        outcome_quantity = {'straight': 38,
                            'split': 57,
                            'street': 12,
                            'corner': 22,
                            '00-0-1-2-3': 1,
                            'line': 6,
                            'dozen': 3,
                            'column': 3,
                            'red': 1,
                            'black': 1,
                            'odd': 1,
                            'even': 1,
                            'high': 1,
                            'low': 1}
        for name, uniq_num in list(outcome_quantity.items()):
            self.assertEqual(len(self.wheel.getOutcome(name)), uniq_num)

    def tearDown(self):
        del self.wheel


class test_BinBuilder(unittest.TestCase):

    def setUp(self):
        self.wheel = bd.Wheel()
        self.builder = bb.BinBuilder()

    def _build_helper(self, wheel, bet, bin_nums):
        for bin_num in bin_nums:
            getattr(self.builder, bet)(wheel, bin_num)

    def test_straight_bet(self):
        bin_nums = (0, 1, 15, 30, 37)
        bet = "_straight_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        for bin_num in bin_nums:
            if bin_num != 37:
                self.assertIn(
                    bd.Outcome(
                        'Straight %d' %
                        bin_num,
                        35),
                    self.wheel[bin_num])
            else:
                self.assertIn(
                    bd.Outcome(
                        'Straight 00',
                        35),
                    self.wheel[bin_num])

    def test_street_bet(self):
        bin_nums = (0, 1, 15, 29, 37)
        bet = "_street_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Street 1-2-3', 11)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {bd.Outcome('Street 13-14-15', 11)}
        self.assertTrue(self.wheel[15] == ans)
        ans = {bd.Outcome('Street 28-29-30', 11)}
        self.assertTrue(self.wheel[29] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_split_bet(self):
        bin_nums = (0, 1, 15, 29, 37)
        bet = "_split_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Split 1-2', 17), bd.Outcome('Split 1-4', 17)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {
            bd.Outcome('Split 12-15', 17),
            bd.Outcome('Split 14-15', 17),
            bd.Outcome('Split 15-18', 17)
        }
        self.assertTrue(self.wheel[15] == ans)
        ans = {
            bd.Outcome('Split 26-29', 17),
            bd.Outcome('Split 28-29', 17),
            bd.Outcome('Split 29-30', 17),
            bd.Outcome('Split 29-32', 17)
        }
        self.assertTrue(self.wheel[29] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_corner_bet(self):
        bin_nums = (0, 1, 15, 29, 37)
        bet = "_corner_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Corner 1-2-4-5', 8)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {
            bd.Outcome(
                'Corner 11-12-14-15',
                8),
            bd.Outcome(
                'Corner 14-15-17-18',
                8)}
        self.assertTrue(self.wheel[15] == ans)
        ans = {
            bd.Outcome('Corner 25-26-28-29', 8),
            bd.Outcome('Corner 28-29-31-32', 8),
            bd.Outcome('Corner 26-27-29-30', 8),
            bd.Outcome('Corner 29-30-32-33', 8)
        }
        self.assertTrue(self.wheel[29] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_line_bet(self):
        bin_nums = (0, 1, 15, 29, 37)
        bet = "_line_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Line 1-2-3-4-5-6', 5)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {bd.Outcome('Line 13-14-15-16-17-18', 5)}
        self.assertTrue(self.wheel[15] == ans)
        ans = {bd.Outcome('Line 25-26-27-28-29-30', 5)}
        self.assertTrue(self.wheel[29] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_dozen_bet(self):
        bin_nums = (0, 1, 15, 29, 37)
        bet = "_dozen_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Dozen 12', 2)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {bd.Outcome('Dozen 24', 2)}
        self.assertTrue(self.wheel[15] == ans)
        ans = {bd.Outcome('Dozen 36', 2)}
        self.assertTrue(self.wheel[29] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_column_bet(self):
        bin_nums = (0, 1, 15, 29, 37)
        bet = "_column_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Column 1', 2)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {bd.Outcome('Column 3', 2)}
        self.assertTrue(self.wheel[15] == ans)
        ans = {bd.Outcome('Column 2', 2)}
        self.assertTrue(self.wheel[29] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_color_bet(self):
        bin_nums = (0, 1, 15, 29, 37)
        bet = "_color_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Red', 1)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {bd.Outcome('Black', 1)}
        self.assertTrue(self.wheel[15] == ans)
        ans = {bd.Outcome('Black', 1)}
        self.assertTrue(self.wheel[29] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_evenness_bet(self):
        bin_nums = (0, 1, 15, 16, 30, 37)
        bet = "_evenness_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Odd', 1)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {bd.Outcome('Odd', 1)}
        self.assertTrue(self.wheel[15] == ans)
        ans = {bd.Outcome('Even', 1)}
        self.assertTrue(self.wheel[16] == ans)
        ans = {bd.Outcome('Even', 1)}
        self.assertTrue(self.wheel[30] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_hight_bet(self):
        bin_nums = (0, 1, 15, 29, 37)
        bet = "_hight_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        self.assertEqual(len(self.wheel[0]), 0)
        ans = {bd.Outcome('Low', 1)}
        self.assertTrue(self.wheel[1] == ans)
        ans = {bd.Outcome('Low', 1)}
        self.assertTrue(self.wheel[15] == ans)
        ans = {bd.Outcome('High', 1)}
        self.assertTrue(self.wheel[29] == ans)
        self.assertEqual(len(self.wheel[37]), 0)

    def test_five_bet(self):
        bin_nums = (0, 1, 15, 16, 30, 37)
        bet = "_five_bet"
        self._build_helper(self.wheel, bet, bin_nums)
        ans = {bd.Outcome('00-0-1-2-3', 6)}
        self.assertTrue(self.wheel[0] == ans)
        self.assertTrue(self.wheel[1] == ans)
        self.assertTrue(self.wheel[37] == ans)
        self.assertEqual(len(self.wheel[15]), 0)
        self.assertEqual(len(self.wheel[30]), 0)

    def tearDown(self):
        del self.wheel


class test_Bet(unittest.TestCase):

    def setUp(self):
        self.bet1 = bd.Bet(5, bd.Outcome('reddish', 8))
        self.bet2 = bd.Bet(10.6, bd.Outcome('80-90', 9))

    def test_winAmount(self):
        self.assertEqual(self.bet1.winAmount(), 45)
        self.assertAlmostEqual(self.bet2.winAmount(), 106, places=3)

    def test_loseAmount(self):
        self.assertEqual(self.bet1.loseAmount(), 5)
        self.assertEqual(self.bet2.loseAmount(), 10.6)

    def test_add(self):
        self.assertEqual(self.bet1 + self.bet2, 15.6)

    def tearDown(self):
        del self.bet1, self.bet2


class test_Table(unittest.TestCase):

    def setUp(self):
        self.bets = [
            bd.Bet(
                5, bd.Outcome(
                    'reddish', 8)), bd.Bet(
                10.6, bd.Outcome(
                    '80-90', 9))]
        self.table = bd.Table(200, 5, self.bets)

    def test_iter(self):
        for table_bet, bet in zip(self.table, self.bets):
            self.assertEqual(table_bet, bet)

    def test_isValid(self):
        self.table.placeBet(bd.Bet(100, bd.Outcome('foo', 10)))
        with self.assertRaises(bd.InvalidBet):
            self.table.placeBet(
                bd.Bet(
                    self.table.limit + 1,
                    bd.Outcome(
                        'bar',
                        5)))

    def test_clear(self):
        self.table.clear()
        self.assertFalse(self.table.bets)

    def tearDown(self):
        del self.bets, self.table


class test_Game(unittest.TestCase):

    def setUp(self):
        self.wheel = bd.Wheel()
        bb.BinBuilder.buildBins(self.wheel)
        self.wheel.rng.seed(1)  # fixed seed
        # assuming test_rng_internal passed, self.wheel lands on 8, 36, 4, then
        # 16.
        self.table = bd.Table(200, 5)
        self.game = ply.Game(self.table, self.wheel)
        self.player = ply.Passenger57(self.table, self.wheel)

    def tearDown(self):
        del self.game, self.player

    def test_game_cycle(self):
        for _ in range(10):
            self.game.cycle(self.player)

    def test_Passenger57(self):
        """integration test for :class:`Passenger57`"""
        self.player = ply.Passenger57(self.table, self.wheel)
        # assuming initial stake is 250 and bet amount is 10.
        expected_stake = [1010, 1000, 1010, 1000]
        for i in range(4):
            self.game.cycle(self.player)
            self.assertEqual(self.player.stake, expected_stake[i])

    def test_Martingale(self):
        """integration test for :class:`Martingale`"""
        self.player = ply.Martingale(self.table, self.wheel)
        # assuming initial stake is 250 and bet amount is 10.
        expected_stake = [1010, 1000, 1020, 1010]
        for i in range(4):
            self.game.cycle(self.player)
            self.assertEqual(self.player.stake, expected_stake[i])


if __name__ == '__main__':
    unittest.main()
