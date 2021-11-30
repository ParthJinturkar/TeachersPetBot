import datetime
from discord_components import Button, ButtonStyle, Select, SelectOption
import validators
from src import db
from src import utils
from src import office_hours
from src import cal


async def get_times(ctx, bot, event_type):
    """
    Function:
        get_times
    Description:
        Helper function for acquiring the times an instructor wants an event to be held during
    Inputs:
        - ctx: context of the message
        - bot: discord bot object
        - event_type: type of the event
    Output:
        The begin & end times of the event
    """

    def check(m):
        return m.content is not None and m.channel == ctx.channel and m.author == ctx.author

    # Looping until a valid time is entered.
    while True:
        await ctx.send(
            'Enter in format `<begin_time>-<end_time>`, and times should be in 24-hour format.\n'
            f'For example, setting {event_type} from 9:30am to 1pm can be done as 9:30-13\n'
            + "Type 'NA' if none. Type 'quit' to abort."
        )

        msg = await bot.wait_for('message', check=check)
        user_input = msg.content

        # Checking whether user entered 'quit' or 'NA'.
        if await check_quit(ctx, user_input):
            return
        elif user_input == 'NA':
            return False

        times = msg.content.strip().split('-')
        if len(times) != 2:
            await ctx.send("Incorrect input. Please enter the time in the expected format.\n")
            continue

        new_times = []
        new_time = None
        for t in times:
            parts = t.split(':')
            if len(parts) == 1:
                new_time = (int(parts[0]), 0)
            elif len(parts) == 2:
                new_time = (int(parts[0]), int(parts[1]))
            new_times.append(new_time)

        if len(new_times) != 2:
            await ctx.send("Incorrect input. Please enter the time in the expected format.\n")
            continue
        return new_times


async def get_due_time(ctx, bot):
    """
    Function:
        get_due_time
    Description:
        Helper function for acquiring the due time of an event
    Inputs:
        - ctx: context of the message
        - bot: discord bot object
    Output:
        The begin & end times of the event
    """

    def check(m):
        return m.content is not None and m.channel == ctx.channel and m.author == ctx.author

    # Looping until a valid time is entered.
    while True:
        await ctx.send("Enter in 24-hour format. e.g. an assignment due at 11:59pm "
                       "can be inputted as 23:59. Type 'NA' if none. Type 'quit to abort.")
        msg = await bot.wait_for("message", check=check)
        time = msg.content.strip()

        # Aborting if user entered 'quit'.
        if await check_quit(ctx, time):
            return
        elif time == 'NA':
            return False

        # Checking whether the format is valid. If invalid, continue the loop.
        try:
            time = datetime.datetime.strptime(time, '%H:%M')
        except ValueError:
            try:
                time = datetime.datetime.strptime(time, '%H')
            except ValueError:
                await ctx.send("Incorrect input. Please enter the time in the expected format.\n")
                continue
        return time


async def check_quit(ctx, value):
    """
    Function:
        check_quit
    Description:
        Helper function for checking whether user entered 'quit'.
    Input:
        - ctx: context of the message
        - value: parameter that holds user input
    Output:
        True if user input is 'quit', False otherwise.
    """
    if value == 'quit':
        await ctx.send("Aborting event creation. Type '!create' to restart.")
        return True
    return False


async def get_date(ctx, bot):
    """
    Function:
        get_date
    Description:
        Helper function for acquiring the date or due date of an event
    Input:
        - ctx: context of the message
        - bot: discord bot object
    Output:
        The date or the due date of the event.
    """
    def check(m):
        return m.content is not None and m.channel == ctx.channel and m.author == ctx.author

    # Looping until a valid date is entered.
    while True:
        await ctx.send("Enter in format `MM-DD-YYYY`. Type NA if none. Type 'quit' to abort")
        msg = await bot.wait_for("message", check=check)
        date = msg.content.strip()

        # Aborting if user entered 'quit'.
        if await check_quit(ctx, date):
            return
        elif date == 'NA':
            return False

        # Checking whether the format is valid. If invalid, continue the loop.
        try:
            datetime.datetime.strptime(date, '%m-%d-%Y')
        except ValueError:
            await ctx.send("Invalid date. Please enter the date in the expected format.\n")
            continue
        return date


async def get_url(ctx, bot):
    """
    Function:
        get_url
    Description:
        Helper function for acquiring the associated url of an event
    Input:
        - ctx: context of the message
        - bot: discord bot object
    Output:
        The url associated with the event, or False if user enters 'NA'.
    """

    def check(m):
        return m.content is not None and m.channel == ctx.channel and m.author == ctx.author

    # Looping until a valid URL is entered (or 'quit'/'NA' is entered).
    while True:
        await ctx.send("Enter the URL. Type NA if none. Type 'quit' to abort.")
        msg = await bot.wait_for("message", check=check)
        link = msg.content.strip()

        if await check_quit(ctx, link):
            return
        elif link == 'NA':
            return False
        elif link and not validators.url(link):
            await ctx.send("Invalid URL. Please enter a valid URL.\n")
        else:
            return link


async def create_event(ctx, bot, testing_mode):
    """
    Function:
        create_event
    Description:
        Event creation subroutine
    Input:
        - ctx: context of the message
        - bot: discord bot object
        - testing_mode: flag indicating whether this event is being created during a system test
    Output:
        A new event is created in the database and calendar is updated with the new event.
    """
    # creating buttons for event types
    if ctx.channel.name == 'instructor-commands':
        await ctx.send(
            'Which type of event would you like to create?',
            components=[
                Button(style=ButtonStyle.blue, label='Assignment', custom_id='assignment'),
                Button(style=ButtonStyle.green, label='Exam', custom_id='exam'),
                Button(style=ButtonStyle.red, label='Office Hour', custom_id='office-hour'),
                Button(style=ButtonStyle.gray, label='Custom Event', custom_id='custom-event')
            ],
        )
        # Getting the ID of the clicked button
        button_clicked = ((await utils.wait_for_msg(bot, ctx.channel)).content
                          if testing_mode else (await bot.wait_for('button_click')).custom_id)

        # If 'Assignment' is clicked, this will run
        if button_clicked == 'assignment':
            def check(m):
                return m.content is not None and m.channel == ctx.channel and m.author == ctx.author

            await ctx.send("What would you like the assignment to be called? "
                           "(Type 'quit' to abort)")
            msg = await bot.wait_for("message", check=check)
            title = msg.content.strip()

            # Aborting if user entered 'quit'.
            if await check_quit(ctx, title):
                return

            # Getting associated url of the event.
            await ctx.send("Is there a link associated with this assignment?\n ")
            link = await get_url(ctx, bot)
            if link is None:
                return

            await ctx.send("Extra description for assignment? Type NA if none. "
                           "Type 'quit' to abort")
            msg = await bot.wait_for("message", check=check)
            description = msg.content.strip()

            # Aborting if user entered 'quit'.
            if await check_quit(ctx, description):
                return

            # Getting the due date.
            await ctx.send("What is the due date of this assignment?\n ")
            date = await get_date(ctx, bot)
            if date is None:
                return

            # Getting the due time.
            await ctx.send("What time is this assignment due?\n ")
            time = await get_due_time(ctx, bot)
            if time is None:
                return
            # If due time is entered as 'NA', this part will run
            elif not time:
                db.mutation_query(
                    'INSERT INTO assignments VALUES (?, ?, ?, ?, ?, ?, ?)',
                    [ctx.guild.id, title, link, description, date, 0, 0]
                )
                await ctx.send('Assignment successfully created!')
                await cal.display_events(None)
                return

            # If there's a valid due time, this will execute
            db.mutation_query(
                'INSERT INTO assignments VALUES (?, ?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, title, link, description, date, time.hour, time.minute]
            )

            await ctx.send('Assignment successfully created!')
            await cal.display_events(None)
            return

        # If 'exam' is clicked, this will run
        elif button_clicked == 'exam':
            def check(m):
                return m.content is not None and m.channel == ctx.channel and m.author == ctx.author

            await ctx.send("What is the title of this exam? (Type 'quit' to abort)")
            msg = await bot.wait_for("message", check=check)
            title = msg.content.strip()

            # Aborting if user entered 'quit'.
            if await check_quit(ctx, title):
                return

            await ctx.send("What content is this exam covering? (Type 'quit' to abort)")
            msg = await bot.wait_for('message', check=check)
            description = msg.content.strip()

            # Aborting if user entered 'quit'.
            if await check_quit(ctx, description):
                return

            # Getting the date.
            await ctx.send("What is the date of this exam?\n ")
            date = await get_date(ctx, bot)
            if date is None:
                return

            # Getting the exam start/end times.
            await ctx.send("Type the start & end times of the exam\n")
            times = await get_times(ctx, bot, 'exam')
            if times is None:
                return
            # This part will run if user entered 'NA'.
            elif not times:
                db.mutation_query(
                    'INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    [ctx.guild.id, title, description, date,
                     0, 0, 0, 0]
                )
                await ctx.send('Exam successfully created!')
                await cal.display_events(ctx)
                return

            ((begin_hour, begin_minute), (end_hour, end_minute)) = times
            db.mutation_query(
                'INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, title, description, date,
                 begin_hour, begin_minute, end_hour, end_minute]
            )

            await ctx.send('Exam successfully created!')
            await cal.display_events(ctx)
            return

        # If 'Office Hour' is clicked, this will run
        elif button_clicked == 'office-hour':
            # Adding instructors in the server to a list
            all_instructors = []
            for mem in ctx.guild.members:
                is_instructor = next((role.name == 'Instructor'
                                      for role in mem.roles), None) is not None
                if is_instructor:
                    all_instructors.append(mem)

            if len(all_instructors) < 1:
                await ctx.send('There are no instructors in the server. Aborting event creation.')
                return

            options = [SelectOption(label=instr.name, value=instr.name)
                       for instr in all_instructors]

            await ctx.send(
                'Which instructor will this office hour be for?',
                components=[
                    Select(
                        placeholder='Select an instructor',
                        options=options
                    )
                ]
            )

            instructor = ((await utils.wait_for_msg(bot, ctx.channel)).content
                          if testing_mode else (await bot.wait_for('select_option')).values[0])

            await ctx.send(
                'Which day would you like the office hour to be on?',
                components=[
                    Select(
                        placeholder='Select a day',
                        options=[
                            SelectOption(label='Monday', value='Mon'),
                            SelectOption(label='Tuesday', value='Tue'),
                            SelectOption(label='Wednesday', value='Wed'),
                            SelectOption(label='Thursday', value='Thu'),
                            SelectOption(label='Friday', value='Fri'),
                            SelectOption(label='Saturday', value='Sat'),
                            SelectOption(label='Sunday', value='Sun')
                        ]
                    )
                ]
            )

            day = (
                (await utils.wait_for_msg(bot, ctx.channel)).content
                if testing_mode else
                (await bot.wait_for('select_option', check=lambda x: x.values[0] in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri',
                                                                                     'Sat', 'Sun'))).values[0]
            )

            day_num = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun').index(day)

            # Looping until a valid time range is entered (or 'quit' is entered).
            await ctx.send("Type the start & end times of your office hours.\n")
            while True:
                times = await get_times(ctx, bot, 'office hour')
                if times is None:
                    return
                if not times:
                    await ctx.send("You must enter a time range for office hours\n")
                    continue
                break
            ((begin_hour, begin_minute), (end_hour, end_minute)) = times

            office_hours.add_office_hour(
                ctx.guild,
                office_hours.TaOfficeHour(
                    instructor,
                    day_num,
                    (datetime.time(hour=begin_hour, minute=begin_minute),
                     datetime.time(hour=end_hour, minute=end_minute))
                )
            )

            db.mutation_query(
                'INSERT INTO ta_office_hours VALUES (?, ?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, instructor, day_num, begin_hour, begin_minute, end_hour, end_minute]
            )

            await ctx.send('Office hour successfully created!')

        # If 'Custom Event' is clicked, this will run
        elif button_clicked == 'custom-event':
            def check(m):
                return m.content is not None and m.channel == ctx.channel and m.author == ctx.author

            await ctx.send("What would you like this event to be called? "
                           "(Type 'quit' to abort)")
            msg = await bot.wait_for("message", check=check)
            title = msg.content.strip()

            # Aborting if user entered 'quit'.
            if await check_quit(ctx, title):
                return

            await ctx.send("Extra description for the event? Type 'NA' if none. "
                           "Type 'quit' to abort")
            msg = await bot.wait_for("message", check=check)
            description = msg.content.strip()

            # Aborting if user entered 'quit'.
            if await check_quit(ctx, description):
                return

            # Getting associated url of the event.
            await ctx.send("Is there an associated link for this event?")
            link = await get_url(ctx, bot)
            if link is None:
                return

            # Getting the associated date.
            await ctx.send("Is there a date or a due date for this event?\n")
            date = await get_date(ctx, bot)
            if date is None:
                return

            # send this message if there's an associated date.
            if date:
                await ctx.send("Is there a due time for this event?\n")
                time = await get_due_time(ctx, bot)
                if time is None:
                    return
                elif time:
                    db.mutation_query(
                        'INSERT INTO custom_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        [ctx.guild.id, title, link, description, date, time.hour, time.minute, 0, 0, 0, 0]
                    )
                    await ctx.send('Event successfully created!')
                    await cal.display_events(None)
                    return

            await ctx.send("What are the start & end times of this event?\n")
            times = await get_times(ctx, bot, 'event')
            if times is None:
                return
            elif not times:
                db.mutation_query(
                    'INSERT INTO custom_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    [ctx.guild.id, title, link, description, date, 0, 0, 0, 0, 0, 0]
                )
                await ctx.send('Event successfully created!')
                await cal.display_events(None)
                return

            ((begin_hour, begin_minute), (end_hour, end_minute)) = times
            db.mutation_query(
                'INSERT INTO custom_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, title, link, description, date, 0, 0, begin_hour, begin_minute, end_hour, end_minute]
            )

            await ctx.send('Assignment successfully created!')
            await cal.display_events(None)
            return

    else:
        await ctx.author.send('`!create` can only be used in the `instructor-commands` channel')
        await ctx.message.delete()
        return
