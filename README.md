# EmoteBot
Discord emote bot where users can add and remove emotes using image links, made in [replit](https://replit.com/@hanikanaan/EmoteBot)


## Invite Link:
[To invite the bot, you will need to have administrator privileges to the server and use this link.](https://discord.com/api/oauth2/authorize?client_id=923643328417906689&permissions=326417573888&scope=bot)

## Implementation:
This was done using Python (discord.py) and then hosted using [uptimerobot.com](uptimerobot.com).

## Commands (Note: EmoteName/EmotePictureLink are variables which the user will have to provide):
### $responding: 
* Global power switch for the bot (currently has to fixed such that it is a server specific status)
* If set to true, then the bot responds to all commands
* If set to false, then the bot responds only to $help EmoteBot

### $add EmoteName EmotePictureLink: 
* Add an emote to the local database
* If link is not provided, error is raised and the bot sends a message that the link was not provided
* If link is provided but invalid, error is raised and the bot sends a message that the link provided was invalid
* If user tries to add an emote which exists in the global database, they are notified that they do not need to make another version of the emote to be able to use it as it is accesssible globally
* Max number of local emotes limited to 200, error is raised if a user tries to add an emote while already at the 200 emote limit

### +global EmoteName EmotePictureLink
* Add an emote to the global database
* If link is not provided, error is raised and the bot sends a message that the link was not provided
* If link is provided but invalid, error is raised and the bot sends a message that the link provided was invalid

### $remove EmoteName: 
* Remove an emote from the database
* Only argument is the emote name

### -global EmoteName:
* Remove an emote from the global database
* Only argument is the emote name

### $list local: 
* Lists all emotes available to the server

### $list global:
* Lists all global emotes

### $list all:
* Lists all emotes in local and global databases (DOES NOT LIST OTHER SERVERS' EMOTES)

### $update: 
* Replace a preexisting local emote from the database with a different picture (e.g. holiday themed emotes)

### $replace global:
* Replace a preexisting global emote from the database with a different picture

### $num:
* Shows the number of local server emotes and how many are still available.

## Example Use:
### Adding an emote:
* Local:

![Example of adding an emote locally](https://github.com/hanikanaan/EmoteBot/blob/main/images/Adding%20local%20emote.png)
* Global:

![Example of adding an emote globally](https://github.com/hanikanaan/EmoteBot/blob/main/images/Global%20emote%20overriding%20local%20emote.png)
* Local add accessed from a different server:

![Added into server "bot"](https://github.com/hanikanaan/EmoteBot/blob/main/images/popCat%20in%20server.png)
![Attempted access from server "bot2"](https://github.com/hanikanaan/EmoteBot/blob/main/images/popCat%20outside%20server.png)
### Removing an emote:
* Local:

![Example of removing a local emote](https://github.com/hanikanaan/EmoteBot/blob/main/images/Removing%20local%20emote.png)
* Global:

![Example of removing a global emote](https://github.com/hanikanaan/EmoteBot/blob/main/images/Removing%20global%20emote.png)
### Replacing an emote:
* Global:

![Example of replacing an emote](https://github.com/hanikanaan/EmoteBot/blob/main/images/Replacing%20global%20emote.png)
* Local:

![Example of replacing local emote](https://github.com/hanikanaan/EmoteBot/blob/main/images/Update%20local%20database.png)
### Typical bot reply to emote mention
![Example of bot response](https://github.com/hanikanaan/EmoteBot/blob/main/images/Example%20using%20emote.png)
### !help command response:

![!help command response from robot](https://github.com/hanikanaan/EmoteBot/blob/main/images/Help%20command.png)
### $num command response:

![$num command response](https://github.com/hanikanaan/EmoteBot/blob/main/images/Num%20command.png)
