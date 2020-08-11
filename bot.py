import discord
import discord.ext
import asyncio
import os
from random import randint
userNickArray = [

]


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, msg: discord.Message):
        # This prevents a recursive issue with the bot replying to itself.
        if msg.author == client.user:
            return

        if msg.content.startswith("~!start"):
            while True:

                member: discord.Member = msg.author
                await member.edit(nick=userNickArray[randint(0, len(userNickArray) - 1)])
                print("Changing username...")
                await asyncio.sleep(3000)

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.id == 215994239920766977:
            if after.nick != before.nick and before.nick not in userNickArray:
                await after.edit(nick=userNickArray[randint(0, len(userNickArray) - 1)])
                print("Changing username..")


client = MyClient()
client.run(os.environ["DISCORD_TOKEN"])
