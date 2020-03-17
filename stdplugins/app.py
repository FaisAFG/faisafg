# -*- coding: utf-8 -*-

from telethon import TelegramClient, events

from async_generator import aclosing

import time

import logging

import random, re

import asyncio

import os

from gtts import gTTS

import time

import sys

import urbandict

import gsearch

import subprocess

from datetime import datetime

from requests import get

import wikipedia

import antispam

import inspect

import platform

from googletrans import Translator

from random import randint

logging.basicConfig(level=logging.DEBUG)

api_id=os.environ['API_KEY']

api_hash=os.environ['API_HASH']

SPAM=False

ISAFK=False

AFKREASON="No Reason"

USERS={}

COUNT_MSG=0

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))

WIDE_MAP[0x20] = 0x3000

client = TelegramClient('session_name', api_id, api_hash).start()

client.start()

@client.on(events.NewMessage(outgoing=True, pattern='.del'))

async def delmsg(event):

    i=1

    async for message in client.iter_messages(event.chat_id,from_user='me'):

        if i>2:

            break

        i=i+1

        await message.delete()

@client.on(events.NewMessage(outgoing=True, pattern='.log'))

async def log(event):

    textx=await event.get_reply_message()

    if textx:

         message = textx

         message = str(message.message)

    else:

        message = await client.get_messages(event.chat_id)

        message = str(message[0].message[4:])

    await client.send_message(-1001162835202,message)

    await event.edit("```Logged Successfully```")

@client.on(events.NewMessage(outgoing=True, pattern='.purgeme'))

async def purgeme(event):

    message=await client.get_messages(event.chat_id)

    count = int(message[0].message[9:])

    i=1

    async for message in client.iter_messages(event.chat_id,from_user='me'):

        if i>count+1:

            break

        i=i+1

        await message.delete()

    await client.send_message(event.chat_id,"```Purge Complete!``` Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")

    await client.send_message(-1001162835202,"Purge of "+str(count)+" messages done successfully.")

    time.sleep(2)

    i=1

    async for message in client.iter_messages(event.chat_id,from_user='me'):

        if i>1:

            break

        i=i+1

        await message.delete()

@client.on(events.NewMessage(incoming=True))

async def spam_tracker(event):

    global SPAM

    if SPAM==True:

       ch=str(event.raw_text)

       spamscore=antispam.score(ch)

       spambool=antispam.is_spam(ch)

       if spambool==True:

         await event.reply('Spam Message Detected')

         await event.reply('Spam results for `' + ch + '`\nScore: ' + spamscore + '\nIs Spam: ' + spambool)

            

@client.on(events.NewMessage(incoming=True))

async def mention_afk(event):

    global COUNT_MSG

    global USERS

    global ISAFK

    global AFKREASON

    if event.message.mentioned:

        if ISAFK:

            if event.sender:

               if event.sender.username not in USERS:

                  await event.reply("Sorry! My boss in AFK due to ```"+AFKREASON+"```Would ping him to look into the message soonðŸ˜‰.**This message shall be self destructed in 15 seconds**")

                  time.sleep(15)

                  i=1

                  async for message in client.iter_messages(event.chat_id,from_user='me'):

                        if i>1:

                           break

                        i=i+1

                        await message.delete()

                  USERS.update({event.sender.username:1})

                  COUNT_MSG=COUNT_MSG+1

            elif event.sender.username in USERS:

                 if USERS[event.sender.username] % 5 == 0:

                      await event.reply("Sorry! But my boss is still not here. Try to ping him a little later. I am sorryðŸ˜–. He mentioned me he was busy with ```"+AFKREASON+"```**This message shall be self destructed in 15 seconds**")

                      time.sleep(15)

                      i=1

                      async for message in client.iter_messages(event.chat_id,from_user='me'):

                               if i>1:

                                   break

                               i=i+1

                               await message.delete()

                      USERS[event.sender.username]=USERS[event.sender.username]+1

                      COUNT_MSG=COUNT_MSG+1

                 else:

                   USERS[event.sender.username]=USERS[event.senser.username]+1

                   COUNT_MSG=COUNT_MSG+1

            else:

                  await event.reply("Sorry! My boss in AFK due to ```"+AFKREASON+"```Would ping him to look into the message soonðŸ˜‰. **This message shall be self destructed in 15 seconds**")

                  time.sleep(15)

                  i=1

                  async for message in client.iter_messages(event.chat_id,from_user='me'):

                        if i>1:

                           break

                        i=i+1

                        await message.delete()

                  USERS.update({event.chat_id:1})

                  COUNT_MSG=COUNT_MSG+1

                  if event.chat_id in USERS:

                   if USERS[event.chat_id] % 5 == 0:

                     await event.reply("Sorry! But my boss is still not here. Try to ping him a little later. I am sorryðŸ˜–. He mentioned me he was busy with ```"+AFKREASON+"```**This message shall be self destructed in 15 seconds**")

                     time.sleep(15)

                     i=1

                     async for message in client.iter_messages(event.chat_id,from_user='me'):

                        if i>1:

                           break

                        i=i+1

                        await message.delete()

                     USERS[event.chat_id]=USERS[event.chat_id]+1

                     COUNT_MSG=COUNT_MSG+1

                   else:

                    USERS[event.chat_id]=USERS[event.chat_id]+1

                    COUNT_MSG=COUNT_MSG+1

                    

@client.on(events.NewMessage(outgoing=True, pattern='.edit'))

async def editme(event):

    message=await client.get_messages(event.chat_id)

    string = str(message[0].message[8:])

    i=1

    async for message in client.iter_messages(event.chat_id,from_user='me'):

        if i==2:

            await message.edit(string)

            await event.delete()

            break

        i=i+1

    await client.send_message(-1001162835202,"Edit query was executed successfully")

    

@client.on(events.NewMessage(pattern=r'.google (.*)'))

async def gsearch(event):

        match = event.pattern_match.group(1)

        result_=subprocess.run(['gsearch', match], stdout=subprocess.PIPE)

        result=str(result_.stdout.decode())

        await client.send_message(await client.get_input_entity(event.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=event.id, link_preview=False)

        await client.send_message(-1001162835202,"Google Search query "+match+" was executed successfully")

        

@client.on(events.NewMessage(pattern=r'.wiki (.*)'))

async def wiki(event):

        match = event.pattern_match.group(1)

        result=wikipedia.summary(match)

        await client.send_message(await client.get_input_entity(event.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=event.id, link_preview=False)

        await client.send_message(-1001162835202,"Wiki query "+match+" was executed successfully")

        

@client.on(events.NewMessage(outgoing=True, pattern='.afk'))

async def set_afk(event):

            message=await client.get_messages(event.chat_id)

            string = str(message[0].message[8:])

            global ISAFK

            global AFKREASON

            ISAFK=True

            await event.edit("I am now AFK!")

            if string!="":

                AFKREASON=string

                

@client.on(events.NewMessage(outgoing=True, pattern='.antispamon'))

async def set_asm(event):

            global SPAM

            SPAM=True

            await event.edit("Spam Tracking turned on!")

                 

@client.on(events.NewMessage(outgoing=True, pattern='.antispamoff'))

async def set_asm_off(event):

            global SPAM

            SPAM=False

            await event.edit("Spam Tracking turned off!")

            

@client.on(events.NewMessage(pattern='.calc'))

async def evaluate(event):    

    evaluation = eval(event.text[6:])

    if inspect.isawaitable(evaluation):

       evaluation = await evaluation

    if evaluation:

      await event.edit("**Query: **\n```"+event.text[6:]+'```\n**Result: **\n```'+str(evaluation)+'```')

    else:

      await event.edit("**Query: **\n```"+event.text[6:]+'```\n**Result: **\n```No Result Returned/False```')

    await client.send_message(-1001162835202,"Eval query "+event.text[6:]+" was executed successfully")

    

#@client.on(events.NewMessage(outgoing=True, pattern=r'.exec (.*)'))

#async def run(event):

# code = event.raw_text[5:]

# resp = event.respond

# creator='written by [Twit](tg://user?id=234480941) and copied by [blank](tg://user?id=214416808) (piece of shit)'

# exec(

#  f'async def __ex(event): ' +

#  ''.join(f'\n {l}' for l in code.split('\n'))

# )

# result = await locals()['__ex'](event)

# if result:

#  await event.edit("**Query: **\n```"+event.text[5:]+'```\n**Result: **\n```'+str(result)+'```')

# else:

#  await event.edit("**Query: **\n```"+event.text[5:]+'```\n**Result: **\n```'+'No Result Returned/False'+'```')

# await client.send_message(-1001162835202,"Exec query "+event.text[5:]+" was executed successfully") 

@client.on(events.NewMessage(pattern='.ping'))

async def ping(event):

    start = datetime.now()

    await event.edit('Pong!')

    end = datetime.now()

    ms = (end - start).microseconds / 1000

    await event.edit('Pong!\n%sms' % (ms))

@client.on(events.NewMessage(outgoing=True, pattern='.spam'))

async def spammer(event):

    message=await client.get_messages(event.chat_id)

    counter=int(message[0].message[6:8])

    spam_message=str(event.text[8:])

    await asyncio.wait([event.respond(spam_message) for i in range(counter)])

    await event.delete()

    

@client.on(events.NewMessage(outgoing=True, pattern='.speed'))

async def speedtest(event):

    l=await event.reply('```Running speed test . . .```')

    k=subprocess.run(['speedtest-cli'], stdout=subprocess.PIPE)

    await l.edit('```' + k.stdout.decode()[:-1] + '```')

    

@client.on(events.NewMessage(pattern='.tl'))

async def translateme(event):     

    translator=Translator()

    textx=await event.get_reply_message()

    message = await client.get_messages(event.chat_id) 

    if textx:

         message = textx

         text = str(message.message)

    else:

        text = str(message[0].message[4:])

    reply_text=translator.translate(text, dest='en').text

    reply_text="```Source: ```\n"+text+"```Translation: ```\n"+reply_text

    await client.send_message(event.chat_id,reply_text)

    await client.send_message(-1001162835202,"Translate query "+message+" was executed successfully")

    

@client.on(events.NewMessage(outgoing=True, pattern='.stretch'))

async def stretch(event):

    textx=await event.get_reply_message()

    message = await client.get_messages(event.chat_id)

    if textx:

         message = textx

         message = str(message.message)

    else:

        message = str(message[0].message[5:])

    count = random.randint(3, 10)

    reply_text = re.sub(r'([aeiouAEIOUï½ï½…ï½‰ï½ï½•ï¼¡ï¼¥ï¼©ï¼¯ï¼µ])', (r'\1' * count), message)

    await event.edit(reply_text)

    

@client.on(events.NewMessage(incoming=True))

async def afk_on_pm(event):

    global ISAFK

    global USERS

    global COUNT_MSG

    global AFKREASON

    if event.is_private:

        if ISAFK:

            if event.sender:

              if event.sender.username not in USERS:

                  await event.reply("Sorry! My boss in AFK due to ```"+AFKREASON+"```Would ping him to look into the message soonðŸ˜‰. **This message shall be self destructed in 15 seconds**")

                  time.sleep(15)

                  i=1

                  async for message in client.iter_messages(event.chat_id,from_user='me'):

                        if i>1:

                           break

                        i=i+1

                        await message.delete()

                  USERS.update({event.sender.username:1})

                  COUNT_MSG=COUNT_MSG+1

            elif event.sender.username in USERS:

                   if USERS[event.sender.username] % 5 == 0:

                     await event.reply("Sorry! But my boss is still not here. Try to ping him a little later. I am sorryðŸ˜–. He mentioned me he was busy with ```"+AFKREASON+"```**This message shall be self destructed in 15 seconds**")

                     time.sleep(15)

                     i=1

                     async for message in client.iter_messages(event.chat_id,from_user='me'):

                        if i>1:

                           break

                        i=i+1

                        await message.delete()

                     USERS[event.sender.username]=USERS[event.sender.username]+1

                     COUNT_MSG=COUNT_MSG+1

                   else:

                    USERS[event.sender.username]=USERS[event.sender.username]+1

                    COUNT_MSG=COUNT_MSG+1

            else:

                  await event.reply("Sorry! My boss in AFK due to ```"+AFKREASON+"```Would ping him to look into the message soonðŸ˜‰. **This message shall be self destructed in 15 seconds**")

                  time.sleep(15)

                  i=1

                  async for message in client.iter_messages(event.chat_id,from_user='me'):

                        if i>1:

                           break

                        i=i+1

                        await message.delete()

                  USERS.update({event.chat_id:1})

                  COUNT_MSG=COUNT_MSG+1

                  if event.chat_id in USERS:

                   if USERS[event.chat_id] % 5 == 0:

                     await event.reply("Sorry! But my boss is still not here. Try to ping him a little later. I am sorryðŸ˜–. He mentioned me he was busy with ```"+AFKREASON+"```**This message shall be self destructed in 15 seconds**")

                     time.sleep(15)

                     i=1

                     async for message in client.iter_messages(event.chat_id,from_user='me'):

                        if i>1:

                           break

                        i=i+1

                        await message.delete()

                     USERS[event.chat_id]=USERS[event.chat_id]+1

                     COUNT_MSG=COUNT_MSG+1

                   else:

                    USERS[event.chat_id]=USERS[event.chat_id]+1

                    COUNT_MSG=COUNT_MSG+1

                    

@client.on(events.NewMessage(pattern='.cp'))   

async def copypasta(event):

    textx=await event.get_reply_message()

    if textx:

         message = textx

         message = str(message.message)

    else:

        message = await client.get_messages(event.chat_id)

        message = str(message[0].message[3:])

    emojis = ["ðŸ˜‚", "ðŸ˜‚", "ðŸ‘Œ", "âœŒ", "ðŸ’ž", "ðŸ‘", "ðŸ‘Œ", "ðŸ’¯", "ðŸŽ¶", "ðŸ‘€", "ðŸ˜‚", "ðŸ‘“", "ðŸ‘", "ðŸ‘", "ðŸ•", "ðŸ’¥", "ðŸ´", "ðŸ’¦", "ðŸ’¦", "ðŸ‘", "ðŸ†", "ðŸ˜©", "ðŸ˜", "ðŸ‘‰ðŸ‘Œ", "ðŸ‘€", "ðŸ‘…", "ðŸ˜©", "ðŸš°"]

    reply_text = random.choice(emojis)

    b_char = random.choice(message).lower() # choose a random character in the message to be substituted with ðŸ…±ï¸

    for c in message:

        if c == " ":

            reply_text += random.choice(emojis)

        elif c in emojis:

            reply_text += c

            reply_text += random.choice(emojis)

        elif c.lower() == b_char:

            reply_text += "ðŸ…±ï¸"

        else:

            if bool(random.getrandbits(1)):

                reply_text += c.upper()

            else:

                reply_text += c.lower()

    reply_text += random.choice(emojis)

    await event.edit(reply_text)

    

@client.on(events.NewMessage(outgoing=True, pattern='.notafk'))

async def not_afk(event):

            global ISAFK

            global COUNT_MSG

            global USERS

            global AFKREASON

            ISAFK=False

            await event.edit("I have returned from AFK mode.")

            await event.respond("```You had recieved "+str(COUNT_MSG)+" messages while you were away. Check log for more details. This auto-generated message shall be self destructed in 2 seconds.```")

            time.sleep(2)

            i=1

            async for message in client.iter_messages(event.chat_id,from_user='me'):

                if i>1:

                    break

                i=i+1

                await message.delete()

            await client.send_message(-1001162835202,"You had recieved "+str(COUNT_MSG)+" messages from "+str(len(USERS))+" chats while you were away") 

            for i in USERS:

                await client.send_message(-1001162835202,str(i)+" sent you "+"```"+str(USERS[i])+" messages```")

            COUNT_MSG=0

            USERS={}

            AFKREASON="No reason"

            

@client.on(events.NewMessage(pattern='.vapor'))  

async def vapor(event):

    textx=await event.get_reply_message()

    message = await client.get_messages(event.chat_id)

    if textx:

         message = textx

         message = str(message.message)

    else:

        message = str(message[0].message[7:])

    if message:

        data = message

    else:

        data = ''    

    reply_text = str(data).translate(WIDE_MAP)

    await event.edit(reply_text)

    

@client.on(events.NewMessage(outgoing=True, pattern=':/'))

async def dopedance(event):

    uio=['/','\\']

    for i in range (1,15):

        time.sleep(0.3)

        await event.edit(':'+uio[i%2])

        

@client.on(events.NewMessage(outgoing=True, pattern='-_-'))

async def mutemeow(event):

    await event.delete()

    t = '-_-'

    r = await event.reply(t)

    for j in range(10):

        t = t[:-1] + '_-'

        await r.edit(t)

        

@client.on(events.NewMessage(pattern='.react'))

async def react(event):        

    reactor=['Ê˜â€¿Ê˜','ãƒ¾(-_- )ã‚ž','(ã£Ë˜Ú¡Ë˜Ï‚)','(Â´Ð¶ï½€Ï‚)','( à²  Ê–Ì¯ à² )','(Â° ÍœÊ–Í¡Â°)â•­âˆ©â•®','(áµŸàº¶ï¸µ áµŸàº¶)','(à¸‡ãƒ„)à¸§','Êš(â€¢ï½€','(ã£â–€Â¯â–€)ã¤','(â— ï¹â— )','( Í¡à²  Ê–Ì¯ Í¡à² )','( à°  ÍŸÊ– à° )','(âˆ©ï½€-Â´)âŠƒâ”â˜†ï¾Ÿ.*ï½¥ï½¡ï¾Ÿ','(âŠƒï½¡â€¢Ìâ€¿â€¢Ì€ï½¡)âŠƒ','(._.)','{â€¢Ìƒ_â€¢Ìƒ}','(áµ”á´¥áµ”)','â™¨_â™¨','â¥€.â¥€','Ø­Ëšà¯°Ëšã¥ ','(Ò‚â—¡_â—¡)','Æª(Ú“×²)â€ŽÆªâ€‹â€‹','(ã£â€¢Ìï½¡â€¢Ì)â™ªâ™¬','â—–áµ”á´¥áµ”â—— â™ª â™« ','(â˜žï¾Ÿãƒ®ï¾Ÿ)â˜ž','[Â¬Âº-Â°]Â¬','(Ô¾â€¸ Ô¾)','(â€¢Ì€á´—â€¢Ì)Ùˆ Ì‘Ì‘','ãƒ¾(Â´ã€‡`)ï¾‰â™ªâ™ªâ™ª','(à¸‡\'Ì€-\'Ì)à¸‡','áƒš(â€¢Ìâ€¢Ìáƒš)','Ê• â€¢ÌØˆâ€¢Ì€ â‚Ž','â™ªâ™ª ãƒ½(Ë‡âˆ€Ë‡ )ã‚ž','Ñ‰ï¼ˆï¾ŸÐ”ï¾ŸÑ‰ï¼‰','( Ë‡à·´Ë‡ )','ëˆˆ_ëˆˆ','(à¹‘â€¢Ì â‚ƒ â€¢Ì€à¹‘) ','( Ë˜ Â³Ë˜)â™¥ ','Ô…(â‰–â€¿â‰–Ô…)','â™¥â€¿â™¥','â—”_â—”','â½â½à¬˜( ËŠáµ•Ë‹ )à¬“â¾â¾','ä¹( â—” à±ªâ—”)ã€Œ      â”‘(ï¿£Ð” ï¿£)â”','( à° àµ à°  )ï¾‰','Ù©(à¹_à¹)Û¶','â”Œ(ã††ã‰¨ã††)Êƒ','à° _à° ','(ã¥ï½¡â—•â€¿â€¿â—•ï½¡)ã¥','(ãƒŽà²  âˆ©à² )ãƒŽå½¡( \\oÂ°o)\\','â€œãƒ½(Â´â–½ï½€)ãƒŽâ€','à¼¼ à¼Žàº¶ à·´ à¼Žàº¶à¼½','ï½¡ï¾Ÿ( ï¾Ÿà®‡â€¸à®‡ï¾Ÿ)ï¾Ÿï½¡','(ã¥ï¿£ Â³ï¿£)ã¥','(âŠ™.â˜‰)7','á••( á› )á•—','t(-_-t)','(à²¥âŒ£à²¥)','ãƒ½à¼¼ à² ç›Šà²  à¼½ï¾‰','à¼¼âˆµà¼½ à¼¼â¨à¼½ à¼¼â¢à¼½ à¼¼â¤à¼½','ãƒŸâ—ï¹â˜‰ãƒŸ','(âŠ™_â—Ž)','Â¿â“§_â“§ï®Œ','à² _à² ','(Â´ï½¥_ï½¥`)','á•¦(Ã²_Ã³Ë‡)á•¤','âŠ™ï¹âŠ™','(â•¯Â°â–¡Â°ï¼‰â•¯ï¸µ â”»â”â”»','Â¯\_(âŠ™ï¸¿âŠ™)_/Â¯','Ù©â—”Ì¯â—”Û¶','Â°â€¿â€¿Â°','á•™(â‡€â€¸â†¼â€¶)á•—','âŠ‚(â—‰â€¿â—‰)ã¤','Vâ€¢á´¥â€¢V','q(â‚â€¿â‚)p','à²¥_à²¥','à¸…^â€¢ï»Œâ€¢^à¸…','à²¥ï¹à²¥','ï¼ˆ ^_^ï¼‰oè‡ªè‡ªoï¼ˆ^_^ ï¼‰','à² â€¿à² ','ãƒ½(Â´â–½`)/','áµ’á´¥áµ’#','( Í¡Â° ÍœÊ– Í¡Â°)','â”¬â”€â”¬ï»¿ ãƒŽ( ã‚œ-ã‚œãƒŽ)','ãƒ½(Â´ãƒ¼ï½€)ãƒŽ','â˜œ(âŒ’â–½âŒ’)â˜ž','Îµ=Îµ=Îµ=â”Œ(;*Â´Ð”`)ï¾‰','(â•¬ à² ç›Šà² )','â”¬â”€â”¬âƒ°Í¡â€‡(áµ”áµ•áµ”Íœâ€‡)','â”»â”â”» ï¸µãƒ½(`Ð”Â´)ï¾‰ï¸µï»¿ â”»â”â”»','Â¯\_(ãƒ„)_/Â¯','Ê•áµ”á´¥áµ”Ê”','(`ï½¥Ï‰ï½¥Â´)','Ê•â€¢á´¥â€¢Ê”','áƒš(ï½€ãƒ¼Â´áƒš)','Ê•Ê˜Ì…ÍœÊ˜Ì…Ê”','ï¼ˆã€€ï¾ŸÐ”ï¾Ÿï¼‰','Â¯\(Â°_o)/Â¯','(ï½¡â—•â€¿â—•ï½¡)']

    index=randint(0,len(reactor))

    reply_text=reactor[index]

    await event.edit(reply_text)

    

@client.on(events.NewMessage(outgoing=True, pattern='.runs'))

async def react(event):        

    reactor=['Where do you think you\'re going?','Get back here!','Not so fast...','Hasta la vista, baby.','I\'m behind you...','Yeah, you better run!']

    index=randint(0,len(reactor)-1)

    reply_text=reactor[index]

    await event.edit(reply_text)

    await client.send_message(-1001162835202,"You ran away from a cancerous chat")

    

@client.on(events.NewMessage(outgoing=True, pattern='.purge'))  

async def fastpurge(event):

   chat = await event.get_input_chat()

   msgs = []

   count =0

   async with aclosing(client.iter_messages(chat, min_id=event.reply_to_msg_id)) as h:

    async for m in h:

        msgs.append(m)

        count=count+1

        if len(msgs) == 100:

            await client.delete_messages(chat, msgs)

            msgs = []

   if msgs:

    await client.delete_messages(chat, msgs)

   await client.send_message(event.chat_id,"```Fast Purge Complete!\n```Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")

   await client.send_message(-1001162835202,"Purge of "+str(count)+" messages done successfully.")

   time.sleep(2)

   i=1

   async for message in client.iter_messages(event.chat_id,from_user='me'):

        if i>1:

            break

        i=i+1

        await message.delete()

        

@client.on(events.NewMessage(outgoing=True, pattern='.sd'))

async def selfdestruct(event):

    message=await client.get_messages(event.chat_id)

    counter=int(message[0].message[4:6])

    text=str(event.text[6:])

    text=text+"```This message shall be self-destructed in "+str(counter)+" seconds```"

    await event.delete()

    await client.send_message(event.chat_id,text)

    time.sleep(counter)

    i=1

    async for message in client.iter_messages(event.chat_id,from_user='me'):

        if i>1:

            break

        i=i+1

        await message.delete()

        await client.send_message(-1001162835202,"sd query done successfully")

        

@client.on(events.NewMessage(pattern='^.ud (.*)'))

async def ud(event):

  await event.edit("Processing...")

  str = event.pattern_match.group(1)

  mean = urbandict.define(str)

  if len(mean) >= 0:

    await event.edit('Text: **'+str+'**\n\nMeaning: **'+mean[0]['def']+'**\n\n'+'Example: \n__'+mean[0]['example']+'__')

    await client.send_message(-1001162835202,"ud query "+str+"executed successfully.")

  else:

    await event.edit("No result found for **"+str+"**")

    

@client.on(events.NewMessage(outgoing=True, pattern='.tts'))  

async def tts(event):

    textx=await event.get_reply_message()

    replye = await client.get_messages(event.chat_id)

    if textx:

         replye = textx

         replye = str(replye.message)

    else:

        replye = str(replye[0].message[5:])

    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")

    lang="en"

    tts = gTTS(replye, lang)

    tts.save("k.mp3")

    with open("k.mp3", "rb") as f:

        linelist = list(f)

        linecount = len(linelist)

    if linecount == 1:

        lang = "en"

        tts = gTTS(replyes, lang)

        tts.save("k.mp3")

    with open("k.mp3", "r") as speech:  

        await client.send_file(event.chat_id,speech,voice_note=True)

        os.remove("k.mp3")

if len(sys.argv) < 2:

    client.run_until_disconnected()

