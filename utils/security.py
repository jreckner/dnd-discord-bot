from discord.ext import commands

import config

def is_owner(ctx):
    return ctx.message.author.id == config.owner
