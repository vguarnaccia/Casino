#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import roulette as rl


class Test_Outcome_Class(unittest.TestCase):

    def setUp(self):
        self.outcome1 = rl.Outcome('name1', 8)
        self.outcome2 = rl.Outcome('name1', 8)
        self.outcome3 = rl.Outcome('name2', 9)

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
        five = rl.Outcome("00-0-1-2-3", 6)
        outcome1 = rl.Outcome("00-0-1-2-3", 6)
        outcome2 = rl.Outcome("0", 35)
        outcome3 = rl.Outcome("00", 35)
        zero = rl.Bin([outcome2, five])
        zerozero = rl.Bin([outcome2, five])
        bin1 = rl.Bin({outcome1, outcome2, outcome3})
        self.assertIsInstance(zero, rl.Bin)
        self.assertIsInstance(zerozero, rl.Bin)
        self.assertIsInstance(bin1, rl.Bin)

class test_Wheel(unittest.TestCase):

    def setUp(self):
        self.wheel = rl.Wheel()

    def test_rng_internal(self):
        first_ten = [8, 36, 4, 16, 7, 31, 28, 30, 24, 13]
        self.wheel.rng.seed(1)  # fixed seed
        self.assertEqual([self.wheel.rng.randint(0, 37) for _ in range(10)], first_ten)

    def tearDown(self):
        del self.wheel

class test_binBuilder(unittest.TestCase):

    def setUp(self):
        self.wheel = rl.Wheel()
        binBuilder = rl.BinBuilder()
        binBuilder.buildBins(self.wheel)

    def test_straight_bet(self):
        for bin_num, Bin in enumerate(self.wheel):
            if bin_num != 37:
                self.assertIn(rl.Outcome('Staight %d' % bin_num, 35), Bin)
            else:
                self.assertIn(rl.Outcome('Staight 00', 35), Bin)

    def test_meh_bet(self):
        for bin_num, Bin in enumerate(self.wheel):
            print('{0} {1}'.format(bin_num, len(Bin)))
    # TODO: add builder tests

    def tearDown(self):
        del self.wheel

if __name__ == '__main__':
    unittest.main()
