#!/usr/bin/env python

from sopel.module import commands
import requests


@commands('qod')
def qod(bot, trigger):
    r = requests.get('http://quotes.rest/qod.json')
    quote = r.json()['contents']['quotes'][0]
    out = '{} ({})'.format(quote['quote'], quote['author'])
    bot.say(out)
