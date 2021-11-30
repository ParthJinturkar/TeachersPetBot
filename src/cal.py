from datetime import datetime
import discord
from src import db

BOT = None
CALENDAR_EMBED = None
MSG = None



async def display_events(ctx):
    """
    Function:
        display_events
    Description:
        Sends or updates the embed for the calendar
    Inputs:
        - ctx: context of function activation
    """
    global MSG

    # recreate the embed from the database
    update_calendar()

    # if it was never created, send the first message
    if MSG is None:
        MSG = await ctx.send(embed=CALENDAR_EMBED)
    else:
        # otherwise, delete the existing calender
        async for msg in MSG.channel.history(limit=2):
            await msg.delete()
        # Adding the updated calender
        await MSG.channel.send(embed=CALENDAR_EMBED)



def update_calendar():
    """
    Function:
        update_calendar
    Description:
        Builds the calendar embed
    """
    global CALENDAR_EMBED

    # create an Embed with a title and description of color 'currently BLUE'
    CALENDAR_EMBED = discord.Embed(title="The Course Calendar, sire",
                                   description="All of the class assignments and exams!", color=0x0000FF)

    # make a list that contains the string representing the
    # event that has the comparison item as the first index
    # which is the date, we are comparing as strings but still works for ordering events by date
    # do this for the events we care about in the calendar 'assignments, exams, and custom events'
    assignments = []
    for title, link, desc, date, due_hr, due_min in db.select_query(
            'SELECT ' +
            'title, link, desc, date, due_hr, due_min ' +
            'FROM ' +
            'assignments ' +
            'ORDER BY ' +
            'date ASC, ' +
            'due_hr ASC, ' +
            'due_min ASC'):
        assignments.append([f'{date} {due_hr}:{due_min}',
                            f'{date} {due_hr}:{due_min}\n{title}\n{desc}\n{link}\n\n'])

    exams = []
    for title, desc, date, begin_hr, begin_min, end_hr, end_min in db.select_query(
            'SELECT ' +
            'title, desc, date, begin_hr, begin_min, end_hr, end_min ' +
            'FROM ' +
            'exams ' +
            'ORDER BY ' +
            'date ASC, ' +
            'begin_hr ASC, '
            'begin_min ASC'):
        exams.append([f'{date} {begin_hr}:{begin_min}',
                      f'{date} {begin_hr}:{begin_min} - {end_hr}:{end_min}\n{title}\n{desc}\n\n'])

    custom_events = []
    for title, link, desc, date, due_hr, due_min, begin_hr, begin_min, end_hr, end_min in db.select_query(
            'SELECT ' +
            'title, link, desc, date, due_hr, due_min, begin_hr, begin_min, end_hr, end_min ' +
            'FROM ' +
            'custom_events ' +
            'ORDER BY ' +
            'date ASC, ' +
            'due_hr ASC, '
            'due_min ASC, '
            'begin_hr ASC, '
            'begin_min ASC'):
        custom_events.append([f'{date} {due_hr}:{due_min}\n'
                              f'{begin_hr}:{begin_min} - {end_hr}:{end_min}\n{title}\n{desc}\n\n'])

    # get current time for comparison and make sure it is of same string format
    current_time = datetime.now().strftime('%m-%d-%Y %H:%M')
    # Time in EST: 2017-01-19 08:06:14

    special_events = ''
    if len(custom_events) == 0:
        special_events = "No special events"
    else:
        for each in custom_events:
            special_events += each[0]

    CALENDAR_EMBED.add_field(name="Special Events", value=special_events, inline=True)

    i = 0
    j = 0

    # 2 lists for fields in the calendar
    past_events = ''
    # current_events = ''
    future_events = ''

    # go through the sorted lists and take the earliest date,
    # moving the index of each until all lists are placed
    # into one of the defined areas
    while i != len(exams) or j != len(assignments):
        if i == len(exams) or (j != len(assignments) and assignments[j][0] < exams[i][0]):
            if assignments[j][0] < current_time:
                past_events += assignments[j][1]
            else:
                future_events += assignments[j][1]
            j += 1
        else:
            if exams[i][0] < current_time:
                past_events += exams[i][1]
            else:
                future_events += exams[i][1]
            i += 1

    # add the built strings to the embed
    if past_events != '':
        CALENDAR_EMBED.add_field(name="Past Events", value=past_events, inline=True)

    # CALENDAR_EMBED.add_field(name="Current Events", value=events, inline=False)

    if future_events != '':
        CALENDAR_EMBED.add_field(name="Coming up", value=future_events, inline=True)

    # mark the time that this was done for both creation and editing
    # NOTE - we put in EST because we are EST
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' EST'
    CALENDAR_EMBED.set_footer(text=f"{time_now}")



async def init(b):
    """
    Function:
        init
    Description:
        Initializes the calendar, creating channel and embed call
    Inputs:
         - b: bot
    """
    global BOT

    BOT = b
    for guild in BOT.guilds:
        for channel in guild.text_channels:
            if channel.name == 'course-calendar':
                await channel.delete()

        channel = await guild.create_text_channel('course-calendar')
        await display_events(channel)
