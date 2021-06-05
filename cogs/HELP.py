import asyncio
import discord
from discord.ext import commands


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    @commands.command(name="wiki", aliases=["w"])
    async def wiki(self, ctx):
        first_run = True
        while True:
            if first_run:
                page1 = discord.Embed(title='Page 1/4', description='Description1', colour=discord.Colour.orange())
                first_run = False
                msg = await ctx.send(embed=page1)

                reactmoji = ["ℹ️", "💸", "🃏", "🛠️"]

                page2 = discord.Embed(title='Page 2/4', description='Description2', colour=discord.Colour.orange())
                page3 = discord.Embed(title='Page 3/4', description='Description3', colour=discord.Colour.orange())
                page4 = discord.Embed(title='Page 4/4', description='Description4', colour=discord.Colour.orange())


                for react in reactmoji:
                    await msg.add_reaction(react)

            def check_react(reaction, user):
                if reaction.message.id != msg.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactmoji:
                    return False
                return True

            try:
                res, user = await self.bot.wait_for('reaction_add', check=check_react)
            except asyncio.TimeoutError:
                return await msg.clear_reactions()

            if user != ctx.message.author:
                pass
            elif 'ℹ️' in str(res.emoji):
                await msg.remove_reaction("ℹ️", user)
                await msg.edit(embed=page1)

            elif '💸' in str(res.emoji):
                await msg.remove_reaction("💸", user)
                await msg.edit(embed=page2)

            elif '🃏' in str(res.emoji):
                await msg.remove_reaction("🃏", user)
                await msg.edit(embed=page3)

            elif '🛠️' in str(res.emoji):
                await msg.remove_reaction("🛠️", user)
                await msg.edit(embed=page4)

def setup(bot):
    bot.add_cog(Wiki(bot))