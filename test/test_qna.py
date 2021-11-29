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
#      - testing_bot: bot that sends commands to test TeachersPetBot
#      - guild_id: id of the guild that is using the TeachersPetBot
# Outputs: None
###########################
@pytest.mark.asyncio
async def test_answer(bot):
    print('testing answer')

    # make sure bot is not an instructor
    guild = bot.get_guild("test")
    role = discord.utils.get(guild.roles, name="Instructor")
    member = guild.get_member(bot.user.id)
    if "instructor" in [y.name.lower() for y in member.roles]:
        await member.remove_roles(role)

    qna_channel = discord.utils.get(bot.get_all_channels(), name='q-and-a')
    await dpytest.message('!answer 1 \"World\"')

    sleep(1.5)

    messages = await qna_channel.history(limit=1).flatten()
    for m in messages:
        assert 'Student Ans: World' in m.content

###########################
# Function: test_instr_answer
# Description: tests answering functionality as an instructor
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
#      - guild_id: id of the guild that is using the TeachersPetBot
# Outputs: None
###########################
async def test_instr_answer(testing_bot, guild_id):
    print('testing instructor answer')

    # Add instructor role to bot
    guild = testing_bot.get_guild(guild_id)
    role = discord.utils.get(guild.roles, name="Instructor")
    member = guild.get_member(testing_bot.user.id)
    await member.add_roles(role)

    # answer question as instructor
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await dpytest.message('!answer 1 \"Hello World\"')

    sleep(1.5)

    # check message was updated
    messages = await qna_channel.history(limit=1).flatten()
    for m in messages:
        assert 'Instructor Ans: Hello World' in m.content

    # remove instructor role from bot
    await member.remove_roles(role)

