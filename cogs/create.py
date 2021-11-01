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

    @commands.command(name='take', help='Create a create events from csv file.')
    # @commands.dm_only()
    @commands.has_role('Instructor')
    async def take_events(self, ctx):
        ''' run event creation interface '''
        TESTING_MODE = False
        await ctx.message.attachments[0].save(
            'data/events/' + str(ctx.message.guild.id) + '/' + ctx.message.attachments[0].filename)

        while True:
            if os.path.exists('data/events/' + ctx.message.attachments[0].filename):
                break

        if ctx.message.attachments[0].filename.endswith('.csv'):
            if ctx.message.attachments[0].filename.startswith('exams'):
                await event_creation.read_exams(ctx)

            if ctx.message.attachments[0].filename.startswith('assignments'):
                await event_creation.read_assignments(ctx)

            # if ctx.message.attachments[0].filename.startswith('ta_office_hours'):
            #     await event_creation.read_assignments(ctx)

    @commands.command(name='eventcsv', help='Create a create events from csv file.')
    @commands.has_role('Instructor')
    async def get_event_sample_csv(self, ctx):
        ''' run event creation interface '''
        await ctx.send(file=discord.File(r'data\sample_event_csv_files\exams.csv'))
        await ctx.send(file=discord.File(r'data\sample_event_csv_files\assignments.csv'))
        await ctx.send(file=discord.File(r'data\sample_event_csv_files\ta_office_hours.csv'))


# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    bot.add_cog(Create(bot))

# Copyright (c) 2021 War-Keeper
