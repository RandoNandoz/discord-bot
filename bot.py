""" DISCORD BOT """
import asyncio
from distutils.util import strtobool
from random import randint
from os import environ
import discord
from discord.ext import commands

COMMAND_PREFIX = "~!"

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

USER_NICKNAME_ARRAY = []


@bot.command()
@commands.has_guild_permissions()
async def setnicknames(ctx: commands.Context, *args):
    if ctx.author == bot.user:
        return
    global USER_NICKNAME_ARRAY
    USER_NICKNAME_ARRAY.clear()
    USER_NICKNAME_ARRAY = list(map(str, args))
    print(f"Set USER_NICKNAME_ARRAY to: {USER_NICKNAME_ARRAY}")
    ctx.send(f"SUCCESS: Set the username list to {USER_NICKNAME_ARRAY}")


@bot.command()
@commands.has_guild_permissions()
async def iterateuser(ctx: commands.Context, user: str, interval: str, go_flag: str):
    """
    A command to change the user's name with the provided args,
    which is `user`, which is a mention of the user.
    The second arg is interval, which is how often to change the user's name.
    """
    # This prevents the bot from replying to itself, which causes problems (duh)
    if ctx.author == bot.user:
        return

    # When you mention a user, you actually mention their user ID,
    # which means we can get the user's ID by just mentioning them,
    # and then splicing off the arrows, the at symbol, and the exclamation point.
    user = user.replace("<", "")
    user = user.replace("@", "")
    user = user.replace(">", "")
    user = user.replace("!", "")
    user = int(user)

    member: discord.Member = discord.Guild.get_member(
        ctx.guild, user)

    if USER_NICKNAME_ARRAY is not None and USER_NICKNAME_ARRAY != list() and member is not None:
        ctx.send(f"Started.")
        while bool(strtobool(go_flag)):
            await member.edit(nick=USER_NICKNAME_ARRAY[randint(0, len(USER_NICKNAME_ARRAY) - 1)])
            print("Nickname changed...")
            await asyncio.sleep(int(interval))
    else:
        await ctx.send("Have you set a list of nicknames with `~!setnicknames`?")

bot.run(environ["DISCORD_TOKEN"])
