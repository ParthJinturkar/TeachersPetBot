# Copyright (c) 2021 War-Keeper
import discord
from discord.utils import get
from discord.ext import commands


# -----------------------------------------------------------------------
# A basic "Hello World!" command, used to verify basic bot functionality
# -----------------------------------------------------------------------
class Helpful(commands.Cog):

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
    @commands.command(name='setInstructor.py', help='Set member to Instructor.')
    @commands.has_role('Instructor')
    async def set_instructor(ctx, member: discord.Member):
        ''' set instructor role command '''
        irole = get(ctx.guild.roles, name='Instructor')
        await member.add_roles(irole, reason=None, atomic=True)
        await ctx.channel.send(member.name + " has been given Instructor role!")


# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    bot.add_cog(Helpful(bot))