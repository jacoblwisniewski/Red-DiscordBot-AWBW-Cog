# Red-DiscordBot-AWBW-Cog
Cog for Red-DiscordBot to interact with Advance Wars By Web.

https://awbw.amarriner.com

## Setup TLDR
This cog is not currently published so you will have to manually set it up on your bot.

1. Clone the advancewarsbyweb directory from Github.
```
git clone https://github.com/jacoblwisniewski/Red-DiscordBot-AWBW-Cog.git
```

2. On your bot, create a directory to hold manually installed cogs if you do not have one already.
```
mkdir ~/cogs
```

3. Copy the advancewarsbyweb directory to the cogs folder you created
```
cp -r Red-DiscordBot-AWBW-Cog/advancewarsbyweb/ ~/cogs/
```

4. In a Discord server with your bot (or via DMs), send a message to add the path to the cogs folder you created.
You must use the full path.
```
# My bot is on EC2 and this is the full path. You can find the path with the pwd command on the bot if needed.
!addpath /home/ec2-user/cogs
```

5. Load the advancewarsbyweb cog by messaging your bot in discord.
```
!load advancewarsbyweb
```

All done!

## Logs
My bot is on EC2 and logs can be grabbed using journal.

While SSH'd to the bot:
```
journalctl -u red@Discord_Bot.service
```

## Commands
Message the bot on discord for help with the commands. 

The parent command is "awbw".

Just using the base command should show the help screen.

In Discord:
```
!awbw
```