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


class Test_TABLE_Constant(unittest.TestCase):

    def setUp(self):
        self.TABLE = rl.TABLE

    def test_full_TABLE(self):
        assert '00' in self.TABLE, 'missing 00'
        for bet in range(37):
            self.assertIn(str(bet), self.TABLE)

    def test_TABLE_pairs(self):
        """test ensure that TABLE key-value pairs have valid attributes
        Does not test if color is correct.
        """
        for k, v in self.TABLE.items():
            if type(v).__name__ == 'Layout':
                self.assertIn(v.color, ('red', 'black'))
                evenness = 'even' if int(k) % 2 == 0 else 'odd'
                self.assertEqual(evenness, evenness)
                if 0 < int(k) < 13:
                    thirds = 'first 12'
                elif 12 < int(k) < 25:
                    thirds = 'second 12'
                elif 24 < int(k) <= 36:
                    thirds = 'third 12'
                else:
                    thirds = 'oops'
                self.assertEqual(v.third, thirds)
                half = 'low' if 0 < int(k) <= 18 else 'high'
                self.assertTrue(v.half == half and int(k) <= 36)
                if (int(k) % 3) == 1:
                    column = 1
                elif (int(k) % 3) == 2:
                    column = 2
                elif (int(k) % 3) == 0:
                    column = 3
                else:
                    column = 'oops'
                self.assertEqual(v.column, column)
            else:
                self.assertTrue(k == '0' or '00')
                self.assertEqual(v.color, 'green')

    def tearDown(self):
        del self.TABLE


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

if '__name__' == '__main__':
    unittest.main()
