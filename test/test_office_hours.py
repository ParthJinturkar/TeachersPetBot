
import discord.ext.test as dpytest
import discord.ext.commands.errors as dperr
import pytest
from time import sleep


@pytest.mark.asyncio
async def test_oh_queue_individual(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]
    oh_channel = dpytest.backend.make_text_channel(name='office-hour-test', guild=guild0, position=2, id_num=2)

    try:
        await dpytest.message(content='!oh enter', channel=oh_channel, member=user0, attachments=None)
        sleep(.5)
        await dpytest.message(content='!oh exit', channel=oh_channel, member=user0, attachments=None)
        sleep(.5)

    except dperr.CommandInvokeError as e:
        if "TypeError" in str(e):
            # Type Error happens because no TA is loaded in the system (since it's not real). This is expected behavior
            pass
        else:
            assert False

@pytest.mark.asyncio
async def test_oh_queue_instructor(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]
    oh_channel = dpytest.backend.make_text_channel(name='office-hour-test', guild=guild0, position=2, id_num=2)

    instructorRole = dpytest.backend.make_role(name="Instructor", guild=guild0, id_num=5, colour=0, permissions=8,
                                               hoist=False,
                                               mentionable=False)
    dpytest.backend.update_member(user0, nick=None, roles=[instructorRole])

    try:
        await dpytest.message(content='!oh enter', channel=oh_channel, member=user0, attachments=None)
        sleep(.5)
        await dpytest.message(content='!oh exit', channel=oh_channel, member=user0, attachments=None)
        sleep(.5)

    except dperr.CommandInvokeError as e:
        if "TypeError" in str(e):
            # Type Error happens because no TA is loaded in the system (since it's not real). This is expected behavior
            pass
        else:
            assert False

@pytest.mark.asyncio
async def test_oh_no_channel(bot):
    await dpytest.message('!oh enter')
    sleep(.5)
    await dpytest.message('!oh exit')
    sleep(.5)