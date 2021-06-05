import discord
from discord.ext import commands
import json

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")

filtered_words = ["ram ranch", "nigga", "fdp", "fils de pute","pute"]

tout_cmd = [{"name":"!whois","description":"Cette commande sert à voir le profile d'une personne."},
            {"name":"!meme (sujet)","description":"Cette commande sert à voir des memes de Reddit."}]

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog moderation online")

    #FILTERD WORD
    @commands.Cog.listener()
    async def on_message(self,msg):
        for word in filtered_words:
            if word in msg.content:
                await msg.delete()


    # CLEAR
    @commands.command(aliases=["c"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

    # KICK
    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Pas de raison."):
        await member.send("Tu as été exclu car: " + reason+". Tu peux toujours rejoindre avec ce lien mais, respect les règles !:https://discord.gg/TF295RRQkd")
        await member.kick(reason=reason)

    # BAN
    @commands.command(aliases=["b"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Pas de raison"):
        await member.send("Tu as été banni car: " + reason+". Si un jour tu es débanni, respect les règles.")
        await ctx.send(member.mention + " a été banni.")
        await member.ban(reason=reason)

    # UNBAN
    @commands.command(aliases=["ub"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split("#")
        for banned_entry in banned_users:
            user = banned_entry.user
            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await ctx.send(member_name + " a été débanni.")
                return

    #MUTE
    @commands.command(aliases=['m'])
    @commands.has_permissions(kick_members=True)
    async def mute(self,ctx,member : discord.Member):
        muted_role = ctx.guild.get_role(845297624444698624)
        await member.add_roles(muted_role)

        await ctx.send(member.mention + " a été mute...")

    #UNMUTE
    @commands.command(aliases=['um'])
    @commands.has_permissions(kick_members=True)
    async def unmute(self,ctx,member : discord.Member):
        muted_role = ctx.guild.get_role(845297624444698624)

        await member.remove_roles(muted_role)

        await ctx.send(member.mention + " a été démute...")

    #reactionrole
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            pass

        else:
            with open('C:\\Users\\dessc\\PycharmProjects\\BOTT\\discordbot\\cogs\\reactrole.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == payload.emoji.name:
                        role = discord.utils.get(self.client.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                        await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        with open('C:\\Users\\dessc\\PycharmProjects\\BOTT\\discordbot\\cogs\\reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(self.client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    guild = self.client.get_guild(payload.guild_id)
                    member = await guild.fetch_member(payload.user_id)
                    await member.remove_roles(role)

    @commands.command()
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def reactrole(self, ctx, emoji, role : discord.Role, *, message):

        emb = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction(emoji)

        with open('C:\\Users\\dessc\\PycharmProjects\\BOTT\\discordbot\\cogs\\reactrole.json') as json_file:
            data = json.load(json_file)

            new_react_role = {'role_name': role.name,
                              'role_id': role.id,
                              'emoji': emoji,
                              'message_id': msg.id
            }


            data.append(new_react_role)

        with open('C:\\Users\\dessc\\PycharmProjects\\BOTT\\discordbot\\cogs\\reactrole.json', 'w') as f:
            json.dump(data,f,indent=4)


def setup(client):
    client.add_cog(moderation(client))