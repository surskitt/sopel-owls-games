#!/usr/bin/env python

from sopel.module import commands
from time import sleep
from string import ascii_uppercase
from random import sample, choice
from collections import Counter


def setup(bot):
    abc = [i for i in ascii_uppercase if i not in 'XYZ']
    bot.memory['asoup'] = {'active': False, 'abc': abc}


@commands('asoup')
def handler(bot, trigger):
    if trigger.is_privmsg:
        asoupmit(bot, trigger)
    else:
        start_game(bot, trigger)


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

    asoup['round'] = 1
    asoup['acro'] = ''.join(sample(asoup['abc'], choice((3, 4, 5))))
    bot.say('Alphabet soup started!')
    bot.say('Acro: {}'.format(asoup['acro']))
    bot.say('Send your acros!')
    bot.say('(e.g. /msg {} .asoup poo bum tits)'.format(bot.nick))
    sleep(20)

    asoup['round'] = 2
    if not asoup['submissions']:
        bot.say('No one submitted...good job.')
        asoup['active'] = False
        return
    bot.say('Submission period over! Choose your winner!')
    bot.say('e.g. /msg {} .asoupmit 1'.format(bot.nick))
    asoup['submissions'] = list(asoup['submissions'].items())
    for n, i in enumerate(asoup['submissions'], start=1):
        bot.say('{}: {}'.format(n, i[1]))
    sleep(10)

    bot.say('Voting period over!')
    if not asoup['votes']:
        bot.say('No one voted...great.')
        return
    c = Counter(int(i) - 1 for i in asoup['votes'].values())
    winners = [asoup['submissions'][i[0]] for i in c.items()
               if i[1] == max(c.values())]
    if len(winners) == 1:
        bot.say('The winner is:')
    else:
        bot.say('The winners are:')
    for i in winners:
        bot.say('{1} ({0})'.format(*i))

    asoup['active'] = False


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
        bot.say('acro accepted!')
        asoup['submissions'][trigger.nick] = msg
    else:
        if not msg.isdigit() and int(msg) > len(asoup['submissions']):
            bot.say('Vote by sending the number of the submission')
            return
        if asoup['submissions'][int(msg) - 1][1] == trigger.nick:
            bot.say('You can\'t vote for your own acro!')
            return
        bot.say('Vote accepted')
        asoup['votes'][trigger.nick] = int(msg) - 1
