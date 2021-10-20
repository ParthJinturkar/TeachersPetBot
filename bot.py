import os
import logging
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from discord_components import DiscordComponents
from discord.ext.commands import Bot
from discord import Intents
from src import profanity


logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD = os.getenv("GUILD")
# GUILD = 'TeachersPet-Dev'

intents = Intents.all()
bot = commands.Bot(command_prefix='!', description='This is TeachersPetBot!', intents=intents)



###########################
# Function: on_ready
# Description: run on bot start-up
###########################
@bot.event
async def on_ready():
    ''' run on bot start-up '''
    # DiscordComponents(bot)
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )


    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Over This Server")
    )
    print("READY!")

    # event_creation.init(bot)
    # office_hours.init(bot)
    # await cal.init(bot)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    ###########################
    # Function: on_guild_join
    # Description: run when a user joins a guild with the bot present
    # Inputs:
    #      - guild: the guild the user joined from
    ###########################
    @ bot.event
    async def on_guild_join(guild):
        ''' run on member joining guild '''
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send('Hi there, I\'m TeachersPetBot, and I\'m here' +
                                   ' to help you manage your class discord! Let\'s do some quick setup. ')
                # create roles if they don't exist
                if 'Instructor' in guild.roles:
                    await channel.send("Instructor Role already exists")
                else:
                    await guild.create_role(name="Instructor", colour=discord.Colour(0x0062ff),
                                            permissions=discord.Permissions.all())
                # Assign Instructor role to admin
                leader = guild.owner
                leadrole = get(guild.roles, name='Instructor')
                await channel.send(leader.name + " has been given Instructor role!")
                await leader.add_roles(leadrole, reason=None, atomic=True)
                await channel.send("To assign more Instructors, type \"!setInstructor.py @<member>\"")
                # Create Text channels if they don't exist
                if 'instructor-commands' not in guild.text_channels:
                    await guild.create_text_channel('instructor-commands')
                    await channel.send("instructor-commands channel has been added!")
                if 'q-and-a' not in guild.text_channels:
                    await guild.create_text_channel('q-and-a')
                    await channel.send("q-and-a channel has been added!")
                if 'course-calendar' not in guild.text_channels:
                    await guild.create_text_channel('course-calendar')
                    await channel.send("course-calendar channel has been added!")

            break

    ###########################
    # Function: on_message
    # Description: run when a message is sent to a discord the bot occupies
    # Inputs:
    #      - message: the message the user sent to a channel
    ###########################
    @bot.event
    async def on_message(message):
        ''' run on message sent to a channel '''


        if message.author == bot.user:
            return

        if profanity.check_profanity(message.content):
            await message.channel.send(message.author.name + ' says: ' +
                                       profanity.censor_profanity(message.content))
            await message.delete()

        await bot.process_commands(message)

        if message.content == 'hey bot':
            response = 'hey yourself ;)'
            await message.channel.send(response)

    ###########################
    # Function: on_message_edit
    # Description: run when a user edits a message
    # Inputs:
    #      - before: the old message
    #      - after: the new message
    ###########################
    @bot.event
    async def on_message_edit(before, after):
        ''' run on message edited '''
        if profanity.check_profanity(after.content):
            await after.channel.send(after.author.name + ' says: ' +
                                     profanity.censor_profanity(after.content))
            await after.delete()


''' run bot command '''
bot.run(TOKEN)

