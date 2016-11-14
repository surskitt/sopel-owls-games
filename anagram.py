#!/usr/bin/env python

from random import choice, sample
from sopel.module import commands, rule
import os.path


def setup(bot):
    bot.memory['anagram'] = {'active': False}


@commands('anagram')
def start_game(bot, trigger):
    if bot.memory['anagram']['active']:
        bot.say('Game is already running')
        bot.say('The word is {}'.format(bot.memory['anagram']['shuffled']))
        return

    bot.memory['anagram']['active'] = True

    basepath = os.path.dirname(__file__)
    words_file = os.path.abspath(os.path.join(basepath, 'words.txt'))
    with open(words_file) as f:
        word = choice(f.readlines()).strip()

    shuffled = ''.join(sample(word, len(word)))

    bot.say('Guess the word!')
    bot.say(shuffled)

    bot.memory['anagram']['word'] = word
    bot.memory['anagram']['shuffled'] = shuffled


@rule('^[a-z]+$')
def handle_game(bot, trigger):
    if not bot.memory['anagram']['active']:
        return

    guess, word = trigger.args[1], bot.memory['anagram']['word']

    if guess == word:
        bot.say('Correct! The word was {}'.format(word))
        bot.memory['anagram']['active'] = False
