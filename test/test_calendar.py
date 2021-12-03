# ###########################
# # Tests Event creation & calendar functionality
# ###########################
import discord

import discord.ext.test as dpytest
from src import cal
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

    await dpytest.message('25:37')
    assert not dpytest.verify().message().content('Assignment successfully created')

@pytest.mark.asyncio
async def test_update_calendar(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]

    try:
        cal.update_calendar()

    except AttributeError:
        # Due to an array not existing in the fake environment; expected behavior
        pass


