# DiegoBotv0.1
# Author: n0bs (code@n0bs.me)
# Custom bot for Indy Social Discord
# Current feature list:
# - Remove/add roles based by matching specific reactions to specific messages against list of role IDs.

import os
import discord
from reader import Reader

config = Reader()
print(config.mcount)
print(config.channel)
print(config.messages)
print(config.data)

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a specific reaction to a specific message."""
        
        #Variable to keep track of whether or not we found a role match for this react event.
        match = False
        
        # Make sure that the channel the user is reacting in is the one we care about.
        if payload.channel_id != int(config.channel):
            return
        
        # Print reaction payload's message ID and emoji as debug mesages to console.
        print('Added',payload.message_id,payload.emoji)
        
        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return
        
        #This first for/if pair checks if the payload message ID matches any of the
        #message IDs defined in the configuration file.
        for x in range(config.mcount):
            if payload.message_id == int(config.messages[x,0]):
                #This second for/if pair checks if the payload emoji matches any of the emoji/reaction
                #pairs defined in the configuration file for the message we matched for.
                for y in range(20):
                    if str(payload.emoji) == str(config.data[x,0,y]):
                        match = True
                        role_id = int(config.data[x,1,y])

        #If we did not find a match, exit the function
        if match == False:
            print('No match')
            return
        
        # Print obtained role ID to console for debugging.
        print('Role:',role_id)
            
        # Make sure the role exists and is valid.
        role = guild.get_role(role_id)
        if role is None:
            return
        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a specific reaction to a specific message."""
        
        #Variable to keep track of whether or not we found a role match for this react event.
        match = False

        # Make sure that the channel the user is reacting in is the one we care about.
        if payload.channel_id != int(config.channel):
            return
        
        # Print reaction payload's message ID and emoji as debug mesages to console.
        print('Removed',payload.message_id,payload.emoji)

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return
            
        #This first for/if pair checks if the payload message ID matches any of the
        #message IDs defined in the configuration file.
        for x in range(config.mcount):
            if payload.message_id == int(config.messages[x,0]):
                #This second for/if pair checks if the payload emoji matches any of the emoji/reaction
                #pairs defined in the configuration file for the message we matched for.
                for y in range(20):
                    if str(payload.emoji) == str(config.data[x,0,y]):
                        match = True
                        role_id = int(config.data[x,1,y])

        #If we did not find a match, exit the function
        if match == False:
            print('No match')
            return

        # Print obtained role ID to console for debugging.
        print('Role:', role_id)

        # Make sure the role still exists and is valid.
        role = guild.get_role(role_id)
        if role is None:
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(os.environ['TOKEN'])