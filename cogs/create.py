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

    ###########################
    # Function: create_event
    # Description: command to create event and send to event_creation module
    # Ensures command author is Instructor
    # Inputs:
    #      - ctx: context of the command
    # Outputs:
    #      - Options to create event
    ###########################
    @commands.command(name='create', help='Create a new event.')
    # @commands.dm_only()
    @commands.has_role('Instructor')
    async def create_event(self, ctx):
        ''' run event creation interface '''
        TESTING_MODE = False

        await event_creation.create_event(ctx, False)

# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    bot.add_cog(Create(bot))

# Copyright (c) 2021 War-Keeper
