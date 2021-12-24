# EmoteBot
Discord emote bot where users can add and remove emotes using image links.


## Invite Link:
[To invite the bot, you will need to have administrator privileges to the server and use this link.](https://discord.com/api/oauth2/authorize?client_id=923643328417906689&permissions=326417573888&scope=bot)

## Implementation:
This was done using Python (discord.py) and then hosted using [uptimerobot.com](uptimerobot.com).

## Commands (Note: EmoteName/EmotePictureLink are variables which the user will have to provide):
### $responding: 
* Global power switch for the bot (currently has to fixed such that it is a server specific status)
* If set to true, then the bot responds to all commands
* If set to false, then the bot responds only to $help EmoteBot

### +EmoteName EmotePictureLink: 
* Add an emote to the database
* If link is not provided, an error is raised and the bot sends a message that the link was invalid/not provided

### -EmoteName: 
* Remove an emote from the database
* Only argument is the emote name

### !list: 
* Lists all remotes available in the database and the images

### $replace: 
* Replace a preexisting emote from the database with a different picture (e.g. holiday themed emotes)

## Example Use:
![Example of adding an emote](https://github.com/hanikanaan/EmoteBot/blob/main/images/Example%20adding%20emote.png)
![Example of removing an emote](https://github.com/hanikanaan/EmoteBot/blob/main/images/Example%20removing%20emote.png)
![Example of replacing an emote](https://github.com/hanikanaan/EmoteBot/blob/main/images/Example%20replacement.png)
![Example of bot response](https://github.com/hanikanaan/EmoteBot/blob/main/images/Example%20using%20emote.png)
