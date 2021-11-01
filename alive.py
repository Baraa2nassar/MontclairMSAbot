# -*- coding: utf-8 -*-
'''
بسم الله
Author: David J. Morfe
Application Name: MSA-Bot
Functionality Purpose: An agile Discord Bot to fit any MSA's needs
'''

import re, os, sys, time
from key import *
from config import *
from tools import *
import discord
from discord.ext import commands
from discord.utils import get
from discord import Intents
from discord import File
from discord import Embed
from discord import Game
from discord import errors
import random


COMMAND_PREFIX='/'

intents = Intents.default()
intents.members = True # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=None, intents=intents)



class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self .stream, attr)
sys.stdout = Unbuffered(sys.stdout)

# Executes when bot begins running

@bot.event
async def on_ready():
   await bot.change_presence(activity = Game(name = "/cmds (For all cmds)"))
   print("We have logged in as {0.user} in {1}")
   whatDoUWant = (input("type if you want to\n -'channel message' \n -'edit' \n -'reply'\n -'emoji'\n -'embed'\n ==> "))

   if (whatDoUWant.lower() == "channel message"):
       try:
          chan = int(input("Enter Channel ID: "))
          channel = bot.get_channel(chan)
       except ValueError:
          print("Wrong type!")
          chan = 778053859536273459
          channel = bot.get_channel(chan)
          
       while True:
          reply = str(input("reply here: "))
          await channel.send(reply)
#----------------------------------------------------
   elif (whatDoUWant.lower() == "edit"):
       print ("ok\n")
       
       try:
           channel = bot.get_channel(int(input("Enter Channel ID: ")))
           message = await channel.fetch_message((int(input("Enter message ID: "))))
           con=str(input("the new content of the message is: "))
           await message.edit(content=f"{con}")
        
       except ValueError:
          print("Wrong type!")
          '''chan = 778053859536273459
          channel = bot.get_channel(chan)'''
 
   elif (whatDoUWant.lower() == "reply"):
       try:
           channel = bot.get_channel(int(input("Enter Channel ID: ")))
           message = await channel.fetch_message(int(input("Enter message ID: ")))
           #rep=
           await message.reply(str(input("reply here: ")))
        
       except ValueError:
          print("Wrong type!")
          '''chan = 778053859536273459
          channel = bot.get_channel(chan)'''
          
   elif (whatDoUWant.lower()=="emoji"):
         channel = bot.get_channel(int(input("Enter Channel ID: ")))
         message = await channel.fetch_message(int(input("Enter message ID: ")))
           #rep=
       #await message.reply(str(input("reply here: ")))
         thumbsDown = str(input("emoji: ")) #"\U0001F44E" #thumbs down emoji
         guild = bot.get_guild(SERVER_ID)
         member= guild.get_member(int(input("user ID: ")))
         removeOrAdd = str(input("do you want to 'remove' or 'add' the emoji: "))
         await message.add_reaction(thumbsDown) if removeOrAdd == 'add' else await message.remove_reaction(thumbsDown,member)          
         #await message.add_reaction(str(input("emoji: ")))
#sending an embed
   elif (whatDoUWant.lower()=="embed"):
         #embed = discord.Embed(color=0xFFD700)
         embed = discord.Embed(color = discord.Color.red())
         #CoolTitle=["Hear me out","You ready?"]
         CoolTitle = str(input("put a title "))
         channel = bot.get_channel(int(input("Enter Channel ID: ")))

         reply = str(input("reply here: "))
         #await channel.send(reply)

         embed.add_field(name=(CoolTitle), value=f"{reply}\n" , inline=False)
         # embed.add_field(name=random.choice(CoolTitle), value=f"{reply}\n [Jump to message]({url})" , inline=False)
         # channel_id = int(channel_id)
         # await channel.send(f"<@{user_id}>")
         await channel.send (embed=embed)

'''ideas'''    
#maybe we can in the future make it reply with an emoji too
#make the bot connect to a voice chat

# Standard MSA Bot Commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return -1;

# Bot Starting Point

BOT = os.getenv("BOT_SECRET", bot_pass())
token = BOT
bot.run(token)

'''
if __name__ == "__main__":
    token = BOT
    bot.run(token)
'''
##bot.logout()
##bot.close()
##print("We have logged out of bot")
