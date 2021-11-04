# Copyright (c) 2021 War-Keeper
import discord
from discord.utils import get
from discord.ext import commands


# -----------------------------------------------------------------------
# A basic "Hello World!" command, used to verify basic bot functionality
# -----------------------------------------------------------------------
class setInstructor(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ###########################
    # Function: set_instructor
    # Description: Command used to give Instructor role out by instructors
    # Inputs:
    #      - ctx: context of the command
    #      - member: user to give role
    # Outputs:
    #      - Sends confirmation back to channel
    ###########################
    @commands.command(name='setInstructor', help='Set member to Instructor.')
    @commands.has_role('Instructor')
    async def set_instructor(self, ctx, member_name: str = None):
        ''' set instructor role command '''
        if member_name is None:
            await ctx.send('To use the setInstructor command, do: !setInstructor DISCORDNAME \n ( For example: !setInstructor Steve )')
            return
        guild = ctx.guild
        member = ctx.guild.get_member_named(member_name)  # finding member using member id
        if member:
            irole = get(guild.roles, name='Instructor')
            await member.add_roles(irole, reason=None, atomic=True)
            await ctx.channel.send(member.name + " has been given Instructor role!")
        else:
            await ctx.send("Could not find a member with that name")
            return

    @set_instructor.error
    async def set_instructor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                'To use the setInstructor command, do: !setInstructor DISCORDNAME \n ( For example: !setInstructor Steve )')


# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    bot.add_cog(setInstructor(bot))
