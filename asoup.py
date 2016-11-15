#!/usr/bin/env python

from sopel.module import commands
from time import sleep
from string import ascii_uppercase
from random import sample, choice
from collections import Counter


def setup(bot):
    # take all uppercase letters apart from those specified
    abc = [i for i in ascii_uppercase if i not in 'XYZ']
    bot.memory['asoup'] = {'active': False, 'abc': abc}


# handler function to start game or submit depending on where command is run
@commands('asoup')
def handler(bot, trigger):
    if not trigger.is_privmsg:
        start_game(bot, trigger)
    else:
        asoupmit(bot, trigger)


# function to start the game
def start_game(bot, trigger):
    asoup = bot.memory['asoup']

    # if game is already running then say so and quit
    if asoup['active']:
        bot.say('Game is already running')
        return

    asoup['active'] = True
    # store the originating channel so the bot knows where to talk
    asoup['chan'] = trigger.sender
    # stores for the submissions and votes
    asoup['submissions'] = {}
    asoup['votes'] = {}

    # round 1 logic
    asoup['round'] = 1
    # create the acro from 3-5 letters from the allowed set
    asoup['acro'] = ''.join(sample(asoup['abc'], choice((3, 4, 5))))
    bot.say('Alphabet soup started!')
    bot.say('Acro: {}'.format(asoup['acro']))
    bot.say('Send your acros!')
    bot.say('(e.g. /msg {} .asoup poo bum tits)'.format(bot.nick))
    sleep(60)

    # round 2 logic
    asoup['round'] = 2
    # if no one submitted then end the game
    if not asoup['submissions']:
        bot.say('No one submitted...good job.')
        asoup['active'] = False
        return
    bot.say('Submission period over! Choose your winner!')
    bot.say('e.g. /msg {} .asoup 1'.format(bot.nick))
    # convert the submissions dict to a list of tuples
    asoup['submissions'] = list(asoup['submissions'].items())
    for n, i in enumerate(asoup['submissions'], start=1):
        bot.say('{}: {}'.format(n, i[1]))
    sleep(60)

    bot.say('Voting period over!')
    # if no one voted then end the game
    if not asoup['votes']:
        bot.say('No one voted...great.')
        asoup['active'] = False
        return
    # counter class to tally the votes
    c = Counter(int(i) - 1 for i in asoup['votes'].values())
    # take the winner(s) using the votes and submissions lists
    winners = [asoup['submissions'][i[0]] for i in c.items()
               if i[1] == max(c.values())]
    if len(winners) == 1:
        bot.say('The winner is:')
    else:
        bot.say('The winners are:')
    for i in winners:
        bot.say('{1} ({0})'.format(*i))

    # mark the game as inactive once ended
    asoup['active'] = False


# submit function (acros and votes)
def asoupmit(bot, trigger):
    asoup = bot.memory['asoup']

    # if the game isn't active then say so and finish
    if not asoup['active']:
        bot.say('game is not active')
        return

    msg = trigger.group(2)

    # determine logic based on the round number
    if asoup['round'] == 1:
        # if the submitted acro doesn't match the given, then return
        if ''.join(i[0] for i in msg.split()).upper() != asoup['acro']:
            bot.say('This doesn\'t match the acro')
            return
        bot.say('acro accepted!')
        # add the submitted acro to a dict with the user as key (so only
        # one submission is allowed per user)
        asoup['submissions'][trigger.nick] = msg
    else:
        # if the vote is either not numeric or doesn't match any submission,
        # then say so and finish
        if not msg.isdigit() and int(msg) > len(asoup['submissions']):
            bot.say('Vote by sending the number of the submission')
            return
        # if the user voted for their own acro then let them know and finish
        if asoup['submissions'][int(msg) - 1][0] == trigger.nick:
            bot.say('You can\'t vote for your own acro!')
            return
        bot.say('Vote accepted')
        # add vote to dict, using the location in the list as the identifier
        asoup['votes'][trigger.nick] = int(msg) - 1
