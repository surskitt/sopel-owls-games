#!/usr/bin/env python

from sopel.module import commands, rule
from sopel.formatting import color, colors
from random import choice

class Board:
    def __init__(self):
        self.board = [[0]*7 for i in range(6)]

    def addpiece(self, col_index, player):
        col = list(zip(*self.board))[col_index]

        row_index = 6 - col[::-1].index(0) - 1

        self.board[row_index][col_index] = player

    def printboard(self):
        print(self.board)
        for i in self.board:
            print ' '.join(str(j) for j in i)


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

c = ['○', color('●', colors.BLUE), color('●', colors.RED)]

@commands('connect4')
def connect4(bot, trigger):
    board = [[choice(c) for j in range(7)] for i in range(6)]

    for i in board:
        bot.say(' '.join(i))
