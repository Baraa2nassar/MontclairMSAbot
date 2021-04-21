# -*- coding: utf-8 -*-
'''
Author: David J. Morfe and Baraa Nassar
Application Name: Montclair MSA bot
Functionality Purpose: a bot that verifies poeple on discord and does smaller command tasks
Version: 
'''
RELEASE = "v0.2.3 - 4/20/2021 (DEV)"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import discord
import asyncio
from email.message import EmailMessage
import re, os, sys, time, json, smtplib, datetime
from config import *
from tools import *
import config
from key import *
from discord.ext import commands
#from discord_slash import SlashCommand, SlashContext

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = '/', intents=intents)  # add the intents= part to your existing constructor call
client = discord.Client(intents=intents)

RUN_TIME = datetime.datetime.now()
LAST_MODIFIED = RUN_TIME.strftime("%m/%d/%Y %I:%M %p")


'''
from discord.ext import commands
bot = commands.Bot("!")
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
'''

#Organize code


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

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "/cmds for commands)"))
    #guild = client.get_guild(SERVER_ID)
    #print (guild.members[1]) for none member debuging 
    print("We have logged in as {0.user}".format(client))
    refresh = []

#reaction roles adds a role once you click the emoji

@client.event
async def on_raw_reaction_add(playload):
    message_id = playload.message_id
    if message_id == 834201348030988328:
        guild_id = playload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if playload.emoji.name == "quran":
            #print ("thumbs up")
            role = discord.utils.get(guild.roles, name = 'Quran Circle')
            if role is not None:
                member = discord.utils.find(lambda m : m.id == playload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                else:
                    print ("member not found")
            else: 
                print ("role not found")
        if playload.emoji.name == "halaqa":
            role = discord.utils.get(guild.roles, name = "Brothers' Halaqa")
            if role is not None:
                member = discord.utils.find(lambda m : m.id == playload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)

#when removing the emoji, it removes the role with it

@client.event
async def on_raw_reaction_remove(playload):
    message_id = playload.message_id
    if message_id == 834201348030988328: #brother reaction-role channel
        guild_id = playload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if playload.emoji.name == "quran":
            role = discord.utils.get(guild.roles, name = 'Quran Circle')
            if role is not None:
                member = discord.utils.find(lambda m : m.id == playload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                else:
                    print ("member not found")
            else: 
                print ("role not found")
        if playload.emoji.name == "halaqa":
            role = discord.utils.get(guild.roles, name = "Brothers' Halaqa")
            if role is not None:
                member = discord.utils.find(lambda m : m.id == playload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role) 

#on messeges commands 
@client.event
async def on_message(message):
    if message.author == client.user:
        return -1;    

#/add gives a role depending where the user is. 
    if message.content.startswith('/add'): 
        
        if check_admin(message):
            user_id = re.search("\d{5,}", message.content)
            print ("user_id is:", user_id)
            #print(user_id)                
            if user_id:
                guild = client.get_guild(SERVER_ID)
                member = guild.get_member(int(user_id.group())) #they changed the .get_member
                #print ("member is", member) # to just check if it will return non or not; debuging
                sibling,rm_role = get_sibling_role(member)              
                role = discord.utils.get(client.get_guild(SERVER_ID).roles, name= f"{sibling}")
                brother = discord.utils.get(client.get_guild(SERVER_ID).roles, name= "Brother Waiting Room")
                print ( "role is", role)

                await member.add_roles(role)
                await member.remove_roles(rm_role)
                siblinghood = get_sibling(sibling)
                channel = client.get_channel(siblinghood.general)
                await channel.send("<@!" + user_id.group() + "> *has* ***officially*** *joined the Montclair MSA Discord! Welcome your " + sibling + "!*")
            else:
                await message.channel.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
                await message.delete(delay=300)

#/say lets the bot repeats what you say 
    if message.content.startswith("/say"): 
      if (message.author.id !=670325339263860758): #if not Baraa
      #to prevent anyone from repearting any bad language
        if re.search(r"\b(retard|ass|fuck|shit|ass|hell|pussy?|fucker|dick|nigger|bitch|bitch|nig|damn|prick|nigga)s?\b", str(message.content).lower()): # No Bad Language/Cussing
            await message.channel.send("I do not speak bad language sir",delete_after=10)
            await message.delete(delay=1)
        else:
          await message.channel.send(message.content.replace ("/say","")+ "\n> ||sent by "+message.author.mention+'||')
          await message.delete(delay=1)   
    if (message.content.startswith("/say")) and (message.author.id == (670325339263860758)): #this removes the tag if Baraa is the one who speaks
      await message.channel.send(message.content.replace ("/say",""))
      await message.delete(delay=1)

#/version shows the current version number with the date of the bot whether on the cloud or local
    if message.content.lower().startswith('/version'):
        if message.author.id == 670325339263860758 or 233691753922691072 : #if baraa or jake
        #if message.author.id in DEVS:
            await message.channel.send(f"`{RELEASE} | {LAST_MODIFIED}`")

#/cmds or help command to present all accessible commands       
    if (message.content.startswith("/cmds")): 
        #await message.channel.send(("hello world"))
        #embed = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        embed = discord.Embed(title = "",desctiption = "this is desctiption",color=0x461111)
        #embed.set_footer(text="this is a footer")
        embed.set_author(name = "Montclair MSA Bot Commands:",icon_url="https://cdn.discordapp.com/attachments/803103105406992415/829141943417962516/Circle_msa_Logo.png")
        #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/803103105406992415/829141943417962516/Circle_msa_Logo.png")
        embed.add_field(name="/verify",value='verifies users',inline=False)
        embed.add_field(name="/add",value='addes users </add><@username>',inline=False)
        embed.add_field(name="/suggest",value="let's see if agree with your suggestion on #feedback",inline=False)
        embed.add_field(name="/say ",value='the power of the bot repeating what you want',inline=False)
        embed.add_field(name="say my name",value='it says your name',inline=False)
        embed.add_field(name="as",value='Assalamualaikum Warahmatullahi Wabarakatuh',inline=False)
        embed.add_field(name="ws",value='waalaikumsalam warahmatullahi wabarakatuh',inline=False)
        await message.channel.send(embed=embed)

#say my name tags your user name
    if "say my name" == message.content.lower():
          await message.channel.send((message.author.mention))

#/suggest lets you suggest any ideas and makes an emoji poll
    if message.content.startswith("/suggest"):
        if message.channel.id == 785554461367468073:#suggestion channel
          thumbsUp = '\N{THUMBS UP SIGN}' #thumbs up emoji
          thumbsDown = "\U0001F44E" #thumbs down emoji
          await message.add_reaction(thumbsUp)
          await message.add_reaction(thumbsDown)

# No Bad Language/Cussing
    if re.search(r"\b(retard|ass|fuck|shit|ass|pussy?|fucker|dick|nigger|bitch|bitch|nig|damn|prick|nigga)s?\b", str(message.content).lower()): 
            await message.channel.send("https://gyazo.com/45ad780b2d98f884f00273e3dc0db6cc", delete_after=20)
            await message.delete(delay=1)
#greetings
    if "as" == message.content:
        await message.channel.send("Assalamualaikum Warahmatullahi Wabarakatuh")        
    if "ws" == message.content.lower():
        await message.channel.send("Walaikum Assalam Wa Rahmatullahi Wa Barakatuh")

#special commands
    if "/baraa" in message.content.lower(): # baraa
        if message.author.id == 670325339263860758:
          await message.channel.send("very well inshAllah")

    # General help commands Commands
    '''if message.content.startswith('/help'): # Help command
        with open("cmds.md") as f:
            cmds = f.read()
        await message.channel.send("__**MontclairMSA Commands:**__```CSS\n" + cmds + "```")'''

#Send to alternate announcement channel
    if listen_announce(message): 
        announce_channel = listen_announce(message)
        channel = client.get_channel(announce_channel)
        await channel.send(message.content) 

#verifies users using a sent code to their email that is randomly generated, they have to put it back to get a role
    if listen_verify(message): # Verify command
        ucid, gender = listen_verify(message)
        #error handler
        if not re.search(r"^[a-zA-Z]{2,}\d{0,}$", ucid) or \
           not re.search(r"(Brother|Sister)", gender) or \
           not re.search(r"^/verify ", str(message.content)):
            await message.channel.send("**Invalid command! Please make sure you're typing everything correctly.**", delete_after=25)
            await message.delete(delay=300)
        elif re.search(r"\d{8}", message.content):#another error handler
            await message.channel.send("**Invalid command! NOT your student ID, use your UCID!**", delete_after=25) #UCID is similar to NEST in Montclair
            await message.delete(delay=300)
        else:
            email_addr = f"{ucid}@montclair.edu"; ucid = ucid.lower()
            vCode = send_email(email_addr); ID = message.author.id
            with open("verify.txt", 'a') as f:
                f.write(f"{vCode} {email_addr} {ID} {gender}\n")
            temp = await message.channel.send(f"**We've sent a verification code to your email at** ___{email_addr}___**, please copy & paste it below.**", delete_after=300)
            await message.delete(delay=300)
            try:
                await asyncio.wait_for(check_verify(f"{vCode} {email_addr}", message, temp), timeout=900) # Purge messages when record is removed from 'verify.txt' otherwise purge in 15 minutes
            except asyncio.TimeoutError:
                try:
                    await message.delete(); await temp.delete()
                except discord.errors.NotFound:
                    pass
                edit_file("verify.txt", f"{vCode} {email_addr} {ID} {gender}")
                
    elif listen_code(message): # Listen for 4-digit code on the montclair MSA #verify
        eCode = listen_code(message)
        if eCode:
            with open("verify.txt") as f:
                lines = f.readlines(); flag = True
                if len(lines) != 0:
                    for line in lines:
                        lst = line.strip('\n').split(' ')
                        if lst[0] == eCode.group() and lst[2] == str(message.author.id): # Verify code
                            edit_file("verify.txt", line.strip('\n'))
                            role = discord.utils.get(client.get_guild(SERVER_ID).roles,
                                                     name=f"{lst[3]}s Waiting Room")
                            await message.author.add_roles(role); flag = False
                            sibling = get_sibling(lst[3])

                            nName = get_name(lst[1]) # New Nick Name
                            await message.delete(); flag = False
                            try:
                                if nName != None: # Re-name user
                                    await message.author.edit(nick=str(nName))
                                else:
                                    nName = lst[1]
                                    await message.author.edit(nick=str(nName))
                            except errors.Forbidden:
                                print("Success!\n", nName)
                                
                            channel = client.get_channel(sibling.wait) # montclair MSA #general
                            await channel.send(f"@here ***" + message.author.mention + "***" + " *has joined the montclair MSA Discord!*")
                        else:
                            await message.delete(delay=60)
                    if flag:
                        temp = await message.channel.send("**Invalid code! Who a u?!**")
                        await temp.delete(delay=60)
    else: # Delete every other message in #verify in 5 min.
        if message.channel.id == VERIFY_ID:
            if re.search(r"^[a-zA-Z]{2,4}\d{0,4}$", message.content):
                await message.channel.send("**Invalid command! Read instructions above and use /verify please!**", delete_after=25)
            await message.delete(delay=300)

    # Sisters Exclusive Commands

    # Brothers Exclusive Commands
BOT = os.getenv("BOT_SECRET", bot_pass())
token = BOT
client.run(token)

##client.logout()
##client.close()
##print("We have logged out of bot client")
