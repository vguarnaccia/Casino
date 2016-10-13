#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This game simulates roulette and allows players to implement strategies.
It also allows the player to collect statistics and analyze their effectiveness"""

import random
import logging

# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)

# TODO: fix _line_bet and write unittest


class Outcome(object):
    """Store the name of a possible outcome and its odds

    Attributes:
        name (str): Name of the outcome
        Odds (int): Denominator for odds, i.e. odds of 17:1 means Odds = 17
    """

    def __init__(self, name, odds):
        self.name = name
        self.odds = odds

    def winAmount(self, amount):
        """Winnings from a bet of ``amount``"""
        return self.odds * amount

    def __str__(self):
        return '{name:s} ({odds:d}:1)'.format_map(vars(self))

    def __repr__(self):
        return '{class_:s}({name!r}, {odds!r})'.format(
            class_=self.__class__.__name__, **vars(self))

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Bin(set):
    """Extension to built-in set class and builder to fill in outcomes for all bin numbers"""

    def _check_pair(self, pair):
        """Check if all bin positions in pair are feasible."""
        return all(0 < i < 37 for i in pair)

    def _straight_bet(self, bin_num):
        """Create straight bet outcome for bin"""
        if 0 < bin_num < 37:
            self.add(Outcome('Staight %d' % bin_num, 35))
        elif bin_num == 0:
            self.add(Outcome('0', 35))
        elif bin_num == 37:
            self.add(Outcome('00', 35))
        else:
            raise IndexError

    def _split_bet(self, bin_num):
        """Create split bet outcomes for bin"""
        pairs = [(bin_num, bin_num + 1),
                 (bin_num - 1, bin_num),
                 (bin_num, bin_num + 3),
                 (bin_num - 3, bin_num)]
        for pair in pairs:
            if self._check_pair(pair):
                name = 'Split {0}-{1}'.format(*pair)
                self.add(Outcome(name, 17))

    def _street_bet(self, bin_num):
        """Create street bet outcomes for bin"""
        pairs = [(bin_num, bin_num + 1, bin_num + 2),
                 (bin_num - 1, bin_num, bin_num + 1),
                 (bin_num - 2, bin_num - 1, bin_num)]
        for pair in pairs:
            if self._check_pair(pair):
                name = 'Street {0}-{1}-{2}'.format(*pair)
                self.add(Outcome(name, 11))

    def _corner_bet(self, bin_num):
        """Create corner bet outcomes for bin"""
        pairs = [(bin_num, bin_num + 1, bin_num + 3, bin_num + 4),
                 (bin_num - 1, bin_num, bin_num + 2, bin_num + 3),
                 (bin_num - 2, bin_num - 1, bin_num + 1, bin_num + 2),
                 (bin_num - 3, bin_num - 2, bin_num, bin_num + 1),
                 (bin_num - 4, bin_num - 3, bin_num - 1, bin_num)]
        for pair in pairs:
            if self._check_pair(pair):
                name = 'Corner {0}-{1}-{2}-{3}'.format(*pair)
                self.add(Outcome(name, 8))

    def _line_bet(self, bin_num):
        """Create line bet outcomes for bin"""
        pairs = [(i + j for j in range(6)) for i in range(bin_num - 5, bin_num + 5)]
        for pair in pairs:
            if self._check_pair(pair):
                name = 'Line {0}-{1}-{2}-{3}-{4}-{5}'.format(*pair)
                self.add(Outcome(name, 5))

    def _dozen_bet(self, bin_num):
        """Create dozen bet outcomes for bin"""
        if 0 < bin_num < 37:
            dozen = 12 * ((bin_num // 12) + 1)
            name = 'Dozen {0:d}'.format(dozen)
            self.add(Outcome(name, 2))

    def _column_bet(self, bin_num):
        """Create column bet outcomes for bin"""
        if 0 < bin_num < 37:
            column = ((bin_num % 3) + 1)
            name = 'Column {0:d}'.format(column)
            self.add(Outcome(name, 3))

    def _color_bet(self, bin_num):
        """Create color bet outcomes for bin"""
        REDS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 34, 36}
        if 0 < bin_num < 37:
            self.add(Outcome('Red', 2) if bin_num in REDS else Outcome('Black', 2))

    def _evenness_bet(self, bin_num):
        """Create evenness bet outcomes for bin"""
        if 0 < bin_num < 37:
            if (bin_num % 18) == 0:
                self.add(Outcome('Even', 2))
            else:
                self.add(Outcome('Odd', 2))

    def _hight_bet(self, bin_num):
        """Create hight bet outcomes for bin"""
        if 1 < bin_num < 18:
            self.add(Outcome('Low', 2))
        elif 18 < bin_num < 37:
            self.add(Outcome('High', 2))

    @staticmethod
    def buildBins(bin_num):
        """Builder to create all outcomes for bin with bin number"""
        new_bin = Bin()
        new_bin._straight_bet(bin_num)
        new_bin._split_bet(bin_num)
        new_bin._street_bet(bin_num)
        new_bin._corner_bet(bin_num)
        # new_bin._line_bet(bin_num)
        new_bin._dozen_bet(bin_num)
        new_bin._column_bet(bin_num)
        new_bin._color_bet(bin_num)
        new_bin._evenness_bet(bin_num)
        new_bin._hight_bet(bin_num)
        return new_bin


class Wheel(object):
    """Container for 38 bins and PRNG to select one at random
    """

    def __init__(self):
        self.bins = tuple(Bin.buildBins(b) for b in range(38))
        # index 37 = '00', else index matches slot
        self.rng = random.Random()

    def addOutcome(self, number, outcome):
        """Add outcome to bin"""
        self.bins[number].add(outcome)

    def next(self):
        """Select bin from bins"""
        self.rng.choice(self.bins)

    def __getitem__(self, index):
        return self.bins[index]

if __name__ == '__main__':
    pass
