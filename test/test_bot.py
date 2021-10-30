import discord
import os
from datetime import datetime, timedelta
import discord.ext.test as dpytest
from dotenv import load_dotenv
import pytest


# --------------------
# Tests cogs/hello.py
# --------------------
@pytest.mark.asyncio
async def test_hello(bot):
    await dpytest.message("!hello")
    assert dpytest.verify().message().content("Hello World!")


# -------------------
# Tests cogs/ping.py
# -------------------
@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("!ping")
    assert dpytest.verify().message().contains().content("Pong!")
