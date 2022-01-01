# -*- coding: utf-8 -*-
'''
Author: David J. Morfe and Baraa Nassar
Application Name: Montclair MSA bot
Functionality Purpose: a bot that verifies poeple on discord and does smaller command tasks
Version: 
'''
RELEASE = "v0.2.7 - 12/07/2021    (DEV)"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import discord
import asyncio
#from webserver import keep_alive
from email.message import EmailMessage
import re, os, sys, time, json, smtplib, datetime
from config import *
from tools import *
import config
from key import *
from time import *
from discord.ext import commands
#from discord_slash import SlashCommand, SlashContext

#need to change the instance from @client to @bot, so I can use the commands by defining the function
#need to add links commans

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = '/', intents=intents)  # add the intents= part to your existing constructor call
client = discord.Client(intents=intents)

RUN_TIME = datetime.datetime.now()
LAST_MODIFIED = RUN_TIME.strftime("%m/%d/%Y %I:%M %p")

#RELEASE += f" ({ENV})"

'''
from discord.ext import commands
bot = commands.Bot("!")
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
'''

#Organize code

#Prevent email from spam


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



def get_sibling_role(member):
    if member is None:
        return None

    #roles = member.roles; ret = None #<==there is an issue on this
    roles, ret = member.roles, None
    reaction_channel = ""

    for role in roles:
        if role.name == "Brothers Waiting Room":
            ret = ("Brother", role);break
        elif role.name == "Sisters Waiting Room":
            #reaction_channel = "<#773420851387301939>" #have to fix this and put one for sisters
            ret = ("Sister", role); break
        elif role.name == "Brother":
            ret = ("Brother", role);break
        elif role.name == "Sister":
            ret = ("Sister", role); break
    return ret

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "/cmds for commands)"))
    guild = client.get_guild(SERVER_ID)
    print (guild.members[1])
    print("We have logged in as {0.user}".format(client))
    #print (guild.members[1])
    refresh = []

# @client.event
# async def on_member_leave(member):
#     print("member has left a server.")

@client.event
async def on_raw_reaction_remove(playload):
    message_id = playload.message_id
    if message_id == 834201348030988328:
        guild_id = playload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if playload.emoji.name == "quran":
            print ("thumbs up")
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

        if playload.emoji.name == "🎓":
            role = discord.utils.get(guild.roles, name = "Alumni")
            if role is not None:
                member = discord.utils.find(lambda m : m.id == playload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role) 

@client.event
async def on_message(message):
  #baraa = message.author.id (670325339263860758):
    
    if message.content.startswith('/add')or  message.content.startswith('>add'): # Add user officially
        
        if check_admin(message):
            user_id = re.search(r"\d{5,}", message.content)
            #print ("user_id is:", user_id)
            #print(user_id)
                        
            if user_id:
                #guild_id = playload.guild_id
                #guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
                guild = client.get_guild(SERVER_ID)
                #print ("guild is", guild)
                #print("type guild is",type(guild))
                #print ("groupID", (int (user_id.group())))
                #print (guild.members[1])
                #print (member.roles)
                #print (client.get_guild(SERVER_ID).roles)#this prints all the roles in the server
                #print (guild.members)
                #async for guild in client.fetch_guilds(limit=150):
    
                member = guild.get_member(int(user_id.group())) #they changed the .get_member
                
                print ("member is", member) # to just check if it will return non or not 

                #print (member.roles)
                sibling,rm_role = get_sibling_role(member)
                 #= get_sibling_role(member) #the issue
                
                
                role = discord.utils.get(client.get_guild(SERVER_ID).roles, name= f"{sibling}")
                brother = discord.utils.get(client.get_guild(SERVER_ID).roles, name= "Brother Waiting Room")
                                            
                #print ( "role is", role)
   
                await member.add_roles(role)#an issue add_roles is empty, why??
                
                await member.remove_roles(rm_role)
                siblinghood = get_sibling(sibling)
                channel = client.get_channel(siblinghood.general)
 
                await channel.send("<@!" + user_id.group() + "> *has* ***officially*** *joined the Montclair MSA Discord! Welcome your " + sibling + "!*")
            else:
                await message.channel.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
                await message.delete(delay=300)
        else: 
                await message.channel.send("**YOU ARE NOT ADMIN WHAT ARE YOU DOING!!!!**")

    if message.author == client.user:
        return -1; 
    if message.content.startswith("/poll"):
      # print (message.content)
      # messageContent=message.content.replace ("/poll","")

      custom_emojis = re.findall(r'[^\w\s()\"#/[@;:<>{}`+=~|.!?,-]', message.content)      
      # custom_emojis = re.findall(r'[^\w\s()\"#/[@;:<>{}`+=~|.!?,-]', message.content)
      print (custom_emojis)
      
      for index, mystr in enumerate(custom_emojis):
       x = await message.channel.send(mystr)
       await x.add_reaction(str(mystr))
          
    if message.content.startswith("/say"):
      print (message.content)  
      mentions = message.role_mentions
      if (message.author.id !=670325339263860758):
        if re.search(r"\b(retard|ass|fuck|shit|ass|hell|pussy?|fucker|dick|nigger|bitch|bitch|nig|prick|nigga)s?\b", str(message.content).lower()): # No Bad Language/Cussing
            await message.delete(delay=1)
            return await message.channel.send("I do not speak bad language :angry:",delete_after=10)

        else:
            #if (message.raw_mentions ):
            if re.search(r"\b(@|everyone|here)s?\b", str(message.content).lower()): # No Bad Language/Cussing
                await message.channel.send("heyo ... I can't @ everyone :octagonal_sign:")
                #print("You can't mention everyone")
            else:
              await message.channel.send(message.content.replace ("/say","")+ "\n> ||sent by "+message.author.mention+'||')
              await message.delete(delay=1)
          
 #-------------------------------------------         
    if (message.content.startswith("/say")) and (message.author.id == (670325339263860758)): #this removes the tag if Baraa is the one who speaks
      await message.channel.send(message.content.replace ("/say",""))
      await message.delete(delay=1)


    if message.content.lower().startswith('/version'):
        if message.author.id == 670325339263860758 or 233691753922691072 : #if baraa or jake
        #if message.author.id in DEVS:
            await message.channel.send(f"`{RELEASE} | {LAST_MODIFIED}`")
        
    if (message.content.startswith("/cmds")): #this removes the tag if Baraa is the one who speaks
      #await message.channel.send(("hello world"))
        #embed = discord.Embed(title="Title", description="Desc", color=0x00ff00)

        embed = discord.Embed(title = "",desctiption = "this is desctiption",color=0x461111)
        #embed.set_footer(text="this is a footer")
        embed.set_author(name = "Montclair MSA Bot Commands:",icon_url="https://cdn.discordapp.com/attachments/803103105406992415/829141943417962516/Circle_msa_Logo.png")
        #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/803103105406992415/829141943417962516/Circle_msa_Logo.png")
        if check_admin == True: #this is a special mod list with custom commands 
          with open("modCMDS.md") as f: 
              cmds = f.read()

          embed = discord.Embed(  
                  color=0xFFD700 ) #changes the color to golden 
          embed.add_field(name="**About**", value="Hello Mod! these are your commands", inline=False)
          embed.add_field(name="**Commands**", value=cmds, inline=False) 
          embed.add_field(name="Social Media",
                              value="➤ [Instagram](https://www.instagram.com/intermsa/) @intermsa\n➤ [website](http://intermsa.com/) http://intermsa.com/\n➤ [Linkin group]( https://www.linkedin.com/groups/9002140) prof. meet\n",
                              inline=False)
          embed.set_author(name = "InterMSA Bot Commands:",icon_url="https://cdn.discordapp.com/attachments/824860377480429588/829180591811461150/InterMSA_Logo.png")

          embed.set_thumbnail(
                url=
                "https://cdn.discordapp.com/attachments/814602442910072842/838359760037216296/240_F_218846526_SqlIXtk20dEnVcuXvVTGpzUeE3rmLkAe.png")
          await ctx.send(embed=embed)

        embed.add_field(name="/verify",value='verifies users',inline=False)
        embed.add_field(name="/add",value='addes users </add><@username>',inline=False)
        embed.add_field(name="/suggest",value="let's see if agree with your suggestion on #feedback",inline=False)
        embed.add_field(name="/say ",value='the power of the bot repeating what you want',inline=False)
        embed.add_field(name="say my name",value='it says your name',inline=False)
        embed.add_field(name="as",value='Assalamualaikum Warahmatullahi Wabarakatuh',inline=False)
        embed.add_field(name="ws",value='waalaikumsalam warahmatullahi wabarakatuh',inline=False)


        await message.channel.send(embed=embed)


    #if message.content.lower().startswith("say my name"):
    if "say my name" == message.content.lower():
          await message.channel.send((message.author.mention))
          
    if message.content.startswith("/suggest"):
        if message.channel.id == 785554461367468073:#suggestion channel
          thumbsUp = '\N{THUMBS UP SIGN}' #thumbs up emoji
          thumbsDown = "\U0001F44E" #thumbs down emoji

          await message.add_reaction(thumbsUp)
          await message.add_reaction(thumbsDown)

          #if message.content.lower().startswith("say my name"):
          if "say my name" == message.content.lower():
                await message.channel.send((message.author.mention))
                
          if message.content.startswith("/suggest"):
              #if message.channel.id == 785554461367468073:#suggestion channel
            thumbsUp = '\N{THUMBS UP SIGN}' #thumbs up emoji
            thumbsDown = "\U0001F44E" #thumbs down emoji

            await message.add_reaction(thumbsUp)
            await message.add_reaction(thumbsDown)

    if re.search(r"\b(retard|ass|fuck|shit|ass|pussy?|fucker|dick|nigger|bitch|bitch|nig|prick|nigga)s?\b", str(message.content).lower()): # No Bad Language/Cussing
            await message.channel.send("https://gyazo.com/45ad780b2d98f884f00273e3dc0db6cc", delete_after=20)
            await message.delete(delay=1)
    if "as" == message.content:
        await message.channel.send("Assalamualaikum Warahmatullahi Wabarakatuh")
        
    if "ws" == message.content.lower():
        await message.channel.send("Walaikum Assalam Wa Rahmatullahi Wa Barakatuh")

    #if message.content.startswith('hi'):
     #   await message.channel.send("hello")

    if "/baraa" in message.content.lower(): # baraa
        if message.author.id == 670325339263860758: #baraa id
          await message.channel.send("very well inshAllah")

    if re.search(r"\b(Lifting|gym|muscle|strong|lift)s?\b", str(message.content).lower()): 
        if message.author.id == 692522836920893453: #Hamza
          lst = ["https://c.tenor.com/SHfIrV3Ozc0AAAAM/spongebob-squarepants-squidward.gif",
                   "https://c.tenor.com/mg8CiQqEQxcAAAAM/squidward-handsome.gif",
                   "https://c.tenor.com/dDngXdxQyh8AAAAC/tai-lung-kung-fu-panda.gif"]
          r_i = randint(0,len(lst)+1)
          await message.channel.send(str(lst[r_i]), delete_after=30)


    if re.search(r"\b(sleepy|good night|moon|asleep|tired|night|late)s?\b", str(message.content).lower()): 
        if message.author.id == 884499166607335465: #Alaa
          lst = ["let the people sleep in peace Alaa",
                   "https://media0.giphy.com/media/SzNvICICwZrRdNOM1q/200w.gif",
                   "https://media.discordapp.net/attachments/751241894805110817/917639527030480906/download.png?width=266&height=266",
                   "https://c.tenor.com/grWYw-2edNMAAAAC/disney-sleepy.gif","https://c.tenor.com/Ftfa-ehSIs4AAAAM/miyako-hoshino-wataten.gif",
                   "https://media.discordapp.net/attachments/751241894805110817/917640709689970728/680.png?width=400&height=300"]
          r_i = randint(0,len(lst)+1)
          await message.channel.send(str(lst[r_i]))
          #await message.channel.send("Alaa, let the people sleep in peace")

    if "done" in message.content.lower(): 
        if message.author.id == 815657491948896297: #Noura
          lst = ["https://c.tenor.com/93OUVuCIk6MAAAAC/done-and-done-spongebob.gif",
                 "https://c.tenor.com/suJJHArPXSgAAAAC/naruto-anime.gif",
                 "https://i.imgur.com/aojrg03.gif","No, Noura u are done.💢", "Noura your teammates are here for you not against you",
                 "yes you're done💯.","https://thumbs.gfycat.com/AjarGlamorousArrowana-size_restricted.gif",
                 "https://c.tenor.com/DTjGghU34AsAAAAM/cats-angry.gif","https://c.tenor.com/EtSlxvVMqFgAAAAM/cat-annoyed.gif",
                 "https://c.tenor.com/M82nGQQZZXMAAAAd/cat-cats.gif"]
          r_i = randint(0,len(lst)+1)
          await message.channel.send(str(lst[r_i]))

    if re.search(r"\b(marriage|wife|Married|couple|love|wedding|late)s?\b", str(message.content).lower()):
        if message.author.id == 571083432315191299: #Ali
          lst = ["The code forbids it",
          "https://cdn.discordapp.com/attachments/687405522131091479/814673940080361553/image0.jpg","#find_Ali_a_wife",
          "that's rough buddy",
          "https://im.vsco.co/aws-us-west-2/d13bb8/184238871/5f70b60a797bbf602238f27f/vsco5f70b60b8165e.jpg?w=480"]
          r_i = randint(0,len(lst)+1)
          await message.channel.send(str(lst[r_i]))

    if "/someone" in message.content.lower():
          if message.author.id == 670325339263860758: #baraa id
            await message.channel.send("https://thumbs.gfycat.com/LavishBoldIvorygull-size_restricted.gif")

    if "listen" in message.content.lower(): 
        if message.author.id == 761666659428728832: #Maysa
          lst = ["I am always here listening",
                 "ALL BE QUITE THE PRINCESS IS TALKING",
                 "https://static.wikia.nocookie.net/disney/images/f/f6/Frozen-disneyscreencaps.com-826.jpg/revision/latest?cb=20140311122855",
                 "MAYSA HAS SPOKEN.", "MashAllah"]
          r_i = randint(0,2)
          await message.channel.send(str(lst[r_i]))
          
    if "hey" in message.content.lower():
        if message.author.id == 761666659428728832:
          lst = ["MAYSA HAS SPOKEN", "**SILENCE** the Princess wants to give her speech"
          ,"https://c.tenor.com/ZmOWVbtbqbUAAAAM/unacceptable-lemon-grab.gif"
          ,"https://64.media.tumblr.com/51ebefb6aae1a5440efe8b2e7a8872e5/55c083568507830d-14/s540x810/fda12e18344e180981a0f8b1a3134e20d360aa33.gifv"
                 ]
          r_i = randint(0,2)
          await message.channel.send(str(lst[r_i]))

    if ("busy") in message.content.lower(): 
        if message.author.id == 761666659428728832: #Maysa
          await message.add_reaction("😭")
          await message.add_reaction("❄")  
          await message.add_reaction("👎")  

    

    if listen_announce(message): # Send to alternate announcement channel
        
        announce_channel = listen_announce(message)
        channel = client.get_channel(announce_channel)
        await channel.send(
    message.content, files=[await f.to_file() for f in message.attachments])

        #await channel.send(message.content)

    '''
        try:
          ext = re.search(r".(png|jpg|jpeg|mp4)$", message.attachments[0].url)
        except IndexError:
          ext = None
        
        if len(message.attachments) == 1 and ext:
            file_name = "imgs/reattach" + str(ext.group())
            with open(file_name, "wb") as f:
                await message.attachments[0].save(f)
            img = File(file_name)
            await channel.send(message.content, file=img)
            os.remove(file_name)
        else:
            await channel.send(message.content)
'''

    


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
                            #print (channel)
                            if str(channel) == "brothers-waiting-room":
                                await channel.send(f"***" + message.author.mention + "***" + " *please wait until <@&769794574071496715> adds you*")

                                #await channel.send(f"<@&769794574071496715> ***" + message.author.mention + "***" + " *has joined the montclair MSA Discord!*")
                            elif str(channel) == "sisters-waiting-room":
                                await channel.send(f"***" + message.author.mention + "***" + " *please wait until <@&769795211869028352> adds you*")
                                #await channel.send(f"<@&769795211869028352> ***" + message.author.mention + "***" + " *has joined the montclair MSA Discord!*")

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
