import datetime
import discord
from discord.ext import commands

# ---------------------------------------------------------------------------------------
# Contains Instructor only commands for polling
# ---------------------------------------------------------------------------------------
class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # contains reactions for multipoll
    @property
    def reactions(self):
        return {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
            10: "🔟",
        }

    # ----------------------------------------------------------------------------------------------
    #    Function: poll(self, ctx, *, poll: str = None)
    #    Description: Instructor command for creating poll with 2 choices
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    - *:
    #    - poll: question for poll
    # ----------------------------------------------------------------------------------------------
    @commands.command(name="poll")
    @commands.has_role("Instructor")
    async def poll(self, ctx, *, poll: str = None):
        msg = ctx.message.content
        await ctx.message.delete()
        if ctx.channel.name == "instructor-commands":
            if poll is None:
                embed = discord.Embed(
                    description="!poll command should be used in following way:"
                    + "\n\n`!poll poll_content`",
                    color=discord.colour.Color.red(),
                )
                await ctx.author.send(embed=embed)
                return
            general_channel = None
            for channel in ctx.guild.text_channels:
                if channel.name == "general":
                    general_channel = channel
                    break
            if general_channel:
                embed = discord.Embed(
                    description=f"**{poll}**\n\n",
                    timestamp=datetime.datetime.utcnow(),
                    color=discord.colour.Color.blue(),
                )
                embed.set_footer(text=f"Poll created by {str(ctx.author)}")
                msg = await general_channel.send(embed=embed)
                await msg.add_reaction("👍")
                await msg.add_reaction("👎")
        else:
            embed = discord.Embed(
                description="`!poll` can only be used in the `instructor-commands` channel."
                + "\n\nYou entered the following command:\n\n`"
                + msg
                + "`",
                color=discord.colour.Color.red(),
            )
            await ctx.author.send(embed=embed)

    # ----------------------------------------------------------------------------------------------
    #    Function: on_reaction(self, reaction)
    #    Description: Listener to avoid members from selecting both choices in 2 choice poll
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - reaction: reaction on the poll
    # ----------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_reaction(self, reaction):
        user = reaction.member
        if user.bot:
            return
        msg = (
            await self.bot.get_guild(reaction.guild_id)
            .get_channel(reaction.channel_id)
            .fetch_message(reaction.message_id)
        )
        emoji = reaction.emoji
        users = []
        if msg.author.bot and ("👍" and "👎") in [str(i) for i in msg.reactions]:
            for react in msg.reactions:
                if str(react) == "👍":
                    async for reactor in react.users():
                        if reactor.bot:
                            continue
                        if reactor in users:
                            await msg.remove_reaction(emoji, user)
                            return
                        users.append(reactor)
                elif str(react) == "👎":
                    async for reactor in react.users():
                        if reactor.bot:
                            continue
                        if reactor in users:
                            await msg.remove_reaction(emoji, user)
                            return
                    return

    # ----------------------------------------------------------------------------------------------
    #    Function: multi_choice(self, ctx, desc: str = None, *choices)
    #    Description: Instructor command for creating multi choice multi option poll
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    - *choices: variable arguments for choices for the poll
    # ----------------------------------------------------------------------------------------------
    @commands.command(name="multipoll")
    @commands.has_role("Instructor")
    async def multi_choice(self, ctx, desc: str = None, *choices):
        msg = ctx.message.content
        await ctx.message.delete()
        if ctx.channel.name == "instructor-commands":
            if desc is None:
                embed = discord.Embed(
                    description='!multipoll command should be used in following way:'
                    + '\n\n`!multipoll "poll_content" "poll_choice1" "poll_choice2"...`',
                    color=discord.colour.Color.red(),
                )
                await ctx.author.send(embed=embed)
                return
            general_channel = None
            for channel in ctx.guild.text_channels:
                if channel.name == "general":
                    general_channel = channel
                    break
            if general_channel:
                if len(choices) < 2:
                    embed = discord.Embed(
                        description="You have to enter two or more choices to make a multipoll."
                        + "\n\nYou entered the following command:\n\n`"
                        + msg
                        + "`",
                        color=discord.colour.Color.red(),
                    )
                    return await ctx.author.send(embed=embed)
                if len(choices) > 10:
                    embed = discord.Embed(
                        description="You can't make a multipoll with more than 10 choices."
                        + "\n\nYou entered the following command:\n\n`"
                        + msg
                        + "`",
                        color=discord.colour.Color.red(),
                    )
                    return await ctx.author.send(embed=embed)
                embed = discord.Embed(
                    description=f"**{desc}**\n\n"
                    + "\n\n".join(
                        f"{str(self.reactions[i])}  {choice}"
                        for i, choice in enumerate(choices, 1)
                    ),
                    timestamp=datetime.datetime.utcnow(),
                    color=discord.colour.Color.gold(),
                )
                embed.set_footer(text=f"Poll created by {str(ctx.author)}")
                msg = await general_channel.send(embed=embed)
                for i in range(1, len(choices) + 1):
                    await msg.add_reaction(self.reactions[i])
        else:
            embed = discord.Embed(
                description="`!multipoll` can only be used in the `instructor-commands` channel."
                + "\n\nYou entered the following command:\n\n`"
                + msg
                + "`",
                color=discord.colour.Color.red(),
            )
            await ctx.author.send(embed=embed)


# --------------------------------------
# add the file to the bot's cog system
# --------------------------------------
def setup(bot):
    bot.add_cog(Helper(bot))
