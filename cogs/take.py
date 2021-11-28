import csv
import os

import discord
from discord.ext import commands

# ----------------------------------------------------------------------------------------------
# Returns the ping of the bot, useful for testing bot lag and as a simple functionality command
# ----------------------------------------------------------------------------------------------
from src import cal, db


class Create(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ImportEvents', help='Create a create events from csv file.')
    # @commands.dm_only()
    @commands.has_role('Instructor')
    async def ImportEvents(self, ctx):
        try:
            ''' run event creation interface '''
            temp = 'data/events/' + str(ctx.message.guild.id)

            if not os.path.exists(temp):
                os.makedirs(temp)

            # Ask for a file if there are no attachments in the initital message
            if len(ctx.message.attachments) == 0:
                pass

            await ctx.message.attachments[0].save(
                temp + '/' + ctx.message.attachments[0].filename)

            while True:
                if os.path.exists(temp + '/' + ctx.message.attachments[0].filename):
                    break

            if ctx.message.attachments[0].filename.endswith('.csv'):
                if ctx.message.attachments[0].filename.startswith('exams'):
                    await self.read_exams(ctx)

                if ctx.message.attachments[0].filename.startswith('assignments'):
                    await self.read_assignments(ctx)
        except Exception as e:
            print(e)
            # if ctx.message.attachments[0].filename.startswith('ta_office_hours'):
            #     await event_creation.read_assignments(ctx)

    @commands.command(name='templates', help='Get file templates for creating events from csv file.')
    @commands.has_role('Instructor')
    async def get_event_sample_csv(self, ctx):
        ''' run event creation interface '''
        await ctx.send(file=discord.File(r'data\sample_event_csv_files\exams.csv'))
        await ctx.send(file=discord.File(r'data\sample_event_csv_files\assignments.csv'))
        await ctx.send(file=discord.File(r'data\sample_event_csv_files\ta_office_hours.csv'))

    async def read_exams(self, ctx):
        temp = 'data/events/' + str(ctx.message.guild.id) + '/'
        with open(temp + 'exams.csv', mode='r') as f:
            reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in reader:
                if line_count > 1:
                    print(f'Testing {", ".join(row)}')
                    db.mutation_query(
                        'INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        [ctx.guild.id, row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
                    )
                line_count += 1
        await ctx.send('File Submitted and Exams successfully created!')

        for guild in self.bot.guilds:
            if guild.id == ctx.guild.id:
                for channel in guild.text_channels:
                    if channel.name == 'course-calendar':
                        await channel.delete()

                channel = await guild.create_text_channel('course-calendar')
                await cal.display_events(channel)

    async def read_assignments(self, ctx):
        temp = 'data/events/' + str(ctx.message.guild.id) + '/'
        with open(temp + 'assignments.csv', mode='r') as f:
            reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in reader:
                if line_count > 1:
                    print(f'Testing {", ".join(row)}')
                    db.mutation_query(
                        'INSERT INTO assignments VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        [ctx.guild.id, row[0], row[1], row[2], row[3], row[4], row[5]]
                    )
                line_count += 1
        await ctx.send('File Submitted and Assignments successfully created!')
        for guild in self.bot.guilds:
            if guild.id == ctx.guild.id:
                for channel in guild.text_channels:
                    if channel.name == 'course-calendar':
                        await channel.delete()

                channel = await guild.create_text_channel('course-calendar')
                await cal.display_events(channel)


# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    bot.add_cog(Create(bot))

# Copyright (c) 2021 War-Keeper
