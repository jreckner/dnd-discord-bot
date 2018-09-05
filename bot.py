# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
# https://media.readthedocs.org/pdf/discordpy/rewrite/discordpy.pdf

import requests
from discord import Client, Colour, Embed, Game
from discord.ext import commands

import enc
import dnd5e
import config
from utils import security

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.PREFIX), description='')


@bot.command(
help='Lookup a D&D 5e Term in the PHB or DM',
brief='D&D 5e Search',
description='Lookup a D&D 5e Term in the PHB or DMG'
)
async def lookup(ctx, term: str):
    if len(term) >= 3:
        results_of_lookup = dnd5e.lookup_term(term)
        if results_of_lookup:
            embedded_results = Embed(color = Colour.green(), description = results_of_lookup)
            await ctx.send(embed=embedded_results)
            url = 'https://roll20.net/compendium/dnd5e/searchbook/?terms={0}'.format(term)
            r = requests.get(url, allow_redirects=False)
            if r.status_code == 302:
                embedded_ref = Embed(color = Colour.blue(), description = 'Online reference found: ' + r.headers['location'])
                await ctx.send(embed=embedded_ref)
        else:
            embedded_err = Embed(color = Colour.red(), description = 'search param yeilded no results in PHB or DMG index')
            await ctx.send(embed=embedded_err)
    else:
        embedded_err_len = Embed(color = Colour.red(), description = 'search param should be at least 3 characters')
        await ctx.send(embed=embedded_err_len)

@bot.command()
async def encounter(ctx):
    embedded_enc = Embed(color = Colour.dark_blue(), description = 'Random Encounter: \n' + enc.get_random_encounter())
    await ctx.send(embed=embedded_enc)

@bot.command(help='!')
async def prefix(ctx):
    embedded_prefix = Embed(color = Colour.red(), description = 'Commands Prefix: ' + config.prefix)
    await ctx.send(embed=embedded_prefix)

@bot.command()
async def info(ctx):
    embedded_info = Embed(color = Colour.gold(), description = 'Commands Prefix: ' + config.PREFIX + '\nVersion: ' + config.VERSION)
    await ctx.send(embed=embedded_info)

@bot.command(hidden=True)
@commands.check(security.is_owner)
async def exit(ctx):
    msg = 'Shutting down {0.author.mention}'.format(ctx.message)
    await ctx.author.send(msg)
    await bot.logout()

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if not message.author.bot:
        await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    pass

@bot.event
async def on_message_edit(before, after):
    pass

@bot.event
async def on_command(ctx):
    message = ctx.message
    print('User: {0.author.name}:{0.author.id}, Server: {0.author.guild.name}, Channel: {0.channel.name}, Command: [{0.clean_content}]'.format(message))

@bot.event
async def on_ready():
    print('Logged in as: ' + bot.user.name + '(' + str(bot.user.id) + ')')
    print('------')
    await bot.change_presence(activity=Game(name="Type !help for usage"))

bot.run(config.TOKEN)
