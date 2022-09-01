import discord
from discord import File
from discord.ext import commands
import asyncio
import base64

from mail import mail
from config import config

client = discord.Client(intents=discord.Intents.default())




@client.event
async def on_ready():
    print('Login As：', client.user)
    game = discord.Game('test by lokey')
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    if message.content == "hi" or message.content == "HI":
        await message.channel.send('Hi')

    if message.content.startswith('m'):
        tmp = message.content.split(" ",2)
        if len(tmp) != 1:
          num,tem,filelist = mail.catch(int(tmp[1]))
          print(len(tem))
          for i in range(len(tem)):
            await message.channel.send(tem[i])
        
          for i in filelist:
              #print(i)
              await message.channel.send(file=discord.File(i))

    if message.content == "m" or message.content == "mail":
        path = 'temp'
        file = open(path, 'r')
        filetxt = file.read()
        file.close()
        tmpmsg = await message.channel.send('正在取得EMAIL資訊')
        tem = mail.check()
        num,tem,filelist = mail.catch(tem)
       
        if int(filetxt) != int(num):
          file = open(path, 'w')
          await tmpmsg.delete()
          await message.channel.send(tem)

          print(len(tem))
          for i in range(len(tem)):
            await message.channel.send(tem[i])

          file.write(str(num))
          file.close()

        else:
          await tmpmsg.delete()
          tmpmsg1 = await message.channel.send('目前已更新最新資訊(本訊息5秒後自動刪除)')
          await asyncio.sleep(5)
          await tmpmsg1.delete()

    if message.content == "relaod" or message.content == "r":
        tmpmsg = await message.channel.send('正在取得與重新列出EMAIL')
        temp = mail.check()
        for k in range(1,temp):
          num,tem,filelist = mail.catch(k)
          print(len(tem))
          for i in range(len(tem)):
            await message.channel.send(tem[i])

          for i in filelist:
            #print(i)
            await message.channel.send(file=discord.File(i))
            
        await tmpmsg.delete()

    if message.content.startswith('!'):
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("!")
      else:
        await message.channel.send(tmp[1])

    if message.content.startswith('?'):
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("?")
      else:
        await message.channel.send("???")

client.run(config.TOKEN,reconnect=True)
