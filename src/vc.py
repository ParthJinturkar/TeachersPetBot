###########################
# Functionality for creating new events
###########################
import datetime
import os

import discord
from discord_components import Button, ButtonStyle, Select, SelectOption
import validators
from src import db
from src import utils
from src import office_hours
from src import cal


###########################
# Function: create_voice_channel
# Description: creates voice channel(s)
# Inputs:
#      - ctx: context of this discord message
# Outputs: new voice channel(s) created
###########################
async def create_voice_channel(ctx, BOT, testing_mode, channelname, catename, limit, num):
    ''' create voice channel input flow '''
    GUILD = os.getenv("GUILD")
    discord.utils.get(BOT.guilds, name=GUILD)
    # if ctx.channel.name == 'instructor-commands':
    cat_exist = False
    for guild in BOT.guilds:
        # Category
        for cat in guild.categories:
            if cat.name == catename:
                cat_exist = True
                print('exist')
                for i in range(int(num)):
                    temp = channelname + str(i + 1)
                    await guild.create_voice_channel(temp, user_limit=int(limit), category=cat)


    if not cat_exist:
        category = await guild.create_category(catename)
        print('exist')
        for i in range(int(num)):
            temp = channelname + str(i + 1)
            await ctx.guild.create_voice_channel(temp, user_limit=int(limit), category=category)

    await ctx.send("Voice channel has been created!!")
    # else:
    #     await ctx.author.send('`!voice_channel` can only be used in the `instructor-commands` channel')
    #     await ctx.message.delete()



###########################
# Function: init
# Description: initializes this module, giving it access to discord bot
# Inputs:
#      - b: discord bot
# Outputs: None
###########################

def init(b):
    ''' initialize event creation '''
    global BOT
    BOT = b
