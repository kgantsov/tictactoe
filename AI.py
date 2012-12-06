#!/usr/bin/env python
# -*- coding: utf-8 -*-


def move(grid, cell, symbol):
    moved = list(grid)
    moved[cell] = symbol
    grid = ''.join(moved)
    return grid


def moves(grid, symbol):
    return [move(grid, cell, symbol) for cell in range(9) if grid[cell] not in ('X', 'O')]


def minimax(grid, symbol):
    if is_win(grid):
        return (1 if symbol is 'O' else -1), None
    elif is_full(grid):
        return 0, None
    elif symbol is 'X':
        best_score = -2
        best_move = None
        for move in moves(grid, 'X'):
            score, mv = minimax(move, 'O')
            if score >= best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    elif symbol is 'O':
        best_score = 2
        best_move = None
        for move in moves(grid, 'O'):
            score, mv = minimax(move, 'X')
            if score <= best_score:
                best_score = score
                best_move = move
        return best_score, best_move


def is_win(grid):
    rows = [[grid[i + j] for j in 0, 1, 2] for i in 0, 3, 6]
    cols = [[grid[i + j] for j in 0, 3, 6] for i in 0, 1, 2]
    digs = [[grid[i] for i in 0, 4, 8], [grid[i] for i in 2, 4, 6]]
    return any(all(cell is 'X' for cell in row) or
               all(cell is 'O' for cell in row)
               for row in rows + cols + digs)


def is_full(grid):
    return all(cell is 'X' or cell is 'O' for cell in grid)
