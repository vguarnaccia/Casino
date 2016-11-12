#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Player simulator for roulette that creates ``players`` to implement strategies.
It also allows the player to collect statistics and analyze their effectiveness

Todo:
    * Go over  `Google Python Style Guide` and `Napoleon`_ examples
    * make sure backslashes in rst worked out properly.
    * build logger.
    * `incorporate solution Q&A into doc.
    <http://buildingskills.itmaybeahack.com/book/oodesign-3.1/html/roulette/solution.html#roul-ov-qanda-main>``:
"""

import roulette as rl
import logging
from abc import ABCMeta, abstractmethod

# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)


class Player(metaclass=ABCMeta):
    """This is a base class for designing players.

    Note:
        Subclass must implement `placeBets()` and may override `__init__`\\ .

    Attributes:
        table (Table): The instance of `Table` that `Bet`\\ s are placed on.
        wheel (Wheel): The instance of `Wheel` that contain allowable `Bet`\\ s.
        stake (int, default 1000): the player's current stake.
        roundsToGo (int, default 100): the number of rounds to play.
    """

    def __init__(self, table, wheel):
        self.table = table
        self.wheel = wheel
        self.stake = 1000  # default, can be set with method
        self.roundsToGo = 100  # default, can be set with method

    def _placeBets_helper(self, bets):
        for bet in bets:
            self.stake -= bet.loseAmount()
        self.table.placeBet(bets)

    @abstractmethod
    def placeBets(self):
        """Updates the ``table`` with the various bets.

        This version creates a :obj:`Bet` instance from the black Outcome.
        It uses :obj:`Table`\\ 's placeBet() to place that bet.
        """
        # bet = not implemented
        # self._placeBets_helper(bets)
        pass

    def win(self, bet):
        """Notification from :obj:`Game` that the :obj:`Bet` was a winner.

        The amount of money won is available via the winAmount() method of :obj:`Bet`\\ .

        Arg:
            bet (:obj:`Bet`): the bet which won.
        """
        self.stake += bet.winAmount()
        self.table.clear()

    def lose(self, bet):
        """Notification from :obj:`Game` that the :obj:`Bet` was a loser.

        Arg:
            bet (:obj:`Bet`): the bet which lost.
        """
        self.table.clear()

    def playing(self):
        """is player to active?"""
        return (self.roundsToGo > 0)


class Passenger57(Player):
    """dead simple player that always bets on black and has infinite money.

    Attributes:
        table (Table): The :obj:`Table` instance on which bets are placed.
        wheel (Wheel): The :obj:`Wheel` instance which defines all :obj:`Outcome`\\ s.
    """

    def __init__(self, table, wheel):
        super(Passenger57, self).__init__(table, wheel)  # call abc __init__
        self.black = self.wheel.getOutcome(
            'Black').pop()  # getOutcome returns a set

    def placeBets(self):
        """Updates the ``table`` with the various bets.

        This version creates a :obj:`Bet` instance from the black Outcome.
        It uses :obj:`Table`\\ 's placeBet() to place that bet.
        """
        amount = 10  # just a placeholder.
        bets = [rl.Bet(amount, self.black)]  # instance of bet black
        self._placeBets_helper(bets)


class Martingale(Player):
    """`Martingale` is a `Player` who doubles their bet on every loss and resets their bet on win.

    Attributes:
        lossCount (int): number of times to double the bet.
        betMultiple (int): bet multiplier based on the number of bets. Equal to 2^lossCount.
        """

    def __init__(self, table, wheel):
        super(Martingale, self).__init__(table, wheel)  # call abc __init__
        self.black = self.wheel.getOutcome(
            'Black').pop()  # getOutcome returns a set
        self.lossCount = 0

    @property
    def betMultiple(self):
        """doulbe bet after each loss"""
        return 2**self.lossCount

    def placeBets(self):
        super(Martingale, self).__doc__ + \
            """Bet amount doubles after each loss and resets after each win"""
        amount = 10 * self.betMultiple  # actually, not implemented
        bets = [rl.Bet(amount, self.black)]  # instance of bet black
        self._placeBets_helper(bets)

    def win(self, bet):
        """Same as `Player`\\ 's win method but resets `lossCount`\\ ."""
        self.lossCount = 0
        super(Martingale, self).win(bet)

    def lose(self, bet):
        """Same as `Player`\\ 's lose method but increments `lossCount`\\ ."""
        self.lossCount += 1
        super(Martingale, self).lose(bet)


class Game(object):
    """manages the sequence of actions that defines the game of Roulette

    This includes notifying the :obj:`Player` to place bets, spinning the :obj:`Wheel` and
    resolving the :obj:`Bet`\\ s actually present on the Table.

    Attributes:
        table (:obj:`Table`): the :obj:`Table` which contains the :obj:`Bet`\\ s
            placed by :obj:`Player`\\ .
        wheel (:obj:`Wheel`): The :obj:`Wheel` that returns a randomly selected :obj:`Bin`\\ .
    """

    def __init__(self, table, wheel):
        self.table = table
        self.wheel = wheel

    def cycle(self, player):
        """Executes a single cycle of play.

        Cycle:
            1. call the :obj:`Player`\\ 's placeBets() to get bet.
            2. call the :obj:`Wheel`\\ 's next() to get winning :obj:`Bin`\\ .
            3. iterate over :obj:`Table`\\ 's :obj:`Bet`\\ s.
            4. call the :obj:`Player`\\ 's win() or lose() method.

        Arg:
            player (:obj:`Player`): the individual player that places bets,
                receives winnings and pays losses.
        """
        if player.playing:
            player.placeBets()  # real work of placing bet is delegated to Player class
            winning_outcomes = self.wheel.next()
            for bet in player.table:
                player.win(
                    bet) if bet.outcome in winning_outcomes else player.lose(bet)


if __name__ == '__main__':
    wheel = rl.Wheel()
