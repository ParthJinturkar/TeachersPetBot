import logging
import os
import discord
from discord import Intents
from discord.ext import commands
from discord.utils import get
from discord_components import DiscordComponents
from dotenv import load_dotenv
from src import profanity, db, office_hours, cal

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv("GUILD")

intents = Intents.all()
bot = commands.Bot(command_prefix='!', description='This is TeachersPetBot!', intents=intents)


@bot.event
async def on_ready():
    """
    Function:
        on_ready
    Description:
        Runs when the bot starts up
    Input:
        None
    Output:
        Initialization of database and cog system
    """
    DiscordComponents(bot)
    db.connect()
    db.add_Tables(db)
    guild = discord.utils.get(bot.guilds, name=GUILD)
    for guild in bot.guilds:
        await start_bot(guild)
        await create_voice_channels(guild)
    office_hours.init(bot)
    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    bot.load_extension("jishaku")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Over This Server")
    )
    print("READY!")
    await cal.init(bot)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_guild_join(guild):
    """
    Function:
        on_guild_join
    Description:
        Runs when the bot joins a guild (server)
    Input:
        guild - the server that the bot is added into
    Output:
        Sends welcome message, create roles and channels
    """
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
    await start_bot(guild)
    await create_voice_channels(guild)


@bot.event
async def on_message(message):
    """
     Function:
         on_message
     Description:
         Runs when a message is sent to the server. Checks for profanity.
     Input:
         message - the message a user sent to a channel of the server
     Output:
         Deletes inappropriate messages
     """

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


@bot.event
async def on_message_edit(before, after):
    """
    Function:
        on_message_edit
    Description:
        Run when a user edits a message. Checks for profanity.
    Input:
        - before: the old message
        - after: the new message
    Output:
        Deletes inappropriate messages
    """
    if profanity.check_profanity(after.content):
        await after.channel.send(after.author.name + ' says: ' +
                                 profanity.censor_profanity(after.content))
        await after.delete()


@bot.command(name="shutdown", help="Shuts down the bot, only usable by the owner")
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    """
    Function:
        shutdown
    Description:
        Shuts down the bot. Can only be used by server owner.
    Input:
        ctx - current context
    Output:
        Deletes the database and sends a message indicating successful shutdown
    """
    db.shutdown()
    await ctx.send('Shutting Down bot')
    print("Bot closed successfully")
    ctx.bot.logout()
    db.delete_db()
    exit()


async def start_bot(guild):
    """
    Function:
        start_bot
    Description:
        Run when the bot starts or when a new guild (server) is added
    Input:
        - guild : the server the bot is added to
    Output:
        Creates roles and create text channels
    """
    print("Bot is now online")
    check = False

    for role in guild.roles:
        if role.name == "Instructor":
            check = True

            check2 = False

            for role2 in guild.owner.roles:
                if role2.name == "Instructor":
                    check2 = True
                    break

            if not check2:
                await guild.owner.add_roles(role, reason=None, atomic=True)
            break

    if not check:
        role = await guild.create_role(name="Instructor", colour=discord.Colour(0x0062ff),
                                       permissions=discord.Permissions.all())
        await guild.owner.add_roles(role, reason=None, atomic=True)

    check = False

    for channel in guild.text_channels:
        if channel.name == "q-and-a":
            check = True
            break
    if not check:
        await guild.create_text_channel('q-and-a')


async def create_voice_channels(guild):
    """
    Function:
        create_voice_channels
    Description:
        Creates voice channels
    Input:
        - server in which voice channels are created
    Output:
        - create voice channels with limits for the number of users in that channel
    """

    for channel in guild.voice_channels:
        if channel.category is not None and (channel.category.name != 'General Office Hours' or channel.category.name != 'Teams'):
            await channel.delete()

    for cat in guild.categories:
        if cat.name == 'General Office Hours' or cat.name == 'Groups' or cat.name == 'Teams' or cat.name == 'TA Office Hours':

            await cat.delete()

    await guild.create_category_channel("TA Office Hours")

    category = await guild.create_category("General Office Hours")
    await guild.create_voice_channel("General Office Hours", user_limit=2, category=category)

    category2 = await guild.create_category("Teams")
    for i in range(1, 41):
        await guild.create_voice_channel("Group " + str(i), user_limit=6, category=category2)

''' run bot command '''
bot.run(TOKEN)
