#!/usr/bin/env python
# -*- coding: utf-8 -*-


import kivy
kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from AI import is_full, is_win, move
from Player import PlayerFabric


class WinPopupContent(FloatLayout):
    pass


class TicTacToeGameGrid(GridLayout):
    player = True
    with_ai = True

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

        self.player_1, self.player_2 = PlayerFabric.make_players(self.with_ai)
        self.cur_player = self.player_1

    def new_game(self, instance):
        self.grid = '---------'
        self.cur_player = self.player_1
        for key, btn in self.cells.items():
            btn.text = ''

    def click(self, cell_num):
        if is_win(self.grid):
            self.result_popup()
            return

        if is_full(self.grid):
            self.result_popup()
            return

        if self.is_correct_cell(cell_num):
            self.set_symbol(cell_num, self.cur_player.symbol)
            move = self.cur_player.move(self.grid)

            if move != None:
                self.set_symbol(move, self.cur_player.symbol)

    def is_correct_cell(self, cell_num):
        return self.grid[cell_num] == '-' and not self.cells[cell_num].text

    def set_symbol(self, cell, symbol):
        self.cells[cell].text = symbol
        self.grid = move(self.grid, cell, symbol)

        if is_win(self.grid):
            self.result_popup()
            return

        if is_full(self.grid):
            self.result_popup()
            return

        if self.cur_player == self.player_1:
            self.cur_player = self.player_2
        else:
            self.cur_player = self.player_1

    def result_popup(self):
        if is_win(self.grid):
            title = 'Congratulation!!!'
            message = '%s win!!!' % self.cur_player.title
        elif is_full(self.grid):
            title = 'Draw'
            message = 'Draw'

        new_game_btn = Button(text='New game', size_hint_y=None, height=50)
        close_btn = Button(text='Close', size_hint_y=None, height=50)
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        buttons = BoxLayout(orientation='horizontal')

        buttons.add_widget(new_game_btn)
        buttons.add_widget(close_btn)
        content.add_widget(buttons)
        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(300, 200)
        )
        close_btn.bind(on_release=popup.dismiss)
        new_game_btn.bind(on_release=self.new_game)
        new_game_btn.bind(on_release=popup.dismiss)
        popup.open()


class TicTacToeApp(App):
    def build(self):
        return TicTacToeGameGrid(cols=3)

if __name__ == '__main__':
    TicTacToeApp().run()
