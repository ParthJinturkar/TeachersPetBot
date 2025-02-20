import csv
import os

import discord
from discord.ext import commands

# ----------------------------------------------------------------------------------------------
# Returns the ping of the bot, useful for testing bot lag and as a simple functionality command
# ----------------------------------------------------------------------------------------------
from src import event_creation


class Create(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create', help='Create a new event.')
    # @commands.dm_only()
    @commands.has_role('Instructor')
    async def create_event(self, ctx):
        """
        Function:
            create_event
        Description:
            ommand to create event and send to event_creation module
        Inputs:
            - ctx: context of the command
        Outputs:
            Options to create event
        """
        TESTING_MODE = False

        await event_creation.create_event(ctx, self.bot, False)

# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    bot.add_cog(Create(bot))

# Copyright (c) 2021 War-Keeper
