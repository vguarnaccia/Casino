"""This module contains the BinBuilder class. Frankly, this class should just be turned into a module."""

from .board import Outcome

class BinBuilder:
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
            name = 'Street {0}-{1}-{2}'.format(bin_num,
                                               bin_num + 1, bin_num + 2)
            wheel.addOutcome(first_bin_num, Outcome(name, 11))

    def _corner_bet(self, wheel, bin_num):
        """Create corner bet outcomes for bin"""
        possible_pairs = {
            'right-up': (bin_num, bin_num + 1, bin_num + 3, bin_num + 4),
            'left-up': (bin_num - 1, bin_num, bin_num + 2, bin_num + 3),
            'right-down': (bin_num - 3, bin_num - 2, bin_num, bin_num + 1),
            'left-down': (bin_num - 4, bin_num - 3, bin_num - 1, bin_num)
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
        reds = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 34, 36}
        if 0 < bin_num < 37:
            wheel.addOutcome(
                bin_num,
                Outcome('Red', 1) if bin_num in reds else Outcome('Black', 1)
                )

    def _evenness_bet(self, wheel, bin_num):
        """Create evenness bet outcomes for bin"""
        if 0 < bin_num < 37:
            if bin_num % 2 == 0:
                wheel.addOutcome(bin_num, Outcome('Even', 1))
            else:
                wheel.addOutcome(bin_num, Outcome('Odd', 1))

    def _hight_bet(self, wheel, bin_num):
        """Create hight bet outcomes for bin"""
        if 0 < bin_num < 18:
            wheel.addOutcome(bin_num, Outcome('Low', 1))
        elif 18 < bin_num < 37:
            wheel.addOutcome(bin_num, Outcome('High', 1))

    def _five_bet(self, wheel, bin_num):
        """Create five bet outcomes for bin"""
        if bin_num in (0, 1, 2, 3, 37):
            wheel.addOutcome(bin_num, Outcome('00-0-1-2-3', 6))

    @staticmethod
    def buildBins(wheel):
        """Builder to create all outcomes for bin with bin number

        Args:
            wheel (:obj:`Wheel`): `Wheel` to be populated with outcomes.

        """
        builder = BinBuilder()
        bets = {
            '_straight_bet',
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
