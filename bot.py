import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
from random import seed
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
async def paranoiaFunc(channelID, msg):
    holdStr = ""
    channel = client.get_channel(channelID)
    try:
        voiceBot = await channel.connect()
    except discord.errors.ClientException:
        print("already connected")
    while holdStr != "N":
        holdStr = ""
        memberIDs = []
        for member in channel.members:
            if member.id != client.user.id:
                memberIDs.append(member.id)
        unmutedUsers = len(memberIDs)
        index = randint(0,len(memberIDs)-1)
        await msg.channel.send("Muting users")
        while(unmutedUsers > 2):
            index = randint(0,len(memberIDs)-1)
            if not msg.channel.guild.get_member(memberIDs[index]).voice.deaf:
                await msg.channel.guild.get_member(memberIDs[index]).edit(deafen = True)
                unmutedUsers = unmutedUsers - 1
        await msg.channel.send("Ask the question and type \"asked\" when done")
        while holdStr != "asked":
            holdStr = await client.wait_for('message')
            holdStr = holdStr.content
        await msg.channel.send("Unmuting users")
        for member in memberIDs:
            if msg.channel.guild.get_member(memberIDs[index]).voice.deaf:
                await msg.channel.guild.get_member(member).edit(deafen = False)
        await msg.channel.send("Flipping the coin")
        seed(int(time.time()*1000.0))
        value = bool(randint(0,1))
        time.sleep(3)
        if value:
            await msg.channel.send("Fess up!")
        else:
            await msg.channel.send("Youre safe this time")
        await msg.channel.send("Another round? (type \"Y\" for yes, \"N\" for no)")
        while holdStr != "Y" and holdStr != "N":
            holdStr = await client.wait_for('message')
            holdStr = holdStr.content
    await voiceBot.disconnect()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        if "paranoia" in message.content:
            for channel in message.channel.guild.voice_channels:
                for member in channel.members:
                    if member.name == message.author.name:
                        if len(channel.members) > 2:
                            await paranoiaFunc(channel.id, message)
                        else:
                            await message.channel.send("Not enough members in channel")
            

client.run(TOKEN)