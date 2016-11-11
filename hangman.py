#!/usr/bin/env python

from random import choice
from sopel.module import commands, rule
import os.path


def setup(bot):
    bot.memory['hangman'] = {'active': False}


@commands('hangman')
def start_game(bot, trigger):
    if bot.memory['hangman']['active']:
        bot.say('Game is already running')
        return

    bot.memory['hangman']['active'] = True

    basepath = os.path.dirname(__file__)
    words_file = os.path.abspath(os.path.join(basepath, 'hangman_words.txt'))
    with open(words_file) as f:
        bot.memory['hangman']['word'] = choice(f.readlines()).strip()

    bot.memory['hangman']['curr'] = '_' * len(bot.memory['hangman']['word'])
    bot.memory['hangman']['wrong'] = 0

    bot.say('Hangman started!')
    bot.say(bot.memory['hangman']['curr'])


def draw_man(x):
    y = 7-x
    return ('{}>--->{};_;'.format(' ' * x, ' ' * y))


@rule('^[a-z]$')
def handle_game(bot, trigger):
    if not bot.memory['hangman']['active']:
        return

    word, curr = bot.memory['hangman']['word'], bot.memory['hangman']['curr']

    g = trigger.args[1]
    curr = ''.join(g if g == i else j for i, j in zip(word, curr))
    bot.memory['hangman']['curr'] = curr

    if '_' not in curr:
        bot.say('You win!')
        bot.say('The word was {}!'.format(word))
        bot.memory['hangman']['active'] = False
        return

    if g not in word:
        bot.memory['hangman']['wrong'] += 1
        if bot.memory['hangman']['wrong'] < 7:
            bot.say(draw_man(bot.memory['hangman']['wrong']))
        else:
            bot.say(' ' * 7 + '>--->X_X')
            bot.say('Game over!')
            bot.say('The word was {}'.format(word))
            bot.memory['hangman']['active'] = False
    else:
        bot.say(bot.memory['hangman']['curr'])
