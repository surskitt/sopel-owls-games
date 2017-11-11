#!/usr/bin/env python

from sopel.module import commands, rule
from sopel.formatting import color, colors
from random import choice

class Board:
    def __init__(self, player):
        self.board = [[0]*6 for i in range(7)]
        self.players = {1: player}
        self.active_player = 1

        print('{} wants to play connect4! .connect4 to join'.format(player))

    def add_player(self, player):
        if len(self.players) > 1:
            print('There are already two players')
            return

        self.players[2] = player
        print('Game started between {} and {}'.format(*self.players.values()))

    def col_full(self, col):
        return 0 not in self.board[col]

    def add_piece(self, col, player):
        self.board[col][self.board[col].index(0)] = player

        print('Piece added')
        self.print_board()

    def print_board(self):
        pieces = {0: '○', 1: '\x1b[34m●\x1b[0m', 2: '\x1b[31m●\x1b[0m'}

        rows = list(zip(*self.board))[::-1]
        for i in [' '.join(pieces[j] for j in i) for i in rows]:
            print(i)

    def take_turn(self, col, player):
        #  if col not in range(1, 8) or not col.isdigit():
            #  print('Column needs to be between 1 and 7')
            #  return

        col = int(col) - 1

        if len(self.players) < 2:
            print('There needs to be two players before starting')
            return

        if self.players[self.active_player] != player:
            print('It is not your go')
            return

        if self.col_full(col):
            print('No space in column')
            return

        self.add_piece(col, self.active_player)

        if self.check_win():
            print('{} won!'.format(self.players[self.active_player]))

        self.active_player = [1,2][self.active_player == 1]
        print('{}\'s go!'.format(self.players[self.active_player]))

    def check_win(self):
        rows = list(zip(*self.board))[::-1]

        directions = self.board + rows
        check = [''.join(str(j) for j in i) for i in directions]

        return any(any(j in i for j in ['1111', '2222']) for i in check)


def diagonals(L):
    h, w = len(L), len(L[0])
    return [[L[h - p + q - 1][q]
            for q in range(max(p-h+1, 0), min(p+1, w))]
            for p in range(h + w - 1)]

def antidiagonals(L):
    h, w = len(L), len(L[0])
    return [[L[p - q][q]
            for q in range(max(p-h+1,0), min(p+1, w))]
            for p in range(h + w - 1)]

if __name__ == '__main__':
    b = Board('shane')

    b.add_player('someone')
    b.take_turn(1, 'shane')
    b.take_turn(1, 'shane')
    b.take_turn(2, 'someone')
    b.take_turn(1, 'shane')
    b.take_turn(1, 'someone')
    b.take_turn(2, 'shane')
    b.take_turn(4, 'someone')
    b.take_turn(5, 'shane')
    b.take_turn(3, 'someone')
    b.take_turn(6, 'shane')
    b.take_turn(2, 'someone')
    b.take_turn(7, 'shane')
    b.take_turn(2, 'someone')
    b.take_turn(7, 'shane')
    b.take_turn(3, 'someone')
    b.take_turn(7, 'shane')
    b.take_turn(4, 'someone')
    b.take_turn(7, 'shane')
    b.take_turn(5, 'someone')
