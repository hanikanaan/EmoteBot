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

  if db['responding'] == 'true':
    curr_msg = msg.content
    curr_msg.replace('+', '', 1)
    curr_msg = curr_msg.split(' ')
    for a in curr_msg:
      if a.lower() == 'surely':
        await msg.channel.send(db['Clueless'])
        return
      elif a in db.keys() and a != 'responding':
        await msg.channel.send(db[a])
        return

    if msg.content.startswith('+'):
      curr = msg.content.replace('+', '', 1)
      curr = curr.split(' ')
      if curr[0] in db.keys():
        await msg.channel.send('This emote is already available in the database')
        return
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

    if msg.content.startswith('-'):
      curr = msg.content.replace('-', '', 1)
      curr = curr.split(' ')
      if curr[0] in db.keys():
        del db[curr[0]]
        await msg.channel.send(f'Removed emote from database: {curr[0]} :wave:')
  
  if msg.content.startswith('!help EmoteBot'):
    await msg.channel.send('Welcome to EmoteBot! This bot will read your messages and see if there is an emote reference in it, and if there is it will send the corresponding emote as per the database.')
    await msg.channel.send('To add a new emote, write "+*EmoteName* *EmotePictureLink*". Note that if the emote is a gif emote you will have to add the .gif extension to the end.')
    await msg.channel.send('To see the list of preexisting emotes, type !list.')
    await msg.channel.send('To turn off the bot, type "$responding false", and to turn it back on type "$responding true."')

keep_alive()
client.run(os.getenv("TOKEN"))
