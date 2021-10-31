import datetime
from datetime import datetime, timedelta

import discord.ext.test as dpytest
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


# -------------------
# Tests cogs/ping.py
# -------------------
@pytest.mark.asyncio
async def test_generate_reminders(bot):
    await dpytest.message("!clearreminders")
    assert dpytest.verify().message().contains().content("No reminders to delete..!!")
    # Try generating a normal reminder
    await dpytest.message("!addhw CSC500 HW1 DEC 21 2021 12:00")
    assert dpytest.verify().message().contains().content(
        "CSC500 homework named: HW1 which is due on: 2021-12-21 12:00:00")
    # Try to generate the same reminder
    await dpytest.message("!addhw CSC500 HW1 DEC 21 2021 12:00")
    assert dpytest.verify().message().contains().content("This homework has already been added..!!")
    # Try updating the due date
    await dpytest.message("!changeduedate CSC500 HW1 DEC 22 2022 10:00")
    assert dpytest.verify().message().contains().content(
        "CSC500 HW1 has been updated with following date: 2022-12-22 10:00:00")
    # Try deleting a reminder
    await dpytest.message("!deletereminder CSC500 HW1")
    assert dpytest.verify().message().contains().content(
        "Following reminder has been deleted: Course: CSC500, Homework Name: HW1, Due Date: 2022-12-22 10:00:00")
    # Try adding a reminder due in an hour
    now = datetime.now() + timedelta(hours=1)
    dt_string = now.strftime("%b %d %Y %H:%M")
    await dpytest.message(f"!addhw CSC600 HW0 {dt_string}")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC600 homework named: HW0")
    # Check to see that the reminder is due this week
    await dpytest.message("!duethisweek")
    assert dpytest.verify().message().contains().content("CSC600 HW0 is due this week")
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("!clearreminders")
    assert dpytest.verify().message().contains().content("All reminders have been cleared..!!")


@pytest.mark.asyncio
async def test_empty_reminders(bot):
    # Test duetoday
    await dpytest.message("!duetoday")
    assert dpytest.verify().message().contains().content("You have no dues today..!!")
    # Test duethisweek
    await dpytest.message("!duethisweek")
    assert dpytest.verify().message().contains().content("No dues this week")
    # Test coursedue
    await dpytest.message("!coursedue CSC505")
    assert dpytest.verify().message().contains().content("Rejoice..!! You have no pending homeworks for CSC505..!!")
    # Test listreminders
    await  dpytest.message("!listreminders")
    assert dpytest.verify().message().contains().content("Mission Accomplished..!! You don't have any more dues..!!")


@pytest.mark.asyncio
async def test_reminder_errors(bot):
    # with pytest.raises(Exception):
    await dpytest.message("!addhw CSC500 HW1 DEC asdf")
    assert dpytest.verify().message().contains().content("Due date could not be parsed")
    with pytest.raises(Exception):
        await dpytest.message("!deletereminder")
        assert dpytest.verify().message().contains().content("To use the deletereminder command, do:")
    with pytest.raises(Exception):
        await dpytest.message("!changeduedate")
        assert dpytest.verify().message().contains().content("To use the changeduedate command, do:")
    with pytest.raises(Exception):
        await dpytest.message("!coursedue")
        assert dpytest.verify().message().contains().content("To use the coursedue command, do:")