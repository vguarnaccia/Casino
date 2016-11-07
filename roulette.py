# -*- coding: utf-8 -*-
"""This module contains the business logic for the game of roulette. It is a solution to the
roulette problems in `Building Skills in Object-Oriented Design`_. However, we more closely follow
the `Google Python Style Guide`.

This module contains two important classes:

    :obj:`Wheel` which contains the set of all bets and all bets for each bin (00, and 0 to 36).
    :obj:`Table` which contains all present bets by a player.

The game and player exist independently from casino table game.

Todo:
    * Go over  `Google Python Style Guide` and `Napoleon`_ examples
    * reread instruction and document.
    * implement logger

.. _`Building Skills in Object-Oriented Design`:
    http://buildingskills.itmaybeahack.com/oodesign.html#book-oodesign

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

.. _Napoleon:
    http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""

import random
import logging
from pprint import pprint

# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)


class Outcome(object):
    """Store the name of a possible outcome and its odds

    Note:
        Outcomes should be accessed via the :obj:`Wheel`\\ .

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

    Note:
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
        if 0 < bin_num <= 12:
            dozen = 12
        elif 12 < bin_num <= 24:
            dozen = 24
        elif 24 < bin_num <= 36:
            dozen = 36
        elif bin_num == 0 or bin_num == 37:
            return
        else:
            raise ValueError
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
        """Add outcomes to bin and maintain set of distinct outcomes

        Args:
            bin (int): the bin index from 0 to 37 inclusive.
            outcome (:obj:`Outcome) the :obj:`Outcome to add to this bin.
        """
        self.bins[number].add(outcome)
        self.all_outcomes.add(outcome)

    def getOutcome(self, name):
        """get all outcomes containing ``name``

        Arg:
            name (str): name of desired outcomes, by partial match, case insensitive.

        Return:
            Set of all outcomes matching ``name``.
        """
        return {oc for oc in self.all_outcomes if name.casefold() in oc.name.casefold()}

    def next(self):
        """Select bin from bins

        Return:
            bin (:obj:`Bin`): random bin from wheel.
        """
        return self.rng.choice(self.bins)

    def __getitem__(self, index):
        return self.bins[index]


class Bet(object):
    """Player to Outcome API.

    A player uses the wheel object's unique set of bets to place an bet with an amount.

        Attributes:
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
        return '{amount:.2f} on {outcome}'.format_map(vars(self))

    def __repr__(self):
        return '{class_:s}({amount!r}, {outcome!r})'.format(
            class_=type(self).__name__, **vars(self))

    def __add__(self, other):
        """allows for summing of bets"""
        return self.amount + other.amount

    def __radd__(self, other):
        """allows for summing of bets"""
        return other + self.amount


class InvalidBet(Exception):
    """InvalidBet is raised when the Player attempts to place a bet which exceeds the table’s limit.
    """
    pass


class Table(object):
    """Table contains all the Bets created by the Player.
    A table also has a betting limit, and the sum of all of a player’s bets must be
    less than or equal to this limit. We assume a single Player in the simulation.

    Note:
        We've made the design choice to deduct a player's bet amount when a bet is placed.

    Attributes:
        limit (int): This is the table limit.
        The sum of the bets from a Player must be less than or equal to this limit.

        minimum (int): This is the table minimum.
        Each individual bet from a Player must be greate than this limit.

        bets (:obj:`list` of :obj:`Bet`): This is a list of the Bets currently active.
        These will result in either wins or losses to the Player.
    """

    def __init__(self, limit, minimum, bets):
        self.limit = limit
        self.minimum = minimum
        self.bets = bets
        self.Table = None  # not implemented constructor

    def placeBet(self, bet):
        """Table to bet interface.

        Args:
            bet (:obj:`Bet`): A Bet instance to be added to the table.

        Raise:
            InvalidBet: indicates bug in :obj:`Player`
        """
        self.bets.append(bet)
        self.isValid()

    def isValid(self):
        """Check table limit rule.

        Raise:	InvalidBet if the bets don’t pass the table limit rules.

        Applies the table-limit rules:

        * The sum of all bets is less than or equal to the table limit.
        * All bet amounts are greater than or equal to the table minimum
        """
        if self.minimum <= sum(self.bets) <= self.limit:
            return None
        else:
            raise InvalidBet

    def __iter__(self):
        """Iterate over all bet in bets.

        Yield:
            bet (:obj:`Bet`)
        """
        for bet in self.bets:
            yield bet

    def __str__(self):
        """Easy-to-read representation of all bets"""
        pprint(self.bets)

    def __repr__(self):
        return '{class_:s}({bets!r})'.format(
            class_=type(self).__name__, **vars(self))
