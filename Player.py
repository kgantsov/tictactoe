#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from AI import minimax


class Player(object):
    symbol = 'X'

    def __init__(self, symbol):
        self.symbol = symbol

    def move(self, grid):
        return None

    @property
    def title(self):
        if self.symbol == 'X':
            return 'Player 1'
        elif self.symbol == 'O':
            return 'Player 2'


class Human(Player):
    pass


class Computer(Player):
    complexity = 'Hard'
    complexities = {
        'Hard': 0,
        'Normal': 3,
        'Easy': 6
    }

    def __init__(self, symbol, complexity):
        super(Computer, self).__init__(symbol)
        self.complexity = complexity

    def move(self, grid):
        avaliable_moves = self._get_avaliable_moves(grid)

        if random.randint(1, 12) <= self.complexities[self.complexity]:
            return random.choice(avaliable_moves)

        if len(avaliable_moves) == 8:
            x = grid.find('X')
            if x != 4:
                return 4

            return random.choice([0, 2, 6, 8])

        score, move = minimax(grid, self.symbol)
        if move != None:
            for i in range(9):
                if grid[i] != move[i]:
                    return i

    def _get_avaliable_moves(self, grid):
        return [i for i, el in enumerate(grid) if el == '-']


class PlayerFabric(object):
    @staticmethod
    def make_players(with_ai, complexity):
        if with_ai:
            return (Human('X'), Computer('O', complexity))
        else:
            return (Human('X'), Human('O'))
