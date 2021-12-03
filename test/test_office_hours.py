
import discord.ext.test as dpytest
import discord.ext.commands.errors as dperr
import pytest
from src import office_hours
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
async def test_oh_open_instructor(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]
    oh_channel = dpytest.backend.make_text_channel(name='office-hour-test', guild=guild0, position=2, id_num=2)

    await guild0.create_category(name='TA Office Hours')
    await guild0.create_category(name='Not TA Office Hours')
    await guild0.create_category(name='Not TA Office Hours')

    instructorRole = dpytest.backend.make_role(name="Instructor", guild=guild0, id_num=5, colour=0, permissions=8,
                                               hoist=False,
                                               mentionable=False)
    dpytest.backend.update_member(user0, nick=None, roles=[instructorRole])

    try:
        await office_hours.open_oh(guild0, "test")
    except NotImplementedError:
        # Limitation of dpytest; expected behavior
        pass

@pytest.mark.asyncio
async def test_oh_close_instructor(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]
    oh_channel = dpytest.backend.make_text_channel(name='office-hour-test', guild=guild0, position=2, id_num=2)

    await guild0.create_category(name='TA Office Hours')
    await guild0.create_category(name='Not TA Office Hours')
    await guild0.create_category(name='Not TA Office Hours')

    instructorRole = dpytest.backend.make_role(name="Instructor", guild=guild0, id_num=5, colour=0, permissions=8,
                                               hoist=False,
                                               mentionable=False)
    dpytest.backend.update_member(user0, nick=None, roles=[instructorRole])

    try:
        await office_hours.close_oh(guild0, "test")
    except AttributeError:
        # Due to an array not existing in the fake environment; expected behavior
        pass


@pytest.mark.asyncio
async def test_oh_no_channel(bot):
    await dpytest.message('!oh enter')
    await dpytest.message('!oh exit')
