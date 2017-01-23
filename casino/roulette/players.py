#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Player simulator for roulette that creates `Player` to implement strategies.
It also allows the player to collect statistics and analyze their effectiveness

Todo:
    * Go over  `Google Python Style Guide`_ and `Napoleon`_ examples
    * make sure backslashes in rst worked out properly.
    * build logger.
    * `incorporate solution Q&A into doc. <http://buildingskills.itmaybeahack.com/book/oodesign-3.1/html/roulette/solution.html#roul-ov-qanda-main>`_

"""

import logging
from abc import ABCMeta, abstractmethod
import statistics as stats

from . import board as bd

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

    def lose(self):
        """Notification from :obj:`Game` that the :obj:`Bet` was a loser.

        Arg:
            bet (:obj:`Bet`): the bet which lost.
        """
        self.table.clear()

    def playing(self):
        """is player to active?"""
        return (self.roundsToGo > 0)

    def setStake(self, stake):
        self.stake = stake

    def setRounds(self, rounds):
        self.roundsToGo = rounds


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
        bets = [bd.Bet(amount, self.black)]  # instance of bet black
        self._placeBets_helper(bets)


class Martingale(Player):
    """`Martingale` is a `Player` who doubles their bet on every loss and resets their bet on win.

    Attributes:
        lossCount (int): number of times to double the bet.
        betMultiple (int): bet multiplier based on the number of bets. Equal to 2^lossCount.
        """

    def __init__(self, table, wheel):
        super(Martingale, self).__init__(table, wheel)  # call abc __init__
        self.black = self.wheel.getOutcome('Black').pop()  # getOutcome returns a set
        self.lossCount = 0

    @property
    def betMultiple(self):
        """doulbe bet after each loss"""
        return 2**self.lossCount

    def placeBets(self):
        super(Martingale, self).__doc__ + \
            """Bet amount doubles after each loss and resets after each win"""
        amount = 10 * self.betMultiple  # actually, not implemented
        bets = [bd.Bet(amount, self.black)]  # instance of bet black
        self._placeBets_helper(bets)

    def win(self, bet):
        """Same as `Player`\\ 's win method but resets `lossCount`\\ ."""
        self.lossCount = 0
        super(Martingale, self).win(bet)

    def lose(self):
        """Same as `Player`\\ 's lose method but increments `lossCount`\\ ."""
        self.lossCount += 1
        super(Martingale, self).lose()


class Game:
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
                if bet.outcome in winning_outcomes:
                    player.win(bet)
                else:
                    player.lose()


class Simulator:
    """Simulate the Roulette game with the `Player` class.
    Reports saw statistics on a number of sessions of play

    Notes:
        cycle:
            A single cycle of betting and bet resolution.
        session:
            One or more cycles in which a player starts with a full stakes.
            Player may decide to leave or may run out of money.
        game:
            Some games may have intermediate events between cycles and sessions.

    Args:
        game (`Game`): The Game to simulate.
        player (`Player`): The player and thus betting strategy.
        initDuration (int, default 250): Length of simulation.
        initStake (int, default 100): Initial money amount.
        samples (int, default 50): Number of game cycles.

    Attributes:
        durations (list): list of lenghts of time the `Player` remained in the game.
        maxima (list): list of maximum stakes for each `Player`.
        See args.
    """

    def __init__(self, game, player, initDuration=250, initStake=100, samples=50):
        self.game = game
        self.player = player
        self.initDuration = initDuration
        self.initStake = initStake
        self.samples = samples

    def session(self):
        """Execute a single game session.

        Return:
            `list` of stake values.
        """
        stakes = []
        self.player.setStake(self.initStake)
        self.player.setRounds(self.initDuration)
        while self.player.playing:
            self.game.cycle(self.player)
            stakes.append(self.player.stake)
        return stakes

    def gather(self):
        """Execute a number of sessions and collect statistics"""
        duration = []
        maxima = []
        for _ in range(self.samples):
            stakes = self.session()
            self.duration.append(len(stakes))
            self.maxima.apppend(max(stakes))
        average_duration, stdev_of_duration = stats.mean(duration), stats.stdev(duration)
        average_maxima, stdev_of_maxima = stats.mean(maxima), stats.stdev(maxima)
        return (average_duration, stdev_of_duration), (average_maxima, stdev_of_maxima)



if __name__ == '__main__':
    wheel = bd.Wheel()
