#!/usr/bin/env python

from sopel.module import commands, require_privmsg
from time import sleep
from string import ascii_uppercase as abc
from random import sample, choice
from collections import Counter


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
    asoup['scores'] = {}
    asoup['submissions'] = {}
    asoup['votes'] = {}
    bot.say('asoup started')

    asoup['round'] = 1
    asoup['acro'] = ''.join(sample(abc, choice((3, 4, 5))))
    bot.say('Alphabet soup started!')
    bot.say('Acro: {}'.format(asoup['acro']))
    bot.say('Send your acros!')
    bot.say('(e.g. /msg {} .asoupmit poo bum tits)'.format(bot.nick))
    sleep(20)

    asoup['round'] = 2
    if not asoup['submissions']:
        bot.say('No one submitted...good job.')
        asoup['active'] = False
        return
    bot.say('Submission period over! Choose your winner!')
    bot.say('e.g. /msg {} .asoupmit 1'.format(bot.nick))
    asoup['submissions'] = [{i: asoup['submissions'][i]}
                            for i in asoup['submissions']]
    for n, i in enumerate(asoup['submissions'], start=1):
        bot.say('{}: {}'.format(n, list(i.values())[0]))
    sleep(10)

    bot.say('Voting period over!')
    if not asoup['votes']:
        bot.say('No one voted...great.')
    c = Counter(asoup['votes'].values())
    winners = [asoup['submissions'][int(i[0])-1] for i in c.items()
               if i[1] == max(c.values())]
    if len(winners) == 1:
        bot.say('The winner is:')
    else:
        bot.say('The winners are:')
    for i in winners:
        bot.say('{1} ({0})'.format(*list(i.items())[0]))

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
        asoup['submissions'][trigger.nick] = msg
    else:
        if not msg.isdigit() and int(msg) > len(asoup['submissions']):
            bot.say('Vote by sending the number of the submission')
            return
        asoup['votes'][trigger.nick] = msg
