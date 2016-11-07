#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Player simulator for roulette that creates ``players`` to implement strategies.
It also allows the player to collect statistics and analyze their effectiveness

Todo:
    * Go over  `Google Python Style Guide` and `Napoleon`_ examples
    * make sure backslashes in rst worked out properly.
    * build logger.
"""

import roulette as rl
import logging


# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)


class Player(object):
    """not implemented yet

    Todo:
        * implement this base class
    """
    pass


class Passenger57(Player):
    """dead simple player that always bets on black and has infinite money.

    Attributes:
        table (:obj:`Table`): The :obj:`Table` instance on which bets are placed.
        wheel (:obj:`Wheel`): The :obj:`Wheel` instance which defines all :obj:`Outcome`\\ s.
        black (:obj:`Outcome`): This :obj:`Player` always bets on Black.
    """

    def __init__(self, wheel, table):
        self.table = table
        self.wheel = wheel
        self.stake = float('inf')
        outcome = wheel.getOutcome('Black')
        amount = 10  # actually, not implemented
        self.black = rl.Bet(amount, outcome)  # instance of bet black

    def placeBets(self):
        """Updates the ``table`` with the various bets.

        This version creates a :obj:`Bet` instance from the black Outcome.
        It uses :obj:`Table`\\ 's placeBet() to place that bet.
        """
        bet = self.black
        self.stake -= bet.loseAmount()
        self.table.placeBet(bet)

    def win(self, bet):
        """Notification from :obj:`Game` that the :obj:`Bet` was a winner.

        The amount of money won is available via the winAmount() method of :obj:`Bet`\\ .

        Arg:
            bet (:obj:`Bet`): the bet which won.
        """
        self.stake += bet.winAmount()


    def lose(self, bet):
        """Notification from :obj:`Game` that the :obj:`Bet` was a loser.

        Arg:
            bet (:obj:`Bet`): the bet which lost.
        """
        return None


class Game(object):
    """manages the sequence of actions that defines the game of Roulette

    This includes notifying the :obj:`Player` to place bets, spinning the :obj:`Wheel` and
    resolving the :obj:`Bet`\\ s actually present on the Table.

    Attributes:
        wheel (:obj:`Wheel`): The :obj:`Wheel` that returns a randomly selected :obj:`Bin`\\ .
        table (:obj:`Table`): the :obj:`Table` which contains the :obj:`Bet`\\ s
            placed by :obj:`Player`\\ .
    """

    def __init__(self, wheel, table):
        self.wheel = wheel
        self.table = table

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
        player.placeBets() # real work of placing bet is delegated to Player class
        winning_bets = self.wheel.next()
        for bet in player.table:
            player.win(bet) if bet in winning_bets else player.lose(bet)



if __name__ == '__main__':
    wheel = rl.Wheel()
