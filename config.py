import os,re
#from key import *
#print (os.getcwd())
#print (os.listdir())
class Server(object):
   #__slots__ = ("name", "wait", "general")
   def __init__(self, name, wait, general, announce, **kwargs):
      self.__dict__.update(kwargs)
      self.name = name
      self.wait = wait
      self.general = general
      self.announce = announce

#BOT = os.getenv("BOT_SECRET", bot_pass())


class StaticMsg(object):
   __slots__ = ("channel", "message", "reaction")
   def __init__(self, channel, message, reaction):
      self.channel = channel
      self.message = message
      self.reaction = reaction

#__bro_options = {"role_select": 756318101880176752} #the role selection channe, so ill not need it for verify
#__sis_options = {"role_select": 750886997874311179}

brothers = Server("Brother", 767930134022848512, # waiting room for the brothers
                  756582312208236700, 756582312208236698) # the one on the left is the general bro, the one on the right is the announcements
                  

sisters = Server("Sister", 769790034999509022,#these are njit sisters id
                 761109060215898132, 761112787292258305)


#CONST_MSG = [role_selection_s, role_selection_b]

SERVER_ID = 756582312208236695
VERIFY_ID = 761359239004160020


DB_PATH = "database/database.db"
#DB_SECRET = "PRIVATE_key"

with open("private.txt") as f:
   privatekey = f.read()

with open ("public.txt") as f:
   publickey = f.read()
   

SP = os.getenv("SECRET_PASS", "ANY")
DB_SECRET = re.sub(r"\\n", '\n', os.getenv("DB_SECRET", privatekey))
ENCRYPT_KEY = re.sub(r"\\n", '\n', os.getenv("PUBLIC_KEY", publickey))

'''
with open("cmds.md") as f:
   cmds = f.read()
await message.channel.send()
'''

'''
- Create 'Muslim' role or w/e you wanna call the role that
  every sister gets to officially join
- Create #verify chat
- Enable Developer Mode
  Copy ID's:
  - Right click on Server Name
  - Right click on #verify chat
  - Right click on #general chat
- Make @everyone role only able to talk in #verify chat
'''
