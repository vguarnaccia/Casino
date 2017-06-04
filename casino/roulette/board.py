# -*- coding: utf-8 -*-
"""This module contains the business logic for the game of roulette. It is a solution to the
roulette problems in `Building Skills in Object-Oriented Design`_. However, we more closely follow
the `Google Python Style Guide`_.

This module contains two important classes:

    :obj:`Wheel` which contains the set of all bets and all bets for each bin (00, and 0 to 36).
    :obj:`Table` which contains all present bets by a player.

The game and player exist independently from casino table game.

Todo:
    * Go over  `Google Python Style Guide`_ and `Napoleon`_ examples
    * reread instruction and document.
    * implement logger

.. _`Building Skills in Object-Oriented Design`:
    http://buildingskills.itmaybeahack.com/oodesign.html#book-oodesign

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

.. _Napoleon:
    http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""

import logging
import random
from builtins import object, range
from pprint import pprint

# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)


class Outcome(object):
    """Store the name of a possible outcome and its odds.

    Note:
        Outcomes should be accessed via the :obj:`Wheel`.

    Attributes:
        name (str): Name of the outcome
        odds (int): Denominator for odds, i.e. odds of 17:1 means ``odds`` = 17
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


class Wheel(object):
    """Container for 38 bins and PRNG to select one at random"""

    def __init__(self):
        self.bins = [Bin() for _ in range(38)]
        self.all_outcomes = set()
        # index 37 = '00', else index matches slot
        self.rng = random.Random()

    def addOutcome(self, number, outcome):
        """Add outcomes to bin and maintain set of distinct outcomes.

        Args:
            bin (int): the bin index from 0 to 37 inclusive.
            outcome (:obj:`Outcome`) the `Outcome` to add to this bin.
        """
        self.bins[number].add(outcome)
        self.all_outcomes.add(outcome)

    def getOutcome(self, name):
        """get all outcomes containing ``name``

        Args:
            name (str): name of desired outcomes, by partial match, case insensitive.

        Return:
            set: all outcomes matching ``name``.
        """
        return {oc for oc in self.all_outcomes if name.lower() in oc.name.lower()}

    def __next__(self):
        """Select bin from bins

        Return:
            :obj:`Bin`: random bin from wheel.
        """
        return self.rng.choice(self.bins)

    def __getitem__(self, index):
        return self.bins[index]


class Bet(object):
    """Player to Outcome API.

    A player uses the wheel object's unique set of bets to place an bet with an amount.

    Attributes:
        amount (int): amount bet
        outcome (:obj:`Outcome`): the :obj:`Outcome` we're betting on
    """

    def __init__(self, amount, outcome):
        self.amount = amount
        self.outcome = outcome

    def winAmount(self):
        """Uses the :obj:`Outcome`'s :meth:`winAmount` to compute the amount won, given the amount of this bet.
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
    """InvalidBet is raised when the :obj:`Player` attempts to place a bet which exceeds the table’s limit.
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

        bets (:obj:`list` of :obj:`Bet`\s): This is a list of the Bets currently active.
            These will result in either wins or losses to the Player.
    """

    def __init__(self, limit, minimum, bets=None):
        self.limit = limit
        self.minimum = minimum
        if bets is None:
            self.bets = []
        else:
            self.bets = bets

    def placeBet(self, bets):
        """Table to bet interface.

        Args:
            bet (:obj:`Bet`): A :obj:`Bet` instance to be added to the table.

        Raises:
            :obj:`InvalidBet`: indicates bug in :obj:`.Player`
        """
        try:
            self.bets.extend(bets)
        except TypeError:
            self.bets.append(bets)
        self.isValid()

    def isValid(self):
        """Check table limit rule.

        Raises:
            :obj:`InvalidBet`: if the bets don’t pass the table limit rules.

        Applies the table-limit rules:

        * The sum of all bets is less than or equal to the table limit.
        * All bet amounts are greater than or equal to the table minimum
        """
        if self.minimum <= sum(self.bets) <= self.limit:
            return None
        else:
            raise InvalidBet

    def clear(self):
        """Remove :obj:`Bet`\s once a :obj:`.Player` has won or lost."""
        self.bets = []

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
