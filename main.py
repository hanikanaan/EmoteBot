import discord
import os
from replit import db
from keep_alive import keep_alive

client = discord.Client()
db['responding'] = 'true'

@client.event
async def on_ready():
  print("logged in as {0.user}".format(client))

@client.event
async def on_message(msg):

  if msg.author == client.user:
    return

  if msg.content.startswith('$responding'):
    curr = msg.content.split(' ')
    
    if len(curr) == 1:
      await msg.channel.send(f'Current response status: {db["responding"]}')
    else:
      status = curr[1].lower()
      if status == 'true' or status == 'false':
        if status == 'false' and status != db['responding']:
          db['responding'] = 'false'
          await msg.channel.send(f'Changed status to {db["responding"]}.')
        elif status == 'true' and status != db['responding']:
          db['responding'] = 'true'
          await msg.channel.send(f'Changed status to {db["responding"]}.')
        else:
          await msg.channel.send('No new status update.')
      else:
        await msg.channel.send('Invalid response status, please enter "true" or "false".')
    return

  if db['responding'] == 'true':
    if msg.content.startswith('+'):
      curr = msg.content.replace('+', '', 1)
      curr = curr.split(' ')
      if curr[0] in db.keys():
        await msg.channel.send('This emote is already available in the database, if you would like to update it please use the $replace command.')
      else:
        try:
          link_check = curr[1][0:4]
        except IndexError:
          await msg.channel.send('Link not provided, no addition made.')
        try:
          if link_check == 'http':
            db[curr[0]] = curr[1]+ '.gif'
            await msg.channel.send(f'Added emote to database: {curr[0]}')
          else:
            await msg.channel.send('Invalid link')
            pass
        except ValueError:
          await msg.channel.send('Invalid link')
      return
        
    if msg.content.startswith('!list'):
      for a in db.keys():
        if a != 'responding':
          await msg.channel.send(f'{a} emote: {db[a]}')
        else:
          pass
      return
    
    if msg.content.startswith('$replace'):
      curr = msg.content.split(' ')
      if len(curr) == 3:
        if curr[1] in db.keys():
          link_check = curr[2][0:4]
          if link_check == 'http':
            db[curr[1]] = curr[2] + '.gif'
            await msg.channel.send(f'Replaced emote {curr[1]} in database')
            await msg.channel.send(db[curr[1]])
          else:
            await msg.channel.send('Invalid image link provided.')
        else:
          await msg.channel.send('Emote does not exist in the database, please use +*EmoteName* *EmotePictureLink*.')
      else:
        await msg.channel.send('Missing required argument for database entry. Please make sure to provide both an emote name and the link to the image you would like to use for it.')
      return
    
    curr_msg = msg.content.split(' ')
    for a in curr_msg:
      if a.lower() == 'surely':
        await msg.channel.send(db['Clueless'])
      elif a in db.keys() and a != 'responding':
        await msg.channel.send(db[a])
      return

    if msg.content.startswith('-'):
      curr = msg.content.replace('-', '', 1)
      curr = curr.split(' ')
      if curr[0] in db.keys():
        del db[curr[0]]
        await msg.channel.send(f'Removed emote from database: {curr[0]} :wave:')
      return
  
  if msg.content.startswith('!help'):
    await msg.channel.send('Welcome to EmoteBot! This bot will read your messages and see if there is an emote reference in it, and if there is it will send the corresponding emote as per the database.')
    await msg.channel.send('To add a new emote, write "+*EmoteName* *EmotePictureLink*".')
    await msg.channel.send('To replace a preexisting emote, write "$replace *EmoteName* *EmotePictureLink*".')
    await msg.channel.send('To see the list of preexisting emotes, type !list.')
    return

keep_alive()
client.run(os.getenv("TOKEN"))
