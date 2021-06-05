import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")

class jstu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog helpcmd online")

    #HELP
    @client.group(invoke_without_command=True)
    async def jstu(self,ctx):
        embed = discord.Embed(title="**Help**",description="Ici, il y a tout ce que tu as besoin de savoir sur le bot, Le but du mode économie, les commandes pour l'économie, les commandes de modération les commandes funs et encore plus !",color=0x00ff00)
        embed.set_thumbnail(url="")
        embed.set_author(name="Pour avoir plus de détails sur les commandes fait: !help commande. Example: !help reddit")
        embed.add_field(name="Économie",value="La partie économie du serveur est simple. Il va falloir attaquer des villages pour récupérer des oeufs 🥚.Ses oeufs vont te servirent à acheter des objects dans le `shop` mais sourtout à être le premier sur le podiome.",inline=False)
        embed.add_field(name="Les commandes pour l'économie sont les suivantes:",value="`attack`,`deposit`,`withdraw`,`slots`,`send`,`shop`,`buy`,`sell`,`inventory` ",inline=False)
        embed.add_field(name="Modération",value="Les commandes de modération sont seulement pour les modérateurs et plus au gradé. Elles vont servir à faire règner l'ordre sur le serveur.",inline=False)
        embed.add_field(name="Les commandes pour la modération sont les suivantes:",value="`kick`,`ban`,`mute`. Il y a aussi `unban` et `unmute` mais pour plus d'information sur ses commandes faite leurs opposé. unban=ban, unmute=mute.",inline=False)
        embed.add_field(name="Fun", value=f"Les commandes fun sont pour le divertisement, elles n'ont pas de lien avec les commandes économies !", inline = False)
        embed.add_field(name="Les commandes funs sont les suivantes:", value="`reddit`,`whois`,`tictactoe`,`gtn`.", inline=False)
        embed.add_field(name="COMME MENTIONNÉ PLUS HAUT, POUR AVOIR DES INFORMATION SUR UNE COMMANDE PARTICULIÈRE FAITE: !help nom_de_la_commande. exemple: !help reddit",value="Amusez-vous bien !", inline=True)
        await ctx.send(embed=embed)

    @jstu.command()
    async def kick(self,ctx):
        em=discord.Embed(title="**Kick**", description="Exclure un membre du serveur si il ne respect pas les règles(léger)",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!kick(k) <membre> [raison]")
        await ctx.send(embed=em)

    @jstu.command()
    async def ban(self,ctx):
        em=discord.Embed(title="**Ban**", description="Banir un membre du serveur si il ne respect pas les règles(grave)",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!ban(b) <membre> [raison],!unban(ub) <membre>")
        await ctx.send(embed=em)

    @jstu.command()
    async def mute(self,ctx):
        em=discord.Embed(title="**Mute and Unmute**", description="Sert a rendre muet un membre du serveur si il est dérangent(spam par exemple)",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!mute(m) <membre>, !unmute(um) <membre>")
        await ctx.send(embed=em)

    @jstu.command()
    async def reddit(self,ctx):
        em=discord.Embed(title="**Reddit**", description="Voir des posts de Reddit",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!reddit <suject>(si rien est dans le suject, un il va y avoir un meme)")
        await ctx.send(embed=em)

    @jstu.command()
    async def whois(self, ctx):
        em = discord.Embed(title="**Whois**", description="Voir le profile de quelqu'un", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!whois <@la personne>")
        await ctx.send(embed=em)

    @jstu.command()
    async def balance(self, ctx):
        em = discord.Embed(title="**Balance**", description="Cette commande sert à voir ton argents.", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!balance(bal)")
        await ctx.send(embed=em)

    @jstu.command()
    async def inventory(self, ctx):
        em = discord.Embed(title="**Inventory**", description="Cette commande sert à voir ton inventaire.", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!inventory(inv)")
        await ctx.send(embed=em)

    @jstu.command()
    async def attack(self, ctx):
        em = discord.Embed(title="**Attack**", description="Cette commande sert à attaquer des villages et gagner de l'argent.", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!attak(atk)")
        await ctx.send(embed=em)

    @jstu.command()
    async def deposit(self, ctx):
        em = discord.Embed(title="**Deposit**", description="Cette commande sert à transférer ton argent de ton porte-monnaie à la banque.", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!deposit(dep)")
        await ctx.send(embed=em)

    @jstu.command()
    async def withdraw(self, ctx):
        em = discord.Embed(title="**Withdraw**", description="Cette commande sert à transférer ton argent de la banque à ton porte-monnaie.", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!withdraw(wdraw)")
        await ctx.send(embed=em)

    @jstu.command()
    async def slots(self, ctx):
        em = discord.Embed(title="**Slots**", description="Cette commande sert à parier de l'argent.", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!slots(slt) <nombre d'argent>")
        await ctx.send(embed=em)

    @jstu.command()
    async def send(self, ctx):
        em = discord.Embed(title="**Send**", description="Cette commande sert à envoyer de l'argent à quelqu'un.", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!send <membre>")
        await ctx.send(embed=em)

    @jstu.command()
    async def shop(self, ctx):
        em = discord.Embed(title="**Shop**", description="Cette commande sert à voir les objets que tu peux acheter.", color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!shop")
        await ctx.send(embed=em)

    @jstu.command()
    async def buy(self,ctx):
        em = discord.Embed(title="**Buy**", description="Cette commande sert à acheter des objets dans le `shop`",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!buy <item>")
        await ctx.send(embed=em)

    @jstu.command()
    async def sell(self, ctx):
        em = discord.Embed(title="**Sell**", description="Cette commande sert à vendre un objet que tu as acheté dans le `shop`",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!sell item")
        await ctx.send(embed=em)

    @jstu.command()
    async def gtn(self, ctx):
        em = discord.Embed(title="**Guess The Number**", description="Un coup le commande activé, tu vas devoir deviné un nombre choisi entre 1 et 15!",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!guessthenumber(gtn)")
        await ctx.send(embed=em)

    @jstu.command()
    async def tictactoe(self, ctx):
        em = discord.Embed(title="**Sell**", description="Cette commande sert à faire un tictactoe avec quelqu'un d'autre",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!tictactoe <@membre>")
        await ctx.send(embed=em)

    @jstu.command()
    async def okok(self, ctx):
        em = discord.Embed(title="**Sell**", description="Cette commande sert à faire un tictactoe avec quelqu'un d'autre",color=ctx.author.color.blue())
        em.add_field(name="**Syntax**", value="!tictactoe <@membre>")
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(jstu(client))