import discord.ext.test as dpytest
import pytest

###########################
# Tests Q-and-A functionality
###########################
import discord
from time import sleep


###########################
# Function: test_question
# Description: tests questioning functionality
# Inputs:
#      - bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
@pytest.mark.asyncio
async def test_question(bot):
    await dpytest.message('!ask \"Hello\"')

    sleep(.5)


###########################
# Function: test_question_no_input
# Description: tests questioning functionality when given incorrect input
# Inputs:
#      - bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
@pytest.mark.asyncio
async def test_question_no_input(bot):
    try:
        await dpytest.message('!ask')
    except discord.ext.commands.errors.MissingRequiredArgument:
        return True
    assert False


###########################
# Function: test_question_invalid
# Description: tests questioning functionality when given incorrect input
# Inputs:
#      - bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
@pytest.mark.asyncio
async def test_question_invalid(bot):
    try:
        await dpytest.message('!ask\"hello\"')
    except discord.ext.commands.errors.CommandNotFound:
        return True
    assert False


###########################
# Function: test_answer
# Description: tests answering functionality as a student
# Inputs:
#      - bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
@pytest.mark.asyncio
async def test_answer(bot):
    await dpytest.message('!answer 1 \"Hello\"')

    sleep(.5)


###########################
# Function: test_instr_answer
# Description: tests answering functionality as an instructor
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
#      - guild_id: id of the guild that is using the TeachersPetBot
# Outputs: None
###########################
@pytest.mark.asyncio
async def test_instr_answer(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]
    instructorRole = dpytest.backend.make_role(name="Instructor", guild=guild0, id_num=5, colour=0, permissions=8,
                                               hoist=False,
                                               mentionable=False)
    dpytest.backend.update_member(user0, nick=None, roles=[instructorRole])

    # answer question as instructor
    qna_channel = discord.utils.get(bot.get_all_channels(), name='q-and-a')
    await dpytest.message('!answer 1 \"Hello World\"')

    sleep(0.5)


###########################
# Function: test_instr_answer_invalid_1
# Description: tests answering functionality as an instructor incorrectly
# Inputs:
#      - bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
@pytest.mark.asyncio
async def test_instr_answer_invalid_1(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]
    instructorRole = dpytest.backend.make_role(name="Instructor", guild=guild0, id_num=5, colour=0, permissions=8,
                                               hoist=False,
                                               mentionable=False)
    dpytest.backend.update_member(user0, nick=None, roles=[instructorRole])

    # answer question as instructor
    qna_channel = discord.utils.get(bot.get_all_channels(), name='q-and-a')

    try:
        await dpytest.message('!answer 1')
        sleep(.5)
    except discord.ext.commands.errors.MissingRequiredArgument:
        return True

    assert False


###########################
# Function: test_instr_answer_invalid_1
# Description: tests answering functionality as an instructor incorrectly
# Inputs:
#      - bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
@pytest.mark.asyncio
async def test_instr_answer_invalid_1(bot):
    await dpytest.empty_queue()
    guild0 = dpytest.get_config().guilds[0]
    user0 = dpytest.get_config().guilds[0].members[0]
    instructorRole = dpytest.backend.make_role(name="Instructor", guild=guild0, id_num=5, colour=0, permissions=8,
                                               hoist=False,
                                               mentionable=False)
    dpytest.backend.update_member(user0, nick=None, roles=[instructorRole])

    # answer question as instructor
    qna_channel = discord.utils.get(bot.get_all_channels(), name='q-and-a')

    try:
        await dpytest.message('!answer \"test\"')
        sleep(.5)
    except discord.ext.commands.errors.MissingRequiredArgument:
        return True

    assert False
