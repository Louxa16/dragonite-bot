import discord
from discord.ext import commands
import json
import random

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): #checks if on cooldown
        msg = '**Encore en cooldown**, réessaye dans {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)

class economie(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog economie online")

    mainshop = [{"name": "helper", "price": 100, "description": "DM moi pour avoir le role helper! "},
                {"name": "vip", "price": 10000, "description": "DM moi pour avoir le role vip!"}]

    # BALANCE
    @client.command(aliases=["bal"])
    async def balance(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        em = discord.Embed(title=f"{ctx.author.name}'s Balance", colour=discord.Colour.green())
        em.add_field(name="Wallet", value="{}🥚".format(wallet_amt))
        em.add_field(name="Bank", value="{}🥚".format(bank_amt))
        await ctx.send(embed=em)

    # Attak
    @client.command(aliases=["atk"])
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def attack(self, ctx):
        await self.open_account(ctx.author)

        users = await self.get_bank_data()

        user = ctx.author

        earnings = random.randrange(101)

        await ctx.send(f"Tu as attaqué des villages pour {earnings}🥚!")

        users[str(user.id)]["wallet"] += earnings

        with open("cogs\\bankbank.json", "w") as f:
            json.dump(users, f)

    # WITHDRAW
    @client.command(aliases=["wdraw"])
    async def withdraw(self, ctx, amount=None):
        await self.open_account(ctx.author)

        if amount == None:
            await ctx.send("Rentre le nombre d'argent d'abbord")
            return

        bal = await self.update_bank(ctx.author)
        if amount == "all":
            amount = bal[1]
            if amount == 0:
                await ctx.send("Tu n'as même pas d'argent dans ta bank")
                return

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("Tu n'as pas asser d'argent dans la bank!")
            return
        if amount < 0:
            await ctx.send("Le montant doit être positif!")
            return

        await self.update_bank(ctx.author, amount)
        await self.update_bank(ctx.author, -1 * amount, "bank")

        await ctx.send(f"Tu as retiré {amount}🥚")

    # DEPOSIT
    @client.command(aliases=["dep"])
    async def deposit(self, ctx, amount=None):
        await self.open_account(ctx.author)

        if amount == None:
            await ctx.send("Rentre le nombre d'argent d'abbord")
            return

        bal = await self.update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]
            if amount == 0:
                await ctx.send("Tu n'as même pas d'argent dans ton wallet")
                return

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("Tu n'as pas asser d'argent dans la bank!")
            return
        if amount < 0:
            await ctx.send("Le montant doit être positif!")
            return

        await self.update_bank(ctx.author, -1 * amount)
        await self.update_bank(ctx.author, amount, "bank")

        await ctx.send(f"Tu as déposé {amount}🥚")

    # SEND
    @client.command()
    async def send(self, ctx, member: discord.Member, amount=None):
        await self.open_account(ctx.author)
        await self.open_account(member.id)

        if amount == None:
            await ctx.send("Rentre le nombre d'argent d'abbord")
            return

        bal = await self.update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("Tu n'as pas asser d'argent dans ton porte monnaie!")
            return
        if amount < 0:
            await ctx.send("Le montant doit être positif!")
            return

        await self.update_bank(ctx.author, -1 * amount, "wallet")
        await self.update_bank(member.id, amount, "wallet")

        await ctx.send(f"Tu as donné {amount}🥚!")

    # SLOTS
    @client.command(aliases=["slt"])
    async def slots(self, ctx, amount=None):
        await self.open_account(ctx.author)

        em = discord.Embed(title="Inventory", colour=discord.Colour.green())

        if amount == None:
            await ctx.send("Rentre le nombre d'argent d'abbord")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("Tu n'as pas asser d'argent dans ton porte monnaie!")
            return
        if amount < 0:
            await ctx.send("Le montant doit être positif!")
            return

        final = []
        for i in range(3):
            a = random.choice(["X", "O", "Q"])

            final.append(a)

        await ctx.send(str(final))

        if final[0] == final[1] or final[2] == final[1]:
            await self.update_bank(ctx.author, 2 * amount)
            await ctx.send(f"Tu as gagné {amount}🥚!")

        else:
            await self.update_bank(ctx.author, -1.2 * amount)
            await ctx.send(f"Tu as perdu {amount}🥚!")

    async def open_account(self, user):

        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0

        with open("cogs\\bankbank.json", "w") as f:
            json.dump(users, f)
        return True

    # VOL
    @client.command()
    async def rob(self, ctx, member: discord.Member):
        await self.open_account(ctx.author)
        await self.open_account(member.id)

        bal = await self.update_bank(member.id)

        if bal[0] < 100:
            await ctx.send("C'est pas la peine, il a même pas 100🥚")
            return

        earnings = random.randrange(0, bal[0])

        await self.update_bank(ctx.author, earnings)
        await self.update_bank(member.id, -1 * earnings)

        await ctx.send(f"Tu as volé {earnings}🥚!")

    # SHOP
    @client.command()
    async def shop(self, ctx):
        em = discord.Embed(title="Shop", colour=discord.Colour.green())
        for item in self.mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name=name, value=f"{price}🥚  !  {desc}")

        await ctx.send(embed=em)

    # BUY
    @client.command()
    async def buy(self, ctx, item, amount=1):
        await self.open_account(ctx.author)

        res = await self.buy_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("Cette object existe même pas!")
                return
            if res[1] == 2:
                await ctx.send(f"Tu n'as pas asser d'oeufs pour acheté {amount} {item}")
                return

        await ctx.send(f"Tu viens d'acheter {amount} {item}!")

    # INV
    @client.command(aliases=["inv"])
    async def inventory(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_bank_data()

        try:
            inv = users[str(user.id)]["inv"]
        except:
            inv = []

        em = discord.Embed(title="Inventory", colour=discord.Colour.green())
        for item in inv:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name=name, value=amount)

        await ctx.send(embed=em)

    # BUY_THIS
    async def buy_this(self, user, item_name, amount):
        global price
        item_name = item_name.lower()
        name_ = None
        for item in self.mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break

        if name_ == None:
            return [False, 1]

        cost = price * amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)

        if bal[0] < cost:
            return [False, 2]

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["inv"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["inv"][index]["amount"] = new_amt
                    t = 1
                    break
                index += 1
            if t == None:
                obj = {"item": item_name, "amount": amount}
                users[str(user.id)]["inv"].append(obj)
        except:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["inv"] = [obj]

        with open("cogs\\bankbank.json", "w") as f:
            json.dump(users, f)

        await self.update_bank(user, cost * -1, "wallet")

        return [True, "Worked", cost]

    # SELL
    @client.command()
    async def sell(self, ctx, item, amount=1):
        await self.open_account(ctx.author)

        res = await self.sell_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("That Object isn't there!")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have {amount} {item} in your inventory.")
                return
            if res[1] == 3:
                await ctx.send(f"You don't have {item} in your inventory.")
                return

        await ctx.send(f"You just sold {amount} {item} .")

    async def sell_this(self, user, item_name, amount, price=None):
        item_name = item_name.lower()
        name_ = None
        for item in self.mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                if price == None:
                    price = 0.9 * item["price"]
                break

        if name_ == None:
            return [False, 1]

        cost = price * amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["inv"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        return [False, 2]
                    users[str(user.id)]["inv"][index]["amount"] = new_amt
                    t = 1
                    break
                index += 1
            if t == None:
                return [False, 3]
        except:
            return [False, 3]

        with open("cogs\\bankbank.json", "w") as f:
            json.dump(users, f)

        await self.update_bank(user, cost, "wallet")

        return [True, "Worked"]

    # OTHER
    async def get_bank_data(self):
        with open("cogs\\bankbank.json", "r") as f:
            users = json.load(f)
        return users

    async def update_bank(self, user, change=0, mode="wallet"):
        users = await self.get_bank_data()

        users[str(user.id)][mode] += change

        with open("cogs\\bankbank.json", "w") as f:
            json.dump(users, f)

        bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
        return bal


def setup(client):
    client.add_cog(economie(client))