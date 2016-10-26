#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This game simulates roulette and allows players to implement strategies.
It also allows the player to collect statistics and analyze their effectiveness"""

import random
import logging

# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)

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

class BinBuilder(object):
    """builder for adding outcomes to bins in the wheel"""

    def __init__(self):
        pass

    def _check_pair(self, pair):
        """Check if all bin positions in pair are feasible."""
        return all(0 < i < 37 for i in pair)

    def _straight_bet(self, bin_num, wheel):
        """Create straight bet outcome for bin"""
        if bin_num < 37:
            wheel.addOutcome(bin_num, Outcome('Staight %d' % bin_num, 35))
        elif bin_num == 37:
            wheel.addOutcome(bin_num, Outcome('Staight 00', 35))
        else:
            raise IndexError

    def _split_bet(self, bin_num, wheel):
        """Create split bet outcomes for bin"""
        pairs = [(bin_num, bin_num + 1), # left pair
                 (bin_num - 1, bin_num), # right pair
                 (bin_num, bin_num + 3), # up pair
                 (bin_num - 3, bin_num)] # down pair
        for pair in pairs:
            if self._check_pair(pair):
                name = 'Split {0}-{1}'.format(*pair)
                wheel.addOutcome(bin_num, Outcome(name, 17))

    def _street_bet(self, bin_num, wheel):
        """Create street bet outcomes for bin"""
        pairs = [(bin_num, bin_num + 1, bin_num + 2),
                 (bin_num - 1, bin_num, bin_num + 1),
                 (bin_num - 2, bin_num - 1, bin_num)]
        for pair in pairs:
            if self._check_pair(pair):
                name = 'Street {0}-{1}-{2}'.format(*pair)
                wheel.addOutcome(bin_num, Outcome(name, 11))

    def _corner_bet(self, bin_num, wheel):
        """Create corner bet outcomes for bin"""
        pairs = [(bin_num, bin_num + 1, bin_num + 3, bin_num + 4),
                 (bin_num - 1, bin_num, bin_num + 2, bin_num + 3),
                 (bin_num - 2, bin_num - 1, bin_num + 1, bin_num + 2),
                 (bin_num - 3, bin_num - 2, bin_num, bin_num + 1),
                 (bin_num - 4, bin_num - 3, bin_num - 1, bin_num)]
        for pair in pairs:
            if self._check_pair(pair):
                name = 'Corner {0}-{1}-{2}-{3}'.format(*pair)
                wheel.addOutcome(bin_num, Outcome(name, 8))

    def _line_bet(self, bin_num, wheel):
        """Create line bet outcomes for bin"""
        lines = [[i for i in range(j, j + 6)] for j in (1, 7, 13, 19, 25, 31)]
        for line in lines:
            if bin_num in line and self._check_pair(line):
                name = 'Line {0}-{1}-{2}-{3}-{4}-{5}'.format(*line)
                wheel.addOutcome(bin_num, Outcome(name, 5))

    def _dozen_bet(self, bin_num, wheel):
        """Create dozen bet outcomes for bin"""
        if 0 < bin_num < 37:
            dozen = 12 * ((bin_num // 12) + 1)
            name = 'Dozen {0:d}'.format(dozen)
            wheel.addOutcome(bin_num, Outcome(name, 2))

    def _column_bet(self, bin_num, wheel):
        """Create column bet outcomes for bin"""
        if 0 < bin_num < 37:
            column = ((bin_num % 3) + 1)
            name = 'Column {0:d}'.format(column)
            wheel.addOutcome(bin_num, Outcome(name, 3))

    def _color_bet(self, bin_num, wheel):
        """Create color bet outcomes for bin"""
        REDS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 34, 36}
        if 0 < bin_num < 37:
            wheel.addOutcome(bin_num, Outcome('Red', 2) if bin_num in REDS else Outcome('Black', 2))

    def _evenness_bet(self, bin_num, wheel):
        """Create evenness bet outcomes for bin"""
        if 0 < bin_num < 37:
            if (bin_num % 18) == 0:
                wheel.addOutcome(bin_num, Outcome('Even', 2))
            else:
                wheel.addOutcome(bin_num, Outcome('Odd', 2))

    def _hight_bet(self, bin_num, wheel):
        """Create hight bet outcomes for bin"""
        if 1 < bin_num < 18:
            wheel.addOutcome(bin_num, Outcome('Low', 2))
        elif 18 < bin_num < 37:
            wheel.addOutcome(bin_num, Outcome('High', 2))

    def _five_bet(self, bin_num, wheel):
        """Create five bet outcomes for bin"""
        if bin_num in (0, 1, 2, 3, 37):
            wheel.addOutcome(bin_num, Outcome('00-0-1-2-3', 6))

    def buildBins(self, wheel):
        """Builder to create all outcomes for bin with bin number"""
        bets = {'_straight_bet',
                '_split_bet',
                '_street_bet',
                '_corner_bet',
                '_line_bet',
                '_dozen_bet',
                '_column_bet',
                '_color_bet',
                '_evenness_bet',
                '_hight_bet',
                '_five_bet'
                    }
        for bin_num in range(38):
            for bet in bets:
                getattr(self, bet)(bin_num, wheel)

class Wheel(object):
    """Container for 38 bins and PRNG to select one at random"""

    def __init__(self):
        self.bins = [Bin() for _ in range(38)]
        # index 37 = '00', else index matches slot
        self.rng = random.Random()

    def addOutcome(self, number, outcome):
        """Add outcomes to bin"""
        self.bins[number].add(outcome)

    def next(self):
        """Select bin from bins"""
        self.rng.choice(self.bins)

    def __getitem__(self, index):
        return self.bins[index]


def Bet(object):
    """Player to Outcome API"""

    def __init__(self, amount, outcome):
        self.amount = amount
        self.outcome = outcome

    def winAmount(self):
        pass

    def loseAmount(self):
        pass

    def __str__(self):
        return '{amount:s} on {outcome:s}'.format_map(vars(self))

    def __repr__(self):
        return '{class_:s}({name!r}, {odds!r})'.format(
            class_=type(self).__name__, **vars(self))

if __name__ == '__main__':
    build = BinBuilder()
    wheel = Wheel()
    build.buildBins(wheel)
    for bin_ in wheel:
        print(*bin_)
