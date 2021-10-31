import discord
from discord.ext import commands
import datetime


# ---------------------------------------------------------------------------------------
# Contains Instructor only commands for polling
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
    @commands.has_role("Instructor")
    async def poll(self, ctx, *, poll: str):
        if ctx.channel.name == 'instructor-commands':
            print("Polling ", poll)
            await ctx.message.delete()
            embed = discord.Embed(description=f"**{poll}**\n\n", timestamp=datetime.datetime.utcnow(), color=discord.colour.Color.red())
            embed.set_footer(text=f"Poll by {str(ctx.author)}")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        else:
            await ctx.author.send('`!poll` can only be used in the `instructor-commands` channel')
            await ctx.message.delete()    

    @commands.Cog.listener()
    async def on_reaction(self, reaction):
        user = reaction.member
        if user.bot:return
        msg = await self.bot.get_guild(reaction.guild_id).get_channel(reaction.channel_id).fetch_message(reaction.message_id)
        emoji = reaction.emoji
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

    @commands.command(name = "multipoll")
    @commands.has_role("Instructor")
    async def multi_choice(self, ctx, desc: str, *choices):
        if ctx.channel.name == 'instructor-commands':
            await ctx.message.delete()
            if len(choices) < 2:
                return await ctx.send("You have to enter two or more choices to make a poll")

            if len(choices) > 10:
                return await ctx.send("You can't make a poll with more than 10 choices")

            embed = discord.Embed(description=f"**{desc}**\n\n" + "\n\n".join(
                f"{str(self.reactions[i])}  {choice}" for i, choice in enumerate(choices, 1)),
                                timestamp=datetime.datetime.utcnow(), color=discord.colour.Color.gold())
            embed.set_footer(text=f"Poll by {str(ctx.author)}")
            msg = await ctx.send(embed=embed)
            for i in range(1, len(choices) + 1):
                await msg.add_reaction(self.reactions[i])
        else:
            await ctx.author.send('`!poll` can only be used in the `instructor-commands` channel \n You entered the following command\n`' + ctx.message.content + '`')
            await ctx.message.delete()            


# --------------------------------------
# add the file to the bot's cog system
# --------------------------------------
def setup(bot):
    bot.add_cog(Helper(bot))    