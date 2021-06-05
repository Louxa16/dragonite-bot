import discord
from discord.ext import commands
import os
from prsaw import RandomStuff
import math
import aiosqlite
import asyncio


client = commands.Bot(command_prefix="!")

intents = discord.Intents.default()
intents.members = True
client.remove_command("help")
client.multiplier = 1
#COGS
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir(r"C:\Users\dessc\PycharmProjects\BOT\Bot discord\cogs"):
    if filename.endswith(r".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

#ON_READY
@client.event
async def on_ready():
    print("IM ON BABBY")


#AI
rs = RandomStuff(async_mode=True)

@client.event
async def on_message(message):
    if client.user== message.author:
        return
    if message.channel.id == 847130010790920192:
        response = rs.get_ai_response(message.content)
        await message.reply(response)
    await client.process_commands(message)
#LEVELLING
async def initialize():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect("expData.db")
    await client.db.execute(
        "CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")


@client.event
async def on_ready():
    print(client.user.name + " is ready.")


@client.event
async def on_message(message):
    if not message.author.bot:
        cursor = await client.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)",
                                      (message.guild.id, message.author.id, 1))

        if cursor.rowcount == 0:
            await client.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?",
                                 (message.guild.id, message.author.id))
            cur = await client.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?",
                                       (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / client.multiplier

            if lvl.is_integer():
                await message.channel.send(f"{message.author.mention} well done! You're now level: {int(lvl)}.")

        await client.db.commit()

    await client.process_commands(message)


@client.command()
async def rank(ctx, member: discord.Member = None):
    if member is None: member = ctx.author

    # get user exp
    async with client.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?",
                              (ctx.guild.id, member.id)) as cursor:
        data = await cursor.fetchone()
        exp = data[0]

        # calculate rank
    async with client.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
        rank = 1
        async for value in cursor:
            if exp < value[0]:
                rank += 1

    lvl = int(math.sqrt(exp) // client.multiplier)

    current_lvl_exp = (client.multiplier * (lvl)) ** 2
    next_lvl_exp = (client.multiplier * ((lvl + 1))) ** 2

    lvl_percentage = ((exp - current_lvl_exp) / (next_lvl_exp - current_lvl_exp)) * 100

    embed = discord.Embed(title=f"Stats for {member.name}", colour=discord.Colour.gold())
    embed.add_field(name="Level", value=str(lvl))
    embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
    embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}")
    embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

    await ctx.send(embed=embed)


@client.command()
async def rankboard(ctx):
    buttons = {}
    for i in range(1, 6):
        buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i  # only show first 5 pages

    previous_page = 0
    current = 1
    index = 1
    entries_per_page = 10

    embed = discord.Embed(title=f"Leaderboard Page {current}", description="", colour=discord.Colour.gold())
    msg = await ctx.send(embed=embed)

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        if current != previous_page:
            embed.title = f"Leaderboard Page {current}"
            embed.description = ""

            async with client.db.execute(
                    f"SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ",
                    (ctx.guild.id, entries_per_page, entries_per_page * (current - 1),)) as cursor:
                index = entries_per_page * (current - 1)

                async for entry in cursor:
                    index += 1
                    member_id, exp = entry
                    member= await client.fetch_user(member_id)
                    embed.description += f"{index}) {member.mention} : {exp}\n"

                await msg.edit(embed=embed)

        try:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction,
                                                                             user: user == ctx.author and reaction.emoji in buttons,
                                                timeout=60.0)

        except asyncio.TimeoutError:
            return await msg.clear_reactions()

        else:
            previous_page = current
            await msg.remove_reaction(reaction.emoji, ctx.author)
            current = buttons[reaction.emoji]

client.loop.create_task(initialize())
client.run("ODQxODM2MzEyNzQzMTE2ODIx.YJsjKQ.CvYeSQwo_rNYFof5VwB-UvvhvTM")
asyncio.run(client.db.close())