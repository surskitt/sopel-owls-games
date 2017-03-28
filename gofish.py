#!/usr/bin/env python

from sopel.module import commands
import random
from itertools import cycle


class Player():
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.pairs = 0

    def fish(self, card):
        if card == 0:
            return
        if card not in self.hand:
            self.hand.append(card)
        else:
            self.pairs += 1
            self.hand.remove(card)

    def fished(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        else:
            return 0

    def get_hand(self):
        return sorted(self.hand)


class Deck():
    def __init__(self):
        self.cards = shuffle('A23456789XJQK'*2)

    def fish(self):
        if self.cards:
            return self.cards.pop()
        else:
            return 0

    def get_size(self):
        return len(self.cards)


def setup(bot):
    bot.memory['gofish'] = {
        'active': False
    }


@commands('gofish')
def gofish(bot, trigger):
    if not bot.memory['gofish']['active']:
        start(bot, trigger)
    else:
        fish(bot, trigger)


def start(bot, trigger):
    if not trigger.group(2):
        bot.say('Error: choose a user to play against')
        bot.say('.gofish <user1> {<user2> ...}')
        return

    players = {i: Player(i) for i in
               set([str(trigger.nick)] + trigger.group(2).split())}

    if not all([i in bot.users for i in players]):
        bot.say('Not all users are online')
        return

    if len(set(players)) < 2:
        bot.say('You can\'t play against yourself!')
        return

    bot.memory['gofish']['deck'] = Deck()

    # deal cards
    for player in players.values():
        for i in range(7 if len(players) == 2 else 5):
            player.fish(bot.memory['gofish']['deck'].fish())

    bot.say('Game started with {}'.format(', '.join(players)))
    bot.memory['gofish']['active'] = True

    bot.memory['gofish']['players'] = players
    bot.memory['gofish']['tracker'] = cycle(shuffle(players.values()))
    bot.memory['gofish']['current'] = next(bot.memory['gofish']['tracker'])
    gofishscores(bot, trigger)

    for player in players:
        gofishcards(bot, player)

    bot.say('{}\'s go!'.format(bot.memory['gofish']['current'].name))
    bot.say('To play: .gofish <player> <card>')


def fish(bot, trigger):
    mem = bot.memory['gofish']

    if trigger.nick != mem['current'].name:
        return

    if not trigger.group(2) or len(trigger.group(2).split()) < 2:
        bot.say('To play: .gofish <player> <card>')
        return

    player, card = trigger.group(2).split()
    card = card.upper()

    if player not in mem['players']:
        bot.say('{} isn\'t in the game! Pick again'.format(player))
        return

    if card not in 'A23456789XJQK':
        bot.say('{} isn\'t a card! Pick again from A23456789JQK'.format(card))
        return

    if trigger.nick == player:
        bot.say('Can\'t fish from yourself!')
        return

    fished = mem['players'][player].fished(card)

    if fished:
        mem['current'].fish(card)
        checkwin(bot, trigger)
        if not mem['active']:
            return
        if mem['deck'].get_size() or mem['current'].get_hand():
            bot.say('{} had {}! Go again!'.format(player, card))
            bot.say('{} cards left in deck'.format(mem['deck'].get_size()))
            if not mem['players'][player].get_hand():
                bot.say('Out of cards, drawing 5 more')
                for i in range(5):
                    mem['current'].fish(mem['deck'].fish())
        else:
            bot.say('No cards left and none in the deck')
            mem['current'] = next(mem['tracker'])
    else:
        bot.say('{} didn\'t have {}! Go fish!'.format(player, card))
        mem['current'].fish(mem['deck'].fish())
        bot.say('{} cards left in deck'.format(mem['deck'].get_size()))
        mem['current'] = next(mem['tracker'])
    while not mem['current'].get_hand():
        mem['current'] = next(mem['tracker'])
    bot.say('{}\'s turn!'.format(mem['current'].name))
    gofishcards(bot, mem['current'].name)


@commands('gfcards')
def gofishcards(bot, trigger=None):
    players = bot.memory['gofish']['players']
    player = getattr(trigger, 'nick', trigger)
    cards = sorted(players[player].get_hand())

    bot.say('Your cards: {}'.format(', '.join(cards)), player)


@commands('gfend')
def gofishend(bot, trigger):
    bot.say('Game over!')
    bot.memory['gofish']['active'] = False


@commands('gfscores')
def gofishscores(bot, trigger):
    players = bot.memory['gofish']['players']

    bot.say('Current scores:')
    for player in sorted(players.values(), key=lambda x: x.pairs, reverse=True):
        bot.say('{}: {}'.format(player.name, player.pairs))


def checkwin(bot, trigger):
    mem = bot.memory['gofish']
    players, deck = mem['players'], mem['deck']
    if deck.get_size() and not any(i.get_hand() for i in players.values()):
        gofishend()
        gofishscores(bot, trigger)
        winner = max(players.values(), key=lambda x: x.pairs)
        bot.say('{} is the winner!'.format(winner.name))


def shuffle(l):
    return random.sample(list(l), len(l))
