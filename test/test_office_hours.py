from utils import wait_for_msg, wait_for_channel_create

import discord.ext.test as dpytest
import pytest
from time import sleep

@pytest.mark.asyncio
async def test_oh_queue_individual(bot):
    await dpytest.message('!oh enter')
    sleep(.5)
    await dpytest.message('!oh exit')
    sleep(.5)
