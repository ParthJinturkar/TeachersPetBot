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


UNVERIFIED_ROLE_NAME = os.getenv("UNVERIFIED_ROLE_NAME")

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

    ###########################
    # Function: test
    # Description: Simple test command that shows commands are working.
    # Inputs:
    #      - ctx: context of the command
    # Outputs:
    #      - Sends test successful message back to channel that called test
    ###########################
    @bot.command()
    async def test(ctx):
        ''' simple sanity check '''
        await ctx.send('test successful')

    ###########################
    # Function: set_instructor
    # Description: Command used to give Instructor role out by instructors
    # Inputs:
    #      - ctx: context of the command
    #      - member: user to give role
    # Outputs:
    #      - Sends confirmation back to channel
    ###########################
    @bot.command(name='setInstructor.py', help='Set member to Instructor.')
    @commands.has_role('Instructor')
    async def set_instructor(ctx, member: discord.Member):
        ''' set instructor role command '''
        irole = get(ctx.guild.roles, name='Instructor')
        await member.add_roles(irole, reason=None, atomic=True)
        await ctx.channel.send(member.name + " has been given Instructor role!")

    ###########################
    # Function: create_event
    # Description: command to create event and send to event_creation module
    # Ensures command author is Instructor
    # Inputs:
    #      - ctx: context of the command
    # Outputs:
    #      - Options to create event
    ###########################
    @bot.command(name='create', help='Create a new event.')
    # @commands.dm_only()
    @commands.has_role('Instructor')
    async def create_event(ctx):
        ''' run event creation interface '''


    ###########################
    # Function: oh
    # Description: command related office hour and send to office_hours module
    # Inputs:
    #      - ctx: context of the command
    #      - command: specific command to run
    #      - *args: arguments for command
    # Outputs:
    #      - Office hour details and options
    ###########################
    @bot.command(name='oh', help='Operations relevant for office hours.')
    async def office_hour_command(ctx, command, *args):
        ''' run office hour commands with various args '''


    ###########################
    # Function: ask
    # Description: command to ask question and sends to qna module
    # Inputs:
    #      - ctx: context of the command
    #      - question: question text
    # Outputs:
    #      - User question in new post
    ###########################
    @bot.command(name='ask', help='Ask question. Please put question text in quotes.')
    async def ask_question(ctx, question):
        ''' ask question command '''
        # make sure to check that this is actually being asked in the Q&A channel


    ###########################
    # Function: answer
    # Description: command to answer question and sends to qna module
    # Inputs:
    #      - ctx: context of the command
    #      - q_num: question number to answer
    #      - answer: answer text
    # Outputs:
    #      - User answer in question post
    ###########################
    @bot.command(name='answer', help='Answer specific question. Please put answer text in quotes.')
    async def answer_question(ctx, q_num, answer):
        ''' answer question command '''
        # make sure to check that this is actually being asked in the Q&A channel

    ###########################
    # Function: test_dummy
    # Description: Run the bot
    ###########################

''' run bot command '''
bot.run(TOKEN)

