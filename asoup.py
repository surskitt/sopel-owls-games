#!/usr/bin/env python

from sopel.module import commands, require_privmsg
from time import sleep
from string import ascii_uppercase as abc
from random import sample, choice


def setup(bot):
    bot.memory['asoup'] = {'active': False}


@commands('asoup')
def start_game(bot, trigger):
    if bot.memory['asoup']['active']:
        bot.say('Game is already running')
        return

    asoup = bot.memory['asoup']

    asoup['active'] = True
    asoup['chan'] = trigger.sender
    bot.say('asoup started')

    asoup['round'] = 1
    asoup['submissions'] = []
    asoup['acro'] = ''.join(sample(abc, choice((3, 4, 5))))
    bot.say('Alphabet soup started!')
    bot.say('Acro: {}'.format(asoup['acro']))
    sleep(30)

    asoup['round'] = 2
    if not asoup['submissions']:
        bot.say('No one submitted...good job.')
        asoup['active'] = False
        return
    bot.say('Submission period over! Choose your winner!')
    for n, i in enumerate(asoup['submissions'], start=1):
        bot.say('{}: {}'.format(n, i))
    asoup['scores'] = {}
    sleep(10)

    winners = [asoup['submissions'][int(i) - 1]
               for i in asoup['scores']
               if asoup['scores'][i] == max(asoup['scores'].values())]

    bot.say('Submission period over!')
    if len(winners) == 1:
        bot.say('The winner is:')
    else:
        bot.say('The winners are:')
    for i in winners:
        bot.say(i)

    asoup['active'] = False


@require_privmsg
@commands('asoupmit')
def asoupmit(bot, trigger):
    asoup = bot.memory['asoup']

    if not asoup['active']:
        bot.say('game is not active')
        return

    msg = trigger.group(2)

    if asoup['round'] == 1:
        if ''.join(i[0] for i in msg.split()).upper() != asoup['acro']:
            bot.say('This doesn\'t match the acro')
            return
        asoup['submissions'].append(msg)
    else:
        if not msg.isdigit() and int(msg) > len(asoup['submissions']):
            bot.say('Vote by sending the number of the submission')
        asoup['scores'][msg] = asoup['scores'].get(msg, 0) + 1
