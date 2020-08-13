import os
import asyncio
from typing import List
from random import randint
import discord

# Represented in seconds, currently at 3600 seconds, which is an hour.
#
NicknameChangeInterval = 3600  # CHANGEME!!! CHANGEME!!! CHANGEME!!!

# The potential names for the user who uses `~!start` will have their name changed.
# The type of this array must be a string.
UserNickArray = [
    # Place the the potential names here, comma seperated.
    # e.g.
    # "Bob is a great man",
    # "Absolute legend",
    # "Alexa, play despacito"
]

UserToChangeNickArray = [
    # Enter user ids here, also comma seperated
    # e.g. (These are random user ids btw.)
    # 2224900345782567455,
    # 2224900608345567485,
    # 270904126974540956,
    # 232634536343643932
]

# This is the array of userids which will be considered immutable.
# The type of this array must be an int.
NoChangeArray = [
    # Enter user ids here, also comma seperated
    # e.g. (These are random user ids btw.)
    # 2224900345782567455,
    # 2224900608345567485,
    # 270904126974540956,
    # 232634536343643932
]
# Array for people who has a permission level above the bot's.
# The type of this array must also be an int.
UserPrivAboveBotArray = [
    # Enter user ids here, also comma seperated
    # e.g. (These are random user ids btw.)
    # 2224900345782567455,
    # 2224900608345567485,
    # 270904126974540956,
    # 232634536343643932
]

# Special UIDs for the "Special Array", ints only.
SpecialUIDArray = [
    # Enter user ids here, also comma seperated
    # e.g. (These are random user ids btw.)
    # 2224900345782567455,
    # 2224900608345567485,
    # 270904126974540956,
    # 232634536343643932
]

# Special names for the Special UIDs. Strings only.
SpecialUserNickArray = [
    # Place the the potential names here, comma seperated.
    # e.g.
    # "Bob is a great man",
    # "Absolute legend",
    # "Alexa, play despacito"
]


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, msg: discord.Message):
        # This prevents a recursive issue with the bot replying to itself.
        if msg.author == client.user:
            return

        if msg.content.startswith("~!start"):
            # TODO: Make this toggleable.
            # First checks whether the user has privs above the bot - usually the owner only.
            if msg.author not in UserPrivAboveBotArray:
                while True:
                    # Changes the username to something random in the UserNickArray
                    member: discord.Member = msg.author
                    await member.edit(nick=UserNickArray[randint(0, len(UserNickArray) - 1)])
                    print("Changing nickname...")
                    await asyncio.sleep(NicknameChangeInterval)

        if msg.content.startswith("~!execonspecial"):
            # TODO: Make this toggleable.
            while True:
                # Initializes a new empty array for the special array.
                memberArray = []
                # Iterates through the SpecialUIDArray for special user IDs.
                for i in range(len(SpecialUIDArray)):
                    # Then, for each id in the array, it gets the member with the id, and appends it to the memberArray.
                    memberArray.append(
                        (discord.Guild.get_member(msg.guild, SpecialUIDArray[i])))

                # For each user in the member array,
                for i in range(len(memberArray)):
                    # it edits the member's username to a random item in the SpecialUserNickArray.
                    await memberArray[i].edit(
                        nick=SpecialUserNickArray[
                            randint(0, len(SpecialUserNickArray) - 1)
                        ]
                    )
                    print("Changing nickname...")
                await asyncio.sleep(NicknameChangeInterval)

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # This prevents the user's name being changed, but instead being changed to the UserNickArray.
        if before.id in UserToChangeNickArray and before.id not in UserPrivAboveBotArray:
            # If the user's name is not the same, and their name is not equal to something in the array,
            # change it to a random item in the array.
            if after.nick != before.nick and after.nick not in UserNickArray:
                await after.edit(nick=UserNickArray[randint(0, len(UserNickArray) - 1)])
                print("Changing nickname...")
        elif before.id in SpecialUIDArray and after.id not in UserPrivAboveBotArray:
            # If the user's name is not the same, and their name is not equal to something in the array,
            # change it to a random item in the array.
            if after.nick != before.nick and after.nick not in UserPrivAboveBotArray:
                await after.edit(nick=SpecialUserNickArray[randint(0, len(SpecialUserNickArray) - 1)])
                print("Changing nickname...")
        # Checks whether the user is in the array of users forbidden from changing their nickname.
        elif before.id in NoChangeArray:
            if after.nick != before.nick:
                await after.edit(nick=before.nick)
                print("Changing nickname...")


# Logs into the discord API. The token should be an environment variable.
client = MyClient()
client.run(os.environ["DISCORD_TOKEN"])
