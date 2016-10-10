#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This game simulates roulette and allows players to implement strategies.
It also allows the player to collect statistics and analyze their effectiveness"""

from collections import namedtuple
import logging

# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)

Layout = namedtuple('Layout', 'color, evenness, third, half, column')
Zero = namedtuple('Lero', 'color, evenness, third, half, column')

TABLE = {
    '00': Zero('green', 'na', 'na', 'na', 'na'),
    '0': Zero('green', 'na', 'na', 'na', 'na'),
    '1': Layout('red', 'odd', 'first 12', 'low', 1),
    '2': Layout('black', 'even', 'first 12', 'low', 2),
    '3': Layout('red', 'odd', 'first 12', 'low', 3),
    '4': Layout('black', 'even', 'first 12', 'low', 1),
    '5': Layout('red', 'odd', 'first 12', 'low', 2),
    '6': Layout('black', 'even', 'first 12', 'low', 3),
    '7': Layout('red', 'odd', 'first 12', 'low', 1),
    '8': Layout('black', 'even', 'first 12', 'low', 2),
    '9': Layout('red', 'odd', 'first 12', 'low', 3),
    '10': Layout('black', 'even', 'first 12', 'low', 1),
    '11': Layout('black', 'odd', 'first 12', 'low', 2),
    '12': Layout('red', 'even', 'first 12', 'low', 3),
    '13': Layout('black', 'odd', 'second 12', 'low', 1),
    '14': Layout('red', 'even', 'second 12', 'low', 2),
    '15': Layout('black', 'odd', 'second 12', 'low', 3),
    '16': Layout('red', 'even', 'second 12', 'low', 1),
    '17': Layout('black', 'odd', 'second 12', 'low', 2),
    '18': Layout('red', 'even', 'second 12', 'low', 3),
    '19': Layout('red', 'odd', 'second 12', 'high', 1),
    '20': Layout('black', 'even', 'second 12', 'high', 2),
    '21': Layout('red', 'odd', 'second 12', 'high', 3),
    '22': Layout('black', 'even', 'second 12', 'high', 1),
    '23': Layout('red', 'odd', 'second 12', 'high', 2),
    '24': Layout('black', 'even', 'second 12', 'high', 3),
    '25': Layout('red', 'odd', 'third 12', 'high', 1),
    '26': Layout('black', 'even', 'third 12', 'high', 2),
    '27': Layout('red', 'odd', 'third 12', 'high', 3),
    '28': Layout('black', 'even', 'third 12', 'high', 1),
    '29': Layout('black', 'odd', 'third 12', 'high', 2),
    '30': Layout('red', 'even', 'third 12', 'high', 3),
    '31': Layout('black', 'odd', 'third 12', 'high', 1),
    '32': Layout('red', 'even', 'third 12', 'high', 2),
    '33': Layout('black', 'odd', 'third 12', 'high', 3),
    '34': Layout('red', 'even', 'third 12', 'high', 1),
    '35': Layout('black', 'odd', 'third 12', 'high', 2),
    '36': Layout('red', 'even', 'third 12', 'high', 3),
}


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


class Bin(frozenset):
    """Extension to built-in frozenset class"""



if __name__ == '__main__':
    pass
