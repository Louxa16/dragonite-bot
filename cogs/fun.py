import praw
import random
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import BucketType


intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")

reddit = praw.Reddit(client_id="Y9yXGfI7Pnam0g",
                         client_secret="oryfUbeMWEgu1mipRf-yz3ICmn7Jzg",
                         username="Louxa_",
                         password="Myr08Ric",
                         user_agent="pythonpraw",
                        check_for_async=False)

winningConditions = [[0, 1, 2],
                         [3, 4, 5],
                         [6, 7, 8],
                         [0, 3, 6],
                         [1, 4, 7],
                         [2, 5, 8],
                         [0, 4, 8],
                         [2, 4, 6]]
class fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog fun online")


    #MEME
    @commands.command()
    async def reddit(self, ctx,subred = "memes"):
        subreddit = reddit.subreddit(subred)
        all_subs = []

        top = subreddit.top(limit=10)

        for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url

        em = discord.Embed(title=name)
        em.set_image(url=url)
        await ctx.send(embed= em)

    #WHOIS
    @commands.command(aliases=["user","info"])
    async def whois(self,ctx,member : discord.Member):
        embed = discord.Embed(title= member.name, description= member.mention+" profile", color= discord.Color.green())
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.set_thumbnail(url= member.avatar_url)
        embed.set_footer(icon_url= ctx.author.avatar_url, text= f"demandé par {ctx.author.name}")

        await ctx.send(embed=embed)

    #GUESS THE NUMBER
    @commands.command(name="guessthenumber", aliases=["gtn"], brief="Guess the number game!")
    @commands.max_concurrency(1, BucketType.user, wait=False)
    async def gtn(self, ctx):
        """Play a guess the number game! You have three chances to guess the number 1-10"""

        no = random.randrange(1, 15)
        await ctx.send(
            f"Un nombre entre **1 et 15** a été choisi, tu as 3 chance pour deviné le nombre!"
        )
        for i in range(0, 3):
            try:
                response = await self.client.wait_for(
                    "message",
                    timeout=10,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                )
                guess = int(response.content)

                if guess > 15 or guess < 1:
                    if 2 - i == 0:
                        await ctx.send(
                            f"Pas de chance, Le nombre était: **{no}**"
                        )
                        return
                    else:
                        await ctx.send(
                            "Ce chiffre n'est pas valide, cela ta couté 1 chance..."
                        )

                else:
                    if guess > no:
                        if 2 - i == 0:
                            await ctx.send(
                                f"Tu as manqué de temps, le nombre était: **{no}**"
                            )
                            return
                        else:
                            await ctx.send(
                                f"Le nombre est plus petit que {guess}\n`{2-i}` essaie restante"
                            )
                    elif guess < no:
                        if 2 - i == 0:
                            await ctx.send(
                                f"Tu as manqué d'essaie, le nombre était: **{no}**"
                            )
                            return
                        else:
                            await ctx.send(
                                f"Le nombre est plus grand que {guess}\n`{2-i}` essaie restante"
                            )

                    else:
                        await ctx.send(
                            f"Bien joué ! Tu l'as bien eu, le nombre était: **{no}** !"
                        )
                        return
            except asyncio.TimeoutError:
                await ctx.send(
                    "Tu dois me donner une réponse... Le jeu a été arrêté!"
                )
                return
            except Exception:
                if 2 - i == 0:
                    await ctx.send(
                        f"Tu as manqué d'essaie, le nombre était: **{no}**"
                    )
                    return
                await ctx.send(
                    "Le nombre n'est pas bon, cela t'as couté un essaie..."
                )
    #TICTACTOE
    # TICTACTOE
    player1 = ""
    player2 = ""
    turn = ""
    gameOver = True

    board = []



    @client.command()
    async def tictactoe(self, ctx, p1: discord.Member, p2: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

                # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("C'est le tour à <@" + str(player1.id) + ">.")
            elif num == 2:
                turn = player2
                await ctx.send("C'est le tour à <@" + str(player2.id) + ">.")
        else:
            await ctx.send("Il y a déjà une partie en court.")

    @client.command()
    async def place(self, ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    self.checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver == True:
                        await ctx.send(mark + " à gagné!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("C'est égalité !!")

                        # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("C'est pas ton tour...")
        else:
            await ctx.send("Commence une nouvelle partie avec !tictactoe.")

    def checkWinner(self, winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Mentionne 2 personnes pour jouer au tictactoe.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Entre un position que tu aimerais marquer.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Sois sur de rentrer une position.")

    #HELP
    @commands.command(name="fight")
    @commands.max_concurrency(1, BucketType.user, wait=False)
    async def fight(self, ctx, member: discord.Member):
        """
        Challenge an user to a duel!
        The user cannot be a bot.
        """
        if member.bot or member == ctx.author:
            return await ctx.send("Tu peux pas combatre contre toi même !")

        users = [ctx.author, member]

        user1 = random.choice(users)
        user2 = ctx.author if user1 == member else member

        user1_hp = 100
        user2_hp = 100

        fails_user1 = 0
        fails_user2 = 0

        x = 2

        while True:
            if user1_hp <= 0 or user2_hp <= 0:
                winner = user1 if user2_hp <= 0 else user2
                loser = user2 if winner == user1 else user1
                winner_hp = user1_hp if user2_hp <= 0 else user2_hp
                await ctx.send(
                    random.choice(
                        [
                            f"Wow! **{winner.name}** à explosé **{loser.name}**, il a gagné avec `{winner_hp} HP` restant pour {winner.name}!",
                            f"YEET! **{winner.name}** REKT **{loser.name}**, avec `{winner_hp} HP` restant pour {winner.name}!",
                            f"Woops! **{winner.name}** a envoyé **{loser.name}** à la maison en pleurant... avec `{winner_hp} HP` restant pour {winner.name}!",
                        ]
                    )
                )
                return

            alpha = user1 if x % 2 == 0 else user2
            beta = user2 if alpha == user1 else user1
            await ctx.send(
                f"{alpha.mention}, Que vas-tu faire ? `punch`, `kick`, `slap` or `end`?\nÉcrit ton attack dans le chat !"
            )

            def check(m):
                if alpha == user1:
                    return m.author == user1 and m.channel == ctx.channel
                else:
                    return m.author == user2 and m.channel == ctx.channel

            try:
                msg = await self.client.wait_for("message", timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(
                    f"**{alpha.name}** n'a pas répondu attaned... **{beta.name}** wins!"
                )
                return

            if msg.content.lower() == "punch":
                damage = random.choice(
                    [
                        random.randint(20, 60),
                        random.randint(0, 50),
                        random.randint(30, 70),
                        random.randint(0, 40),
                        random.randint(10, 30),
                        random.randint(5, 10),
                    ]
                )

                if alpha == user1:
                    user2_hp -= damage
                    hpover = 0 if user2_hp < 0 else user2_hp
                else:
                    user1_hp -= damage
                    hpover = 0 if user1_hp < 0 else user1_hp

                randommsg = random.choice(
                    [
                        f"**{alpha.name}** a fait **{damage}** avec son **SUPER** punch.\n**{beta.name}** reste {hpover} HP",
                        f"**{alpha.name}** À éclater le figure des **{beta.name}** et a fait **{damage}** dommage!\n**{beta.name}** reste {hpover} HP!",
                        f"**{alpha.name}** a mis son poing dans **{beta.name}** et a fait **{damage}** de dommage!\n**{beta.name}** reste {hpover} HP!",
                    ]
                )
                await ctx.send(f"{randommsg}")

            elif msg.content.lower() == "kick":
                damage = random.choice(
                    [
                        random.randint(30, 45),
                        random.randint(30, 60),
                        random.randint(-50, -1),
                        random.randint(-40, -1),
                    ]
                )
                if damage > 0:

                    if alpha == user1:
                        user2_hp -= damage
                        hpover = 0 if user2_hp < 0 else user2_hp
                    else:
                        user1_hp -= damage
                        hpover = 0 if user1_hp < 0 else user1_hp

                    await ctx.send(
                        random.choice(
                            [
                                f"**{alpha.name}** a kické **{beta.name}** et a fait **{damage}** de dommage\n**{beta.name}** reste **{hpover}** HP",
                                f"**{alpha.name}** a fait un **SUPER KICK** à **{alpha.name}**, il a fait **{damage}** dommage à {beta.name}.\n**{beta.name}** reste **{hpover}** HP",
                            ]
                        )
                    )
                elif damage < 0:

                    if alpha == user1:
                        user1_hp += damage
                        hpover = 0 if user1_hp < 0 else user1_hp
                    else:
                        user2_hp += damage
                        hpover = 0 if user2_hp < 0 else user2_hp

                    await ctx.send(
                        random.choice(
                            [
                                f"**{alpha.name}** flipped over while kicking their opponent, dealing **{-damage}** damage to themselves.",
                                f"{alpha.name} tried to kick {beta.name} but FELL DOWN! They took {-damage} damage!",
                            ]
                        )
                    )

            elif msg.content.lower() == "slap":
                damage = random.choice(
                    [
                        random.randint(20, 60),
                        random.randint(0, 50),
                        random.randint(30, 70),
                        random.randint(0, 40),
                        random.randint(10, 30),
                        random.randint(5, 10),
                    ]
                )

                if alpha == user1:
                    user2_hp -= damage
                    hpover = 0 if user2_hp < 0 else user2_hp
                else:
                    user1_hp -= damage
                    hpover = 0 if user1_hp < 0 else user1_hp

                await ctx.send(
                    f"**{alpha.name}** a tapé {beta.name}et lui a fait **{damage}** dommage.\n{beta.name} reste **{hpover}** HP"
                )

            elif msg.content.lower() == "end":
                await ctx.send(f"{alpha.name} à arrêter la partie...")
                return

            elif (
                msg.content.lower() != "kick"
                and msg.content.lower() != "slap"
                and msg.content.lower() != "punch"
                and msg.content.lower() != "end"
            ):
                if fails_user1 >= 1 or fails_user2 >= 1:
                    return await ctx.send(
                        "La partie à été terminer à cause de plusieur raison... DIEU, POURQUOI !!!"
                    )
                if alpha == user1:
                    fails_user1 += 1
                else:
                    fails_user2 += 1
                await ctx.send("Ce chois n'est pas valide!")
                x -= 1

            x += 1


def setup(client):
    client.add_cog(fun(client))