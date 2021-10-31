import discord
from discord.ext import commands
import datetime
import os
import csv
import random


# ---------------------------------------------------------------------------------------
# Contains commands for member verification, which is handled with direct DMs to the bot
# ---------------------------------------------------------------------------------------
class Helper(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    @property
    def reactions(self):
        return {
            1: '1️⃣',
            2: '2️⃣',
            3: '3️⃣',
            4: '4️⃣',
            5: '5️⃣',
            6: '6️⃣',
            7: '7️⃣',
            8: '8️⃣',
            9: '9️⃣',
            10: '🔟'
        }

    @commands.command(name = "poll")
    async def poll(self, ctx, *, poll: str):
        print("Polling ", poll)
        await ctx.message.delete()
        embed = discord.Embed(description=poll)
        embed.set_author(name=f"Poll by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')




# --------------------------------------
# add the file to the bot's cog system
# --------------------------------------
def setup(bot):
    bot.add_cog(Helper(bot))    