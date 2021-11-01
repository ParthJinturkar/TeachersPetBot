import discord
from discord.ext import commands


# ----------------------------------------------------------------------------------------------
# Returns the ping of the bot, useful for testing bot lag and as a simple functionality command
# ----------------------------------------------------------------------------------------------
from src import qna


class qanda(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ###########################
    # Function: ask
    # Description: command to ask question and sends to qna module
    # Inputs:
    #      - ctx: context of the command
    #      - question: question text
    # Outputs:
    #      - User question in new post
    ###########################
    @commands.command(name='ask', help='Ask question. Please put question text in quotes.')
    async def ask_question(self, ctx, question):
        ''' ask question command '''
        # make sure to check that this is actually being asked in the Q&A channel
        if ctx.channel.name == 'q-and-a':
            await qna.question(ctx, question)
        else:
            await ctx.author.send('Please send questions to the #q-and-a channel.')
            await ctx.message.delete()

    ###########################
    # Function: answer
    # Description: command to answer question and sends to qna module
    # Inputs:
    #      - ctx: context of the command
    #      - q_num: question number to answer
    #      - answer: answer text
    # Outputs:
    #      - User answer in question post
    ###########################
    @commands.command(name='answer', help='Answer specific question. Please put answer text in quotes.')
    async def answer_question(self, ctx, q_num, answer):
        ''' answer question command '''
        # make sure to check that this is actually being asked in the Q&A channel
        if ctx.channel.name == 'q-and-a':
            await qna.answer(ctx, q_num, answer)
        else:
            await ctx.author.send('Please send answers to the #q-and-a channel.')
            await ctx.message.delete()

# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    bot.add_cog(qanda(bot))

# Copyright (c) 2021 War-Keeper
