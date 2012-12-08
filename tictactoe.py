#!/usr/bin/env python
# -*- coding: utf-8 -*-


import kivy
kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from AI import is_full, is_win, move
from Player import PlayerFabric


class TicTacToeGameGrid(StackLayout):
    player = True
    with_ai = True
    complexity = 'Hard'

    xo_cell_0 = ObjectProperty(None)
    xo_cell_1 = ObjectProperty(None)
    xo_cell_2 = ObjectProperty(None)
    xo_cell_3 = ObjectProperty(None)
    xo_cell_4 = ObjectProperty(None)
    xo_cell_5 = ObjectProperty(None)
    xo_cell_6 = ObjectProperty(None)
    xo_cell_7 = ObjectProperty(None)
    xo_cell_8 = ObjectProperty(None)
    with_ai_switch = ObjectProperty(None)
    complexity_spiner = ObjectProperty(None)

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

        self.with_ai_switch.bind(active=self.with_ai_switch_change)
        self.complexity_spiner.bind(text=self.complexity_spiner_change)

        self.new_game()

    def on_new_game(self, instance):
        self.new_game()

    def new_game(self):
        self.grid = '---------'
        for key, btn in self.cells.items():
            btn.background_normal = 'images/blank.png'

        self.player_1, self.player_2 = PlayerFabric.make_players(
            self.with_ai,
            self.complexity
        )
        self.cur_player = self.player_1

    def with_ai_switch_change(self, instance, enable):
        self.with_ai = enable
        self.new_game()

    def complexity_spiner_change(self, instance, text):
        self.complexity = text
        self.new_game()

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
        self.cells[cell].background_normal = 'images/%s.png' % symbol.lower()
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
        new_game_btn.bind(on_release=self.on_new_game)
        new_game_btn.bind(on_release=popup.dismiss)
        popup.open()


class TicTacToeApp(App):
    def build(self):
        return TicTacToeGameGrid(cols=3)

if __name__ == '__main__':
    TicTacToeApp().run()
