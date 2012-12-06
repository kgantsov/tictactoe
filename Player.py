#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AI import minimax, is_full, is_win, move


class Player():
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
    def move(self, grid):
        score, move = minimax(grid, self.symbol)
        if move != None:
            for i in range(9):
                if grid[i] != move[i]:
                    return i


class PlayerFabric():
    @staticmethod
    def make_players(with_ai):
        if with_ai:
            return (Human('X'), Computer('O'))
        else:
            return (Human('X'), Human('O'))
