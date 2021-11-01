import discord
from discord.ext import commands
import datetime

from discord.ext.commands import bot
# ---------------------------------------------------------------------------------------
# Contains Instructor only commands for getting member information
# ---------------------------------------------------------------------------------------
class Helper(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "whois")
    @commands.has_role("Instructor")
    async def identify_member(self, ctx, *, member_name: str = None):
        member = ctx.guild.get_member_named(member_name)
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.orange(), timestamp=ctx.message.created_at,
                              title=str(member))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)
        
# --------------------------------------
# add the file to the bot's cog system
# --------------------------------------
def setup(bot):
    bot.add_cog(Helper(bot))      