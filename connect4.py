#!/usr/bin/env python

from sopel.module import commands, rule
from sopel.formatting import color, colors
from random import choice

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
