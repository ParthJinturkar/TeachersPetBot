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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = payload.member
        if user.bot:return
        msg = await self.bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id)
        emoji = payload.emoji
        users = []
        if msg.author.bot and("👍"and"👎")in[str(i)for i in msg.reactions]:
            for react in msg.reactions:
                if str(react)=="👍":
                    async for reactor in react.users():
                        if reactor.bot:continue
                        if reactor in users:
                            await msg.remove_reaction(emoji, user)
                            return
                        users.append(reactor)
                elif str(react)=="👎":
                    async for reactor in react.users():
                        if reactor.bot:continue
                        if reactor in users:
                            await msg.remove_reaction(emoji, user)
                            return
                    return
   


# --------------------------------------
# add the file to the bot's cog system
# --------------------------------------
def setup(bot):
    bot.add_cog(Helper(bot))    