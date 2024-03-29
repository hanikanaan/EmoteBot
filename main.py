import discord
import os
from replit import db
from keep_alive import keep_alive
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


client = discord.Client()


@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(msg) -> None:
    if msg.author == client.user:
        return

    if str(msg.guild.id) in db.keys():
        pass
    else:
        server_init(str(msg.guild.id))

    validate = URLValidator()
    if msg.content.startswith('$responding'):
        curr = msg.content.split(' ')
        if len(curr) == 1:
            await msg.channel.send(f'Current response status: {db[str(msg.guild.id)]["status"]}')
        else:
            status = curr[1].lower()
            if status == 'true' or status == 'false':
                if status == 'false' and status != db[str(msg.guild.id)]['status']:
                    db[str(msg.guild.id)]["status"] = False
                    await msg.channel.send(f'Changed status to {db[str(msg.guild.id)]["status"]}.')
                elif status == 'true' and status != db[str(msg.guild.id)]["status"]:
                    db[str(msg.guild.id)]["status"] = True
                    await msg.channel.send(f'Changed status to {db[str(msg.guild.id)]["status"]}.')
                else:
                    await msg.channel.send('No new status update.')
            else:
                await msg.channel.send('Invalid response status, please enter "true" or "false".')
        return

    if db[str(msg.guild.id)]["status"]:
        if len(db[str(msg.guild.id)].keys()) <= 200:
            if msg.content.startswith('$add'):
                curr = msg.content.replace('$add ', '', 1)
                curr = curr.split(' ')
                if curr[0] in db.keys():
                    await msg.channel.send(
                        'This emote is already available in the database as a global emote. You can use it without adding '
                        'to your server.')
                else:
                    try:
                        validate(curr[1])
                        db[str(msg.guild.id)][curr[0]] = curr[1] + '.gif'
                        await msg.channel.send(f'Added emote to database: {curr[0]}')
                        return
                    except ValidationError:
                        await msg.channel.send('Invalid link provided.')
                    except IndexError:
                        await msg.channel.send('Link not provided, no addition made.')
                return
        else:
            await msg.channel.send('You are at the maximum capacity of emotes (200). To add more, please use the '
            '"-*EmoteName*" command, or to change a preexisting emote use the "$replace *EmoteName* *EmotePictureLink*" '
            'command.')

        if msg.content.startswith('$list all'):
            await msg.channel.send('**Local emotes:**')
            for a in db[str(msg.guild.id)].keys():
                if a != "status":
                    await msg.channel.send(f'{a} emote: {db[str(msg.guild.id)][a]}')
                else:
                    pass
            await msg.channel.send('**Global emotes:**')
            for a in db.keys():
                if not a.isnumeric():
                    await msg.channel.send(f'{a} emote: {db[a]}')
            return

        if msg.content.startswith('$list local'):
            for a in db[str(msg.guild.id)].keys():
                if a != "status":
                    await msg.channel.send(f'{a} emote: {db[str(msg.guild.id)][a]}')
                else:
                    pass
        
        if msg.content.startswith('$list global'):
            for a in db.keys():
                if not a.isnumeric():
                    await msg.channel.send(f'{a} emote: {db[a]}')

        if msg.content.startswith('$update'):
            curr = msg.content.replace('$update ', '', 1)
            curr = curr.split(' ')
            if len(curr) == 2:
                if curr[0] in db[str(msg.guild.id)].keys():
                    try:
                        validate(curr[1])
                        db[str(msg.guild.id)][curr[0]] = curr[1] + '.gif'
                        await msg.channel.send(f'Replaced emote {curr[0]} in database')
                        await msg.channel.send(db[str(msg.guild.id)][curr[0]])
                        return
                    except IndexError:
                        await msg.channel.send('Link not provided, no addition made.')
                        return
                    except ValidationError:
                        await msg.channel.send('Invalid image link provided.')
                        return
                else:
                    await msg.channel.send(
                        'Emote does not exist in the database, please use +*EmoteName* *EmotePictureLink*.')
                    return
            else:
                await msg.channel.send(
                    'Missing required argument(s) for database entry. Please make sure to provide both an emote name and the link to the image you would like to use for it.')
            return

        if msg.content.startswith('$remove'):
            curr = msg.content.replace('$remove ', '', 1)
            curr = curr.split(' ')
            if curr[0] in db[str(msg.guild.id)].keys():
                del db[str(msg.guild.id)][curr[0]]
                await msg.channel.send(f'Removed emote from database: {curr[0]} :wave:')
                return
            elif curr[0] == '':
                await msg.channel.send('No entry provided for emote to be removed. Please make sure that the emote name provided is in the database and is length greater than 0.')
            else:
                await msg.channel.send('This emote is not available in the database and so no removal was made.')
                return

        if msg.content.startswith('+global'):
            curr = msg.content.replace('+global ', '', 1)
            curr = curr.split(' ')
            try:
                print(curr[1])
                validate(curr[1])
            except IndexError:
                await msg.channel.send('Link not provided, no addition made.')
                return
            except ValidationError:
                await msg.channel.send('Invalid link provided.')
                return
            for a in db.keys():
                if curr[0] in db[a]:
                    del db[a][curr[0]]
                    db[curr[0]] = curr[1] + '.gif'
                    await msg.channel.send(f'Global emote {curr[0]} replaced a local emote with the same name.')
                    return
            if curr[0] in db.keys():
                await msg.channel.send('This global emote is already available in the database. To replace it, '
                'please use the $replace global function.')
            else:
                db[curr[0]] = curr[1] + '.gif'
                await msg.channel.send(f'Global emote {curr[0]} added.')
            return

        if msg.content.startswith('-global'):
            curr = msg.content.split(' ')
            if curr[1] in db.keys():
                del db[curr[1]]
                await msg.channel.send(f'Removed global emote from database: {curr[1]} :wave:')
                return
            elif len(curr) == 1:
                await msg.channel.send('No emote specified to be removed from global emote database.')
            else:
                await msg.channel.send('The provided emote is not available in the global emotes database. Please '
                'use the "-*EmoteName*" function to remove the emote from your server.')
                return

        if msg.content.startswith('$replace global'):
            curr = msg.content.replace('$replace global ', '', 1)
            curr = curr.split(' ')
            if curr[0] in db.keys() and not curr[0].isnumeric():
                try:
                    validate(curr[1])
                    db[curr[0]] = curr[1] + '.gif'
                    await msg.channel.send(f'Replaced emote {curr[0]} in the global emote database.')
                    return
                except ValidationError:
                    await msg.channel.send('Invalid link provided.')
                    return
                except IndexError:
                    await msg.channel.send('Link not provided, no addition made.')
                    return
            else:
                await msg.channel.send('This emote is not in the global database. If the emote is in your local database then use $update to replace it.')
                return
        curr_msg = msg.content
        curr_msg = curr_msg.split(' ')
        for a in curr_msg:
            if a.lower() == 'surely':
                await msg.channel.send(db['Clueless'])
                return
            elif a in db.keys() and not a.isnumeric():
                await msg.channel.send(db[a])
                return
            elif a in db[str(msg.guild.id)].keys():
                await msg.channel.send(db[str(msg.guild.id)][a])
                return
    else:
        await msg.channel.send('EmoteBot is currently disabled. Use comand "$responding true" to reactivate.')

    if msg.content.startswith('$num'):
        await msg.channel.send(f'{len(db[str(msg.guild.id)].keys())} local emotes in use. {200 - len(db[str(msg.guild.id)].keys())} slots still available.')

    if msg.content.startswith('!help'):
        await msg.channel.send('**Welcome to EmoteBot! This bot will read your messages and see if there is an emote '
                               'reference in it, and if there is it will send the corresponding emote as per the '
                               'database**.\n     -> To add a new emote, write "$add *EmoteName* *EmotePictureLink*".\n     '
                               '-> To replace a preexisting emote, write "$update *EmoteName* *EmotePictureLink*".\n     '
                               '-> To see the list of preexisting emotes, type $list all to list all the emotes, $list global to list global emotes only, and $list local'
                               ' to list local emotes only.\n     '
                               '-> To turn off the bot for this server, write "$responding false", and to turn it back '
                               'on, write ''"$responding true". If you are unsure of current bot status, type '
                               '"$responding".\n     -> To see the total number of server emotes the current server has, use the command "$num".')
        return


def server_init(serverid: str) -> None:
    db[serverid] = {
        'status': True
    }


keep_alive()
client.run(os.getenv("TOKEN"))
