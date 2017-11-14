#!/usr/bin/env python

from sopel.module import commands, require_chanmsg
from sopel.formatting import color, colors
from random import choice
import time

def setup(bot):
    for channel in bot.config.core.channels:
        bot.memory[channel] = {'connect4': None}

class Board:
    def __init__(self, player, bot, trigger):
        self.active = True
        self.board = [[0]*6 for i in range(7)]
        self.players = {1: player}
        self.active_player = 1
        self.colours = {1: colors.RED, 2: colors.BLUE}

        self.bot, self.trigger = bot, trigger

        self.bot.say('{} wants to play connect4! .connect4 to join'.format(player))

    def add_player(self, player):
        if len(self.players) > 1:
            self.bot.say('There are already two players')
            return

        if self.players[1] == player:
            self.bot.say('You\'re already playing...')
            return

        self.players[2] = player
        self.bot.say('Game started between {} and {}'.format(*self.players.values()))
        self.print_board()
        self.bot.say(color('{}\'s go!'.format(self.players[1]), self.colours[1]))
        self.bot.say('(.connect4 COLUMN_NUMBER to play)')

    def col_full(self, col):
        return 0 not in self.board[col]

    def add_piece(self, col, player):
        self.board[col][self.board[col].index(0)] = player

        self.bot.say('Piece added')
        self.print_board()

    def rows(self):
        return list(zip(*self.board))[::-1]

    def diagonals(self):
        h, w = len(self.board), len(self.board[0])
        return [[self.board[h - p + q - 1][q]
                for q in range(max(p-h+1, 0), min(p+1, w))]
                for p in range(h + w - 1)]

    def antidiagonals(self):
        h, w = len(self.board), len(self.board[0])
        return [[self.board[p - q][q]
                for q in range(max(p-h+1,0), min(p+1, w))]
                for p in range(h + w - 1)]


    def print_board(self):
        pieces = {0: '○', 1: color('●', colors.RED), 2: color('●', colors.BLUE)}

        for i in [' '.join(pieces[j] for j in i) for i in self.rows()]:
            self.bot.say(i + ' '*choice(range(10)))

    def check_win(self):
        directions = (self.board + self.rows() + self.diagonals() +
                      self.antidiagonals())
        check = [''.join(str(j) for j in i) for i in directions]

        return any(any(j in i for j in ['1111', '2222']) for i in check)

    def check_boardfull(self):
        return not any(0 in i for i in self.board)

    def take_turn(self, col, player):
        if col not in [str(i) for i in range(1, 8)] or not col.isdigit():
            self.bot.say('Column needs to be between 1 and 7')
            return

        col = int(col) - 1

        if len(self.players) < 2:
            self.bot.say('There needs to be two players before starting')
            return

        if player not in self.players.values():
            self.bot.say('You aren\'t playing...')
            return

        if self.players[self.active_player] != player:
            self.bot.say('It is not your go')
            return

        if self.col_full(col):
            self.bot.say('No space in column')
            return

        self.add_piece(col, self.active_player)

        if self.check_win():
            self.bot.say('{} won!'.format(self.players[self.active_player]))
            self.active = False
            return

        if self.check_boardfull():
            self.bot.say('Board full, game over!')
            self.active = False
            return

        self.active_player = [1,2][self.active_player == 1]

        player_name = self.players[self.active_player]
        player_colour = self.colours[self.active_player]

        self.bot.say(color('{}\'s go!'.format(player_name), player_colour))

@require_chanmsg
@commands('connect4')
def handler(bot, trigger):
    if bot.memory[trigger.sender]['connect4']:
        if trigger.group(2):
            handle_turns(bot, trigger, trigger.group(2))
        else:
            handle_players(bot, trigger)
    else:
        board = Board(trigger.nick, bot, trigger)
        bot.memory[trigger.sender]['connect4'] = board

        time.sleep(600)
        if len(board.players) < 2:
            bot.say('No one accepted the connect4 challenge, game cancelled.')
            bot.memory[trigger.sender]['connect4'] = None

def handle_players(bot, trigger):
    board = bot.memory[trigger.sender]['connect4']

    board.add_player(trigger.nick)

def handle_turns(bot, trigger, col):
    board = bot.memory[trigger.sender]['connect4']

    board.take_turn(col, trigger.nick)

    if not board.active:
        bot.memory[trigger.sender]['connect4'] = None

if __name__ == '__main__':
    b = Board('shane')

    b.add_player('someone')

    b.take_turn(2, 'shane')
    b.take_turn(3, 'someone')
    b.take_turn(3, 'arse')
