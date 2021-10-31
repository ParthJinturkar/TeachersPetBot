import discord
from discord.ext import commands
import datetime

from discord.ext.commands import bot
# ---------------------------------------------------------------------------------------
# Contains Instructor only commands for polling
# ---------------------------------------------------------------------------------------
class Helper(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot





    # --------------------------------------
    # add the file to the bot's cog system
    # --------------------------------------
    def setup(bot):
        bot.add_cog(Helper(bot))      