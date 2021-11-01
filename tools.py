import asyncio
import re, os, time, smtplib, hashlib
import sqlite3 as sql
from random import randint
from email.message import EmailMessage
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from config import *
#from key import *


#from key import *
# make sure install the libraries pip3 install -r requitments.txt

#from key import db_pass, email_pass

DB_CONN = sql.connect(DB_PATH)
KEY = RSA.import_key(DB_SECRET.encode("ascii"), SP) # Just you try and get it :D


#If email treated as spam:
 #https://support.google.com/mail/contact/bulk_send_new?rd=1


def edit_file(file, value):
    with open(file, 'r+') as f:
        lines = f.readlines()
        f.seek(0); found = False
        for line in lines:
            line = line.strip('\n')
            if str(line).lower() != str(value).lower():
                f.write(line + '\n')
            else:
                found = True
        f.truncate()
        return found

def email_pass():
    with open("email.txt") as f:
        return f.read()

APP_PASS = os.getenv("EMAIL_SECRET", email_pass())
# Return 4-digit verification code string after sending email
def send_email(addr: str, test=False) -> str:
    # Return 4-digit verification code string
    sCode = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"
    if not test:
        msg = EmailMessage()
        msg.set_content(f"\
    <html><body><b>Your verification code to join the chat is below:<br><br>\
    <h2>{sCode}</h2></b>Please copy & paste this code in the \
    <i><u>#verify</u></i> text channel of your montclair  MSA Discord. \
    This code will expire in 15 minutes.</body></html>", subtype="html")
        msg["Subject"] = "Verification Code for montclair MSA Discord"
        msg["From"] = "Montclair MSA"#noreply.njitmsa.discord@gmail.com
        msg["To"] = addr
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login("montclairmsaofficialdiscord@gmail.com", APP_PASS)
                #s.login("montclairmsaofficialdiscord@gmail.com", "hdopqkbwwqnftsny")
                s.send_message(msg)
    else:
        print(sCode) 
    return sCode
# SQL Query Function

def sqlite_query(query, args=(), one=False):
   cur = DB_CONN.cursor()
   cur = DB_CONN.execute(query, args); DB_CONN.commit()
   rv = [dict((cur.description[idx][0], value)
              for idx, value in enumerate(row)) for row in cur.fetchall()]
   return (rv[0] if rv else None) if one else rv

def encrypt(msg):
    cipher = PKCS1_OAEP.new(KEY.publickey())
    cipher_text = cipher.encrypt(msg.encode())
    return cipher_text

def decrypt(cipher_text):
    cipher = PKCS1_OAEP.new(KEY)
    decrypted_text = cipher.decrypt(cipher_text)
    return decrypted_text.decode()

def get_name(addr: str) -> str:
    sid = re.sub(r"@.+\.", '', str(addr))
    sid = sid.replace("edu", '')
    hashed_sid = hashlib.sha1(sid.encode()).hexdigest()
    query = f"SELECT full_name FROM Links WHERE sid=?"
    result = sqlite_query(query, (hashed_sid,), one=True)
    if result != None:
        full_name = result["full_name"]
        return decrypt(full_name)
        
print (get_name("nassarb1@montclair.edu"))

# Return gender based on user

def check_admin(msg):
    roles = msg.author.roles
    for role in roles:
        if role.name == "Eboard Sister" or role.name == "Eboard Brother" or role.name == "development" or role.name == "Admin": 
            return True
    return False


def get_sibling_role(member):
    if member is None:
        return None
    #roles = member.roles; ret = None #<==there is an issue on this
    roles, ret = member.roles, None

    for role in roles:
        if role.name == "Brothers Waiting Room":
            ret = ("Brother", role); break
        elif role.name == "Sisters Waiting Room":
            ret = ("Sister", role); break
    return ret

def get_sibling(sibling):
    if sibling == "Brother":
        return brothers
    else:
        return sisters

#checks if you say @everyone on either brothers or sisters announcement, retuns true if detects it
def listen_announce(msg):
    if msg.channel.id == brothers.announce:
        if "@everyone" in msg.content:
            return sisters.announce
    elif msg.channel.id == sisters.announce:
        if "@everyone" in msg.content:
            return brothers.announce
    else:
        False


def listen_verify(msg):
    if msg.channel.id == VERIFY_ID:
        if msg.content.startswith('/verify'):
            request = re.sub(r"/verify ", '', msg.content)
            gender = re.search(r"(brothers?|sis(tas?|ters?))", request) or ''
            if gender:
                ucid = re.sub(fr"{gender.group()}", '', request).strip(' ')
                if gender.group()[0] == 'b':
                    gender = "Brother"
                else:
                    gender = "Sister"
                return ucid, gender
            return ('', '')

def listen_code(msg):
    if msg.channel.id == VERIFY_ID:
        return re.search(r"^\d\d\d\d$", msg.content)

def in_general(channel_id):
    if channel_id == brothers.general:
        return brothers
    elif channel_id == sisters.general:
        return sisters
    else:
        return False

async def check_verify(record, msg, temp):
    while True:
        with open("verify.txt") as f:
            text = f.read()
            if not re.search(fr"{record}", text):
                break
        await asyncio.sleep(0)
    await msg.delete(); await temp.delete()
