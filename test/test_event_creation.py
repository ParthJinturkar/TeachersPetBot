# ###########################
# # Tests Event creation functionality
# ###########################

import discord.ext.test as dpytest
import pytest


async def test_create_assignment_valid(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('assignment')
    assert dpytest.verify().message().content('What would you like the assignment to be called')

    await dpytest.message('test')
    assert dpytest.verify().message().content('Link associated with submission? Type N/A if none')

    await dpytest.message('N/A')
    assert dpytest.verify().message().content('Extra description for assignment? Type N/A if none')

    await dpytest.message('Some stuff')
    assert dpytest.verify().message().content('What is the due date')

    await dpytest.message('01-01-1999')
    assert dpytest.verify().message().content('What time is this assignment due')

    await dpytest.message('13:37')
    assert dpytest.verify().message().content('Assignment successfully created')


async def test_create_assignment_invalid_url(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('assignment')
    assert dpytest.verify().message().content('What would you like the assignment to be called')

    await dpytest.message('test')
    assert dpytest.verify().message().content('Link associated with submission? Type N/A if none')

    await dpytest.message('Oops')
    assert dpytest.verify().message().content('Invalid URL. Aborting')


async def test_create_assignment_invalid_date(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('assignment')
    assert dpytest.verify().message().content('What would you like the assignment to be called')

    await dpytest.message('test')
    assert dpytest.verify().message().content('Link associated with submission? Type N/A if none')

    await dpytest.message('N/A')
    assert dpytest.verify().message().content('Extra description for assignment? Type N/A if none')

    await dpytest.message('Some stuff')
    assert dpytest.verify().message().content('What is the due date')

    await dpytest.message('Oops')
    assert dpytest.verify().message().content('Invalid date')


async def test_create_assignment_invalid_time(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('assignment')
    assert dpytest.verify().message().content('What would you like the assignment to be called')

    await dpytest.message('test')
    assert dpytest.verify().message().content('Link associated with submission? Type N/A if none')

    await dpytest.message('N/A')
    assert dpytest.verify().message().content('Extra description for assignment? Type N/A if none')

    await dpytest.message('Some stuff')
    assert dpytest.verify().message().content('What is the due date')

    await dpytest.message('01-01-1999')
    assert dpytest.verify().message().content('What time is this assignment due')

    await dpytest.message('Oops')
    assert dpytest.verify().message().content('Incorrect input')


async def test_create_exam_valid(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('exam')
    assert dpytest.verify().message().content('What is the title of this exam')

    await dpytest.message('test')
    assert dpytest.verify().message().content('What content is this exam covering?')

    await dpytest.message('Some stuff')
    assert dpytest.verify().message().content('What is the date of this exam?')

    await dpytest.message('01-01-1999')
    assert dpytest.verify().message().content('Which times would you like the exam to be on')

    await dpytest.message('12-12:01')
    assert dpytest.verify().message().content('Exam successfully created')


async def test_create_exam_invalid_date(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('exam')
    assert dpytest.verify().message().content('What is the title of this exam')

    await dpytest.message('test')
    assert dpytest.verify().message().content('What content is this exam covering?')

    await dpytest.message('Some stuff')
    assert dpytest.verify().message().content('What is the date of this exam?')

    await dpytest.message('Oops')
    assert dpytest.verify().message().content('Invalid date')


async def test_create_exam_invalid_time(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('exam')
    assert dpytest.verify().message().content('What is the title of this exam')

    await dpytest.message('test')
    assert dpytest.verify().message().content('What content is this exam covering?')

    await dpytest.message('Some stuff')
    assert dpytest.verify().message().content('What is the date of this exam?')

    await dpytest.message('01-01-1999')
    assert dpytest.verify().message().content('Which times would you like the exam to be on')

    await dpytest.message('Oops')
    assert dpytest.verify().message().content('Incorrect input')


async def test_create_oh_valid(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('office-hour')
    assert dpytest.verify().message().content('Which instructor will this office hour be for?')

    await dpytest.message('Apollo')
    assert dpytest.verify().message().content('Which day would you like the office hour to be on')

    await dpytest.message('Mon')
    assert dpytest.verify().message().content('Which times would you like the office hour to be on')

    await dpytest.message('12-12:01')
    assert dpytest.verify().message().content('Office hour successfully created')


async def test_create_oh_invalid_times(bot):

    await dpytest.message('!create')
    assert dpytest.verify().message().content('Which type of event')

    await dpytest.message('office-hour')
    assert dpytest.verify().message().content('Which instructor will this office hour be for?')

    await dpytest.message('Apollo')
    assert dpytest.verify().message().content('Which day would you like the office hour to be on')

    await dpytest.message('Mon')
    assert dpytest.verify().message().content('Which times would you like the office hour to be on')

    await dpytest.message('Oops')
    assert dpytest.verify().message().content('Incorrect input')

@pytest.mark.asyncio
async def test_take(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]
    instructorRole = dpytest.backend.make_role(name="Instructor", guild=guild0, id_num=5, colour=0, permissions=8,
                                               hoist=False,
                                               mentionable=False)
    dpytest.backend.update_member(user0, nick=None, roles=[instructorRole])

    await dpytest.message('!importevents', attachments='files/assignments.csv')
    bool = dpytest.verify().message().contains().content("Please Submit") == True #Convert verify() to bool
    assert not bool

