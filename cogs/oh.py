import discord
from discord.ext import commands

# ----------------------------------------------------------------------------------------------
# Returns the ping of the bot, useful for testing bot lag and as a simple functionality command
# ----------------------------------------------------------------------------------------------
from src import office_hours


class Helpful(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='oh', help='Operations relevant for office hours.')
    async def office_hour_command(self, ctx, command, *args):
        """
        Function:
            oh
        Description:
            command related office hour and send to office_hours module
        Inputs:
            - ctx: context of the command
            - command: specific command to run
            - *args: arguments for command
        Outputs:
            Office hour details and options
        """
        await office_hours.office_hour_command(ctx, command, *args)


# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    bot.add_cog(Helpful(bot))

# Copyright (c) 2021 War-Keeper
