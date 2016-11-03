#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This game simulates roulette and allows players to implement strategies.
It also allows the player to collect statistics and analyze their effectiveness

Todo:
    * Go over google style guide
    http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
    * reread instruction and document.
"""

import random
import logging

# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)


class Outcome(object):
    """Store the name of a possible outcome and its odds

    Attributes:
        name (str): Name of the outcome
        odds (int): Denominator for odds, i.e. odds of 17:1 means Odds = 17
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
            class_=type(self).__name__, **vars(self))

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Bin(set):
    """Extension to built-in set class and builder to fill in outcomes for all bin numbers"""


class BinBuilder(object):
    """builder for adding outcomes to bins in the wheel

    This class is not pythonic and could be written much better.
    It contains a static method called buildBins which populates all the bins in a :obj:`Wheel`.

    Examples:
        >>> wheel = Wheel()
        >>> BinBuilder.buildBins(wheel)

    """

    def __init__(self):
        pass

    def _check_pair(self, pair):
        """Check if all bin positions in pair are feasible."""
        return all(0 < i < 37 for i in pair)

    def _straight_bet(self, wheel, bin_num):
        """Create straight bet outcome for bin"""
        if bin_num < 37:
            wheel.addOutcome(bin_num, Outcome('Straight %d' % bin_num, 35))
        elif bin_num == 37:
            wheel.addOutcome(bin_num, Outcome('Straight 00', 35))
        else:
            raise IndexError

    def _split_bet(self, wheel, bin_num):
        """Create split bet outcomes for bin"""
        possible_pairs = {'right': (bin_num, bin_num + 1),
                          'left': (bin_num - 1, bin_num),
                          'up': (bin_num, bin_num + 3),
                          'down': (bin_num - 3, bin_num)}
        if 0 < bin_num < 37:
            if bin_num == 1:
                pairs = (possible_pairs['right'], possible_pairs['up'])
            elif bin_num == 3:
                pairs = (possible_pairs['left'], possible_pairs['up'])
            elif bin_num == 34:
                pairs = (possible_pairs['right'], possible_pairs['down'])
            elif bin_num == 36:
                pairs = (possible_pairs['left'], possible_pairs['down'])
            else:
                if bin_num % 3 == 1:
                    pairs = (possible_pairs['right'],
                             possible_pairs['up'],
                             possible_pairs['down'])
                elif bin_num % 3 == 2:
                    pairs = possible_pairs.values()
                elif bin_num % 3 == 0:
                    pairs = (possible_pairs['left'],
                             possible_pairs['up'],
                             possible_pairs['down'])
            for pair in pairs:
                if self._check_pair(pair):
                    name = 'Split {0}-{1}'.format(*pair)
                    wheel.addOutcome(bin_num, Outcome(name, 17))

    def _street_bet(self, wheel, bin_num):
        """Create street bet outcomes for bin"""
        if 0 < bin_num < 37:
            first_bin_num = bin_num
            while bin_num % 3 != 1:
                bin_num -= 1
            name = 'Street {0}-{1}-{2}'.format(bin_num, bin_num+1, bin_num+2)
            wheel.addOutcome(first_bin_num, Outcome(name, 11))

    def _corner_bet(self, wheel, bin_num):
        """Create corner bet outcomes for bin"""
        possible_pairs = {
                     'right-up':
                                (bin_num, bin_num + 1, bin_num + 3, bin_num + 4),
                     'left-up':
                                (bin_num - 1, bin_num, bin_num + 2, bin_num + 3),
                     'right-down':
                                (bin_num - 3, bin_num - 2, bin_num, bin_num + 1),
                     'left-down':
                                (bin_num - 4, bin_num - 3, bin_num - 1, bin_num)
                             }
        if 0 < bin_num < 37:
            if bin_num == 1:
                pairs = (possible_pairs['right-up'],)
            elif bin_num == 3:
                pairs = (possible_pairs['left-up'],)
            elif bin_num == 34:
                pairs = (possible_pairs['right-down'],)
            elif bin_num == 36:
                pairs = (possible_pairs['left-down'],)
            else:
                if bin_num % 3 == 1:
                    pairs = (possible_pairs['right-down'],
                             possible_pairs['right-up'])
                elif bin_num % 3 == 2:
                    pairs = possible_pairs.values()
                elif bin_num % 3 == 0:
                    pairs = (possible_pairs['left-down'],
                             possible_pairs['left-up'])
            for pair in pairs:
                if self._check_pair(pair):
                    name = 'Corner {0}-{1}-{2}-{3}'.format(*pair)
                    wheel.addOutcome(bin_num, Outcome(name, 8))

    def _line_bet(self, wheel, bin_num):
        """Create line bet outcomes for bin"""
        lines = [[i for i in range(j, j + 6)] for j in (1, 7, 13, 19, 25, 31)]
        for line in lines:
            if bin_num in line and self._check_pair(line):
                name = 'Line {0}-{1}-{2}-{3}-{4}-{5}'.format(*line)
                wheel.addOutcome(bin_num, Outcome(name, 5))

    def _dozen_bet(self, wheel, bin_num):
        """Create dozen bet outcomes for bin"""
        if 0 < bin_num < 37:
            dozen = 12 * ((bin_num // 12) + 1)
            name = 'Dozen {0:d}'.format(dozen)
            wheel.addOutcome(bin_num, Outcome(name, 2))

    def _column_bet(self, wheel, bin_num):
        """Create column bet outcomes for bin"""
        if 0 < bin_num < 37:
            column = bin_num % 3 if bin_num % 3 > 0 else 3
            name = 'Column {0:d}'.format(column)
            wheel.addOutcome(bin_num, Outcome(name, 2))

    def _color_bet(self, wheel, bin_num):
        """Create color bet outcomes for bin"""
        REDS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 34, 36}
        if 0 < bin_num < 37:
            wheel.addOutcome(bin_num, Outcome('Red', 2) if bin_num in REDS else Outcome('Black', 2))

    def _evenness_bet(self, wheel, bin_num):
        """Create evenness bet outcomes for bin"""
        if 0 < bin_num < 37:
            if bin_num % 2 == 0:
                wheel.addOutcome(bin_num, Outcome('Even', 2))
            else:
                wheel.addOutcome(bin_num, Outcome('Odd', 2))

    def _hight_bet(self, wheel, bin_num):
        """Create hight bet outcomes for bin"""
        if 0 < bin_num < 18:
            wheel.addOutcome(bin_num, Outcome('Low', 2))
        elif 18 < bin_num < 37:
            wheel.addOutcome(bin_num, Outcome('High', 2))

    def _five_bet(self, wheel, bin_num):
        """Create five bet outcomes for bin"""
        if bin_num in (0, 1, 2, 3, 37):
            wheel.addOutcome(bin_num, Outcome('00-0-1-2-3', 6))

    @staticmethod
    def buildBins(wheel):
        """Builder to create all outcomes for bin with bin number"""
        builder = BinBuilder()
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
                getattr(builder, bet)(wheel, bin_num)


class Wheel(object):
    """Container for 38 bins and PRNG to select one at random"""

    def __init__(self):
        self.bins = [Bin() for _ in range(38)]
        self.all_outcomes = set()
        # index 37 = '00', else index matches slot
        self.rng = random.Random()

    def addOutcome(self, number, outcome):
        """Add outcomes to bin and maintain set of distinct outcomes"""
        self.bins[number].add(outcome)
        self.all_outcomes.add(outcome)

    def getOutcome(self, name):
        """get all outcomes containing ``name``"""
        return {oc for oc in self.all_outcomes if name.casefold() in oc.name.casefold()}

    def next(self):
        """Select bin from bins"""
        self.rng.choice(self.bins)

    def __getitem__(self, index):
        return self.bins[index]


def Bet(object):
    """Player to Outcome API.

    A plyaer uses the wheel object's unique set of bets to place an bet with an amount.

        Args:
            amount (int): amount bet
            outcome (Outcome): the :class:`Outcome` we're betting on"""

    def __init__(self, amount, outcome):
        self.amount = amount
        self.outcome = outcome

    def winAmount(self):
        """Uses the Outcome‘s winAmount to compute the amount won, given the amount of this bet.
        Note that the amount bet must also be added in.
        A 1:1 outcome (e.g. a bet on Red) pays the amount bet plus the amount won.
        """
        return self.amount + self.outcome.winAmount(self.amount)

    def loseAmount(self):
        """returns the amount bet as the amount lost.
        This is the cost of placing the bet."""
        return self.amount

    def __str__(self):
        return '{amount:s} on {outcome:s}'.format_map(vars(self))

    def __repr__(self):
        return '{class_:s}({amount!r}, {outcome!r})'.format(
            class_=type(self).__name__, **vars(self))

if __name__ == '__main__':
    wheel = Wheel()
    builder = BinBuilder()
    builder.buildBins(wheel)
