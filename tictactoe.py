#!/usr/bin/env python
# -*- coding: utf-8 -*-


import kivy
kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from kivy.factory import Factory
from random import random as r
from functools import partial


class TicTacToeGameGrid(GridLayout):
    player_1 = 'X'
    player_2 = 'O'
    player = True

    xo_cell_0 = ObjectProperty(None)
    xo_cell_1 = ObjectProperty(None)
    xo_cell_2 = ObjectProperty(None)
    xo_cell_3 = ObjectProperty(None)
    xo_cell_4 = ObjectProperty(None)
    xo_cell_5 = ObjectProperty(None)
    xo_cell_6 = ObjectProperty(None)
    xo_cell_7 = ObjectProperty(None)
    xo_cell_8 = ObjectProperty(None)

    grid = '---------'

    def __init__(self, **kwargs):
        super(TicTacToeGameGrid, self).__init__(**kwargs)

        self.cells = {
            0: self.xo_cell_0,
            1: self.xo_cell_1,
            2: self.xo_cell_2,
            3: self.xo_cell_3,
            4: self.xo_cell_4,
            5: self.xo_cell_5,
            6: self.xo_cell_6,
            7: self.xo_cell_7,
            8: self.xo_cell_8
        }

    def click(self, cell_num):
        print 'The button <%s> is being pressed' % cell_num

        if self.wins(self.grid):
            print 'win'
            return

        if self.full(self.grid):
            print 'full'
            return

        if not self.cells[cell_num].text:
            if self.player:
                self.set_symbol(cell_num, self.player_1)
                move = self.get_move(self.grid, self.player_2)
            else:
                self.set_symbol(cell_num, self.player_2)
                move = self.get_move(self.grid, self.player_1)
            self.player = not self.player

            if move != None:
                if self.player:
                    self.set_symbol(move, self.player_1)
                else:
                    self.set_symbol(move, self.player_2)
                self.player = not self.player

    def set_symbol(self, cell, symbol):
        self.cells[cell].text = symbol
        self.grid = self.move(self.grid, cell, symbol)

    def get_move(self, grid, symbol):
        score, move = self.minimax(grid, symbol)
        print grid, move
        if move != None:
            for i in range(9):
                if grid[i] != move[i]:
                    return i

    def move(self, grid, cell, symbol):
        moved = list(grid)
        moved[cell] = symbol
        grid = ''.join(moved)
        return grid

    def moves(self, grid, symbol):
        return [self.move(grid, cell, symbol) for cell in range(9) if grid[cell] not in ('X', 'O')]

    def minimax(self, grid, symbol):
        if self.wins(grid):
            return (1 if symbol is 'O' else -1), None
        elif self.full(grid):
            return 0, None
        elif symbol is 'X':
            best_score = -2
            best_move = None
            for move in self.moves(grid, 'X'):
                score, mv = self.minimax(move, 'O')
                if score >= best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        elif symbol is 'O':
            best_score = 2
            best_move = None
            for move in self.moves(grid, 'O'):
                score, mv = self.minimax(move, 'X')
                if score <= best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def wins(self, grid):
        rows = [[grid[i + j] for j in 0, 1, 2] for i in 0, 3, 6]
        cols = [[grid[i + j] for j in 0, 3, 6] for i in 0, 1, 2]
        digs = [[grid[i] for i in 0, 4, 8], [grid[i] for i in 2, 4, 6]]
        return any(all(cell is 'X' for cell in row) or
                   all(cell is 'O' for cell in row)
                   for row in rows + cols + digs)

    def full(self, grid):
        return all(cell is 'X' or cell is 'O' for cell in grid)


class TicTacToeApp(App):
    def build(self):
        return TicTacToeGameGrid(cols=3)

if __name__ == '__main__':
    TicTacToeApp().run()
