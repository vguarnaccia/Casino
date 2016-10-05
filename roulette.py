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

def test_full_TABLE():
    assert '00' in TABLE, 'missing 00'
    for bet in range(37):
        assert str(bet) in TABLE, 'missing bet %s' % bet

def test_TABLE_pairs():
    """test ensure that TABLE key-value pairs have valid attributes
    Does not test if color is correct.
    """
    for k, v in TABLE.items():
        if type(v).__name__ == 'Layout':
            assert v.color in ('red', 'black'), 'Invalid color %s' % k
            evenness = 'even' if int(k) % 2 == 0 else 'odd'
            assert v.evenness == evenness, 'Evenness error %s' % k
            if 0 < int(k) < 13:
                thirds = 'first 12'
            elif 12 < int(k) < 25:
                thirds = 'second 12'
            elif 24 < int(k) <= 36:
                thirds = 'third 12'
            else:
                thirds = 'oops'
            assert v.third == thirds, 'Wrong thirds range %s' % k
            half = 'low' if 0 < int(k) <= 18 else 'high'
            assert v.half == half and int(k) <= 36, 'Not high nor low %s' % k
            if (int(k) % 3) == 1:
                column = 1
            elif (int(k) % 3) == 2:
                column = 2
            elif (int(k) % 3) == 0:
                column = 3
            else:
                column = 'oops'
            assert v.column == column, 'Invalid column number %s' % k
        else:
            assert k == '0' or '00', 'Invalid bet'
            assert v.color == 'green', 'Invalid bet type'


def tests():
    test_full_TABLE()
    test_TABLE_pairs()

if __name__ == '__main__':
    tests()
