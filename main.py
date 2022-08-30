from deck import Deck
from card import Card
import random
import game
import interactions
import threading
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")
guild = os.getenv("GUILD_ID")

bot = interactions.Client(token=token)

turnOrder = []
playerOrder = []

lock = threading.Lock()

showHandButton = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Show Hand",
    custom_id="show_hand"
)

shoutUnoButton = interactions.Button(
    style=interactions.ButtonStyle.DANGER,
    label="Shout Uno",
    custom_id="shout_uno",
    disabled=False
)

def findPlayer(name):
    for player in game.playerOrder:
        if player.name == name:
            return game.playerOrder.index(player)

def advancePlayer():
    if game.isIncrement:
        game.currentPlayer += 1
        if game.currentPlayer >= len(game.turnOrder):
            game.currentPlayer = 0
    else:
        game.currentPlayer -= 1
        if game.currentPlayer <= -1:
            game.currentPlayer = len(game.turnOrder) - 1

@bot.command(
    name="start_game",
    description="Setup the game",
    scope=guild,
    options = [
        interactions.Option(
            name = "p1",
            description = "adds player 1",
            type = interactions.OptionType.USER,
            required = True
        ),
        interactions.Option(
            name = "p2",
            description = "adds player 2",
            type = interactions.OptionType.USER,
            required = True
        ),
        interactions.Option(
            name = "p3",
            description = "adds player 3",
            type = interactions.OptionType.USER,
            required = False
        ),
        interactions.Option(
            name = "p4",
            description = "adds player 4",
            type = interactions.OptionType.USER,
            required = False
        ),
        interactions.Option(
            name = "p5",
            description = "adds player 5",
            type = interactions.OptionType.USER,
            required = False
        ),
        interactions.Option(
            name = "p6",
            description = "adds player 6",
            type = interactions.OptionType.USER,
            required = False
        )
    ]
)
async def start_game(ctx: interactions.CommandContext, p1: interactions.User, p2: interactions.User, p3: interactions.User = None, p4: interactions.User = None, p5: interactions.User = None, p6: interactions.User = None):
    game.turnOrder = []
    game.playerOrder = []
    game.currentPlayer = 0
    game.drawStack = 0
    game.deck = None
    game.pile = None
    game.isIncrement = True

    global turnOrder
    global playerOrder
    turnOrder = [p1, p2]
    if p3 != None:
        turnOrder.append(p3)
    if p4 != None:
        turnOrder.append(p4)
    if p5 != None:
        turnOrder.append(p5)
    if p6 != None:
        turnOrder.append(p6)

    game.turnOrder = turnOrder
    game.deck = Deck()
    game.playerOrder = game.deck.distribute(turnOrder)
    if "yellow+4" not in game.emojis.keys():
        game.emojis["0"] = bot.guilds[0].emojis[0]
        game.emojis["1"] = bot.guilds[0].emojis[1]
        game.emojis["2"] = bot.guilds[0].emojis[2]
        game.emojis["3"] = bot.guilds[0].emojis[3]
        game.emojis["4"] = bot.guilds[0].emojis[4]
        game.emojis["5"] = bot.guilds[0].emojis[5]
        game.emojis["6"] = bot.guilds[0].emojis[6]
        game.emojis["7"] = bot.guilds[0].emojis[7]
        game.emojis["8"] = bot.guilds[0].emojis[8]
        game.emojis["9"] = bot.guilds[0].emojis[9]
        game.emojis["+2"] = bot.guilds[0].emojis[10]
        game.emojis["skip"] = bot.guilds[0].emojis[11]
        game.emojis["reverse"] = bot.guilds[0].emojis[12]
        game.emojis["blue"] = bot.guilds[0].emojis[13]
        game.emojis["red"] = bot.guilds[0].emojis[14]
        game.emojis["green"] = bot.guilds[0].emojis[15]
        game.emojis["yellow"] = bot.guilds[0].emojis[16]
        game.emojis["wild"] = bot.guilds[0].emojis[17]
        game.emojis["+4"] = bot.guilds[0].emojis[18]
        game.emojis["blue+4"] = bot.guilds[0].emojis[19]
        game.emojis["red+4"] = bot.guilds[0].emojis[20]
        game.emojis["green+4"] = bot.guilds[0].emojis[21]
        game.emojis["yellow+4"] = bot.guilds[0].emojis[22]
    await ctx.send("Your Turn! " + p1.mention + "\nCurrent card is " + game.pile.currentCard.toString(game.emojis), ephemeral = False, components = showHandButton)

@bot.command(
    name="use_card",
    description="In Game: Use a card",
    scope=guild,
    options = [
        interactions.Option(
            name = "color",
            description = "input the color",
            type = interactions.OptionType.STRING,
            required = True
        ),
        interactions.Option(
            name = "number_or_power",
            description = "input the number or power",
            type = interactions.OptionType.STRING,
            required = True
        )
    ]
)
async def use_card(ctx: interactions.CommandContext, color: str, number_or_power: str):
    if color == "y":
        color = "yellow"
    elif color == "r":
        color = "red"
    elif color == "g":
        color = "green"
    elif color == "b":
        color = "blue"
    if len(game.turnOrder) != 0:
        if ctx.author.id == turnOrder[game.currentPlayer].id:
            user = game.turnOrder[game.currentPlayer]
            player = game.playerOrder[game.currentPlayer]

            isSkip = False
            isReverse = False
            isDrawTwo = False
            isWild = False
            isDrawFour = False

            resultIndex = player.useCard(color, number_or_power)
            if resultIndex != -1 and resultIndex != -2:
                result = player.hand[resultIndex]
                previousCard = game.pile.stack[-1]
                isValid = False
                if result.isNumber and not player.hasToDraw:
                    if previousCard.isNumber:
                        if (result.number == previousCard.number) or (result.color == previousCard.color):
                            isValid = True
                    elif result.color == previousCard.color:
                        isValid = True
                elif result.isAction == True:
                    if result.power == "skip" and not player.hasToDraw:
                        if (result.color == previousCard.color) or (result.power == previousCard.power):
                            isValid = True
                            isSkip = True
                            advancePlayer()
                            skippedPlayer = turnOrder[game.currentPlayer]
                    elif result.power == "reverse" and not player.hasToDraw:
                        if (result.color == previousCard.color) or (result.power == previousCard.power):
                            isValid = True
                            isReverse = True
                            game.isIncrement = not game.isIncrement
                    elif result.power == "+2":
                        if (result.color == previousCard.color) or (result.power == previousCard.power):
                            isValid = True
                            isDrawTwo = True
                            game.drawStack += 2
                            playerToDrawIndex = game.currentPlayer
                            if game.isIncrement:
                                playerToDrawIndex += 1
                                if playerToDrawIndex >= len(game.turnOrder):
                                    playerToDrawIndex = 0
                            else:
                                playerToDrawIndex -= 1
                                if playerToDrawIndex <= -1:
                                    playerToDrawIndex = len(game.turnOrder) - 1
                            playerToDraw = game.playerOrder[playerToDrawIndex]
                            userToDraw = game.turnOrder[playerToDrawIndex]
                            player.hasToDraw = False
                            playerToDraw.hasToDraw = True
                elif result.isWild == True:
                    if result.power == "+4":
                        isValid = True
                        newCard = Card(color, None, "+4", isWild = True)
                        isDrawFour = True
                        game.drawStack += 4
                        playerToDrawIndex = game.currentPlayer
                        if game.isIncrement:
                            playerToDrawIndex += 1
                            if playerToDrawIndex >= len(game.turnOrder):
                                playerToDrawIndex = 0
                        else:
                            playerToDrawIndex -= 1
                            if playerToDrawIndex <= -1:
                                playerToDrawIndex = len(game.turnOrder) - 1
                        playerToDraw = game.playerOrder[playerToDrawIndex]
                        userToDraw = game.turnOrder[playerToDrawIndex]
                        player.hasToDraw = False
                        playerToDraw.hasToDraw = True
                    if result.power == "wild" and not player.hasToDraw:
                        isValid = True
                        newCard = Card(color, None, "wild", isWild = True)
                        isWild = True
                if isValid:
                    del player.hand[resultIndex]
                    player.hasDrawn = False
                    if result.isWild:
                        game.pile.addCard(newCard)
                        await ctx.send(user.mention + " played " + newCard.toString(game.emojis), ephemeral = False)
                    else:
                        game.pile.addCard(result)
                        await ctx.send(user.mention + " played " + result.toString(game.emojis), ephemeral = False)
                    if isSkip:
                        await ctx.send(skippedPlayer.mention + " got skipped LOL", ephemeral = False)
                    if isReverse:
                        await ctx.send(user.mention + " reversed the direction", ephemeral = False)
                    if isDrawTwo:
                        await ctx.send(userToDraw.mention + " might have to draw " + str(game.drawStack) + " cards", ephemeral = False)
                    if isWild:
                        await ctx.send(user.mention + " changed the color to " + color, ephemeral = False)
                    if isDrawFour:
                        await ctx.send(user.mention + " changed the color to " + color + " and " + userToDraw.mention + " might have to draw " + str(game.drawStack) + " cards", ephemeral = False)
                    if player.isFinished():
                        await ctx.send("GG! " + user.mention + " has 0 cards! " + user.mention + " won the game!", ephemeral = False)
                        game.turnOrder = []
                        game.playerOrder = []
                        game.currentPlayer = 0
                        game.drawStack = 0
                        game.deck = None
                        game.pile = None
                        game.isIncrement = True
                        return
                    num = random.random()
                    if num <= 0.1 and len(player.hand) > 0:
                        if len(player.hand) > 1:
                            await ctx.send("Oops! " + user.mention + " accidentally revealed that they have a " + random.choice(player.hand).toString(game.emojis), ephemeral = False)
                        elif len(player.hand) == 1:
                            await ctx.send("Oops! " + user.mention + " accidentally revealed that they have a " + random.choice(player.hand).color + " card", ephemeral = False)
                    if len(player.hand) == 1:
                        await ctx.send("UNO! " + user.mention + " has only 1 card left!", ephemeral = False, components = shoutUnoButton)
                    else:
                        advancePlayer()
                        nextUser = game.turnOrder[game.currentPlayer]
                        await ctx.send("Your Turn! " + nextUser.mention + "\nCurrent card is " + game.pile.currentCard.toString(game.emojis), ephemeral = False, components = showHandButton)
                else:
                    await ctx.send("That is not a valid card", ephemeral = True)
            elif resultIndex == -1:
                await ctx.send("You do not have that card", ephemeral = True)
            elif resultIndex == -2:
                await ctx.send("You have mispelled something", ephemeral = True)
        else:
            await ctx.send("It's not your turn", ephemeral = True)
    else:
        await ctx.send("There is currently no game being played", ephemeral = True)

@bot.command(
    name="game_stats",
    description="In Game: See the number of cards each player has",
    scope=guild,
)
async def game_stats(ctx: interactions.CommandContext):
    if len(game.turnOrder) != 0:
        statString = ""
        index = 0
        for player in game.playerOrder:
            statString += player.name + " has " + str(len(player.hand)) + " cards"
            if index != len(game.playerOrder) - 1:
                statString += "\n"
            index += 1
        await ctx.send(statString, ephemeral = True)
    else:
        await ctx.send("There is currently no game being played", ephemeral = True)

@bot.command(
    name="draw_card",
    description="In Game: Draw a card",
    scope=guild,
)
async def draw_card(ctx: interactions.CommandContext):
    if len(game.turnOrder) != 0:
        if ctx.author.id == turnOrder[game.currentPlayer].id:
            user = game.turnOrder[game.currentPlayer]
            player = game.playerOrder[game.currentPlayer]
            if not player.hasDrawn:
                if not player.hasToDraw:
                    card = game.deck.cards[-1]
                    player.hand.append(card)
                    del game.deck.cards[-1]
                    player.hasDrawn = True
                    player.isUnoCalled = False
                    await ctx.send(user.mention + " drew a card", ephemeral = False)
                    await ctx.send("You drew a " + card.toString(game.emojis), ephemeral = True)
                else:
                    await ctx.send("You can't draw right now", ephemeral = True)
            else:
                await ctx.send("You already drew a card this turn", ephemeral = True)
        else:
            await ctx.send("It's not your turn", ephemeral = True)
    else:
        await ctx.send("There is currently no game being played", ephemeral = True)

@bot.command(
    name="end_turn",
    description="In Game: When you have nothing to play",
    scope=guild,
)
async def end_turn(ctx: interactions.CommandContext):
    if len(game.turnOrder) != 0:
        if ctx.author.id == turnOrder[game.currentPlayer].id:
            user = game.turnOrder[game.currentPlayer]
            player = game.playerOrder[game.currentPlayer]

            player.hasDrawn = False
            await ctx.send(user.mention + " ended their turn", ephemeral = False)

            if player.hasToDraw:
                player.hand += (game.deck.cards[:game.drawStack])
                del game.deck.cards[:game.drawStack]
                await ctx.send(user.mention + " drew " + str(game.drawStack) + " cards", ephemeral = False)
                game.drawStack = 0
                player.hasToDraw = False
                player.isUnoCalled = False
            num = random.random()
            if num <= 0.1 and len(player.hand) > 0:
                if len(player.hand) > 1:
                    await ctx.send("Oops! " + user.mention + " accidentally revealed that they have a " + random.choice(player.hand).toString(game.emojis), ephemeral = False)
                elif len(player.hand) == 1:
                    await ctx.send("Oops! " + user.mention + " accidentally revealed that they have a " + random.choice(player.hand).color + " card", ephemeral = False)
            if len(player.hand) == 1:
                await ctx.send("UNO! " + user.mention + " has only 1 card left!", ephemeral = False, components = shoutUnoButton)
            else:
                advancePlayer()
                nextUser = game.turnOrder[game.currentPlayer]
                await ctx.send("Your Turn! " + nextUser.mention + "\nCurrent card is " + game.pile.currentCard.toString(game.emojis), ephemeral = False, components = showHandButton)
        else:
            await ctx.send("It's not your turn", ephemeral = True)
    else:
        await ctx.send("There is currently no game being played", ephemeral = True)

@bot.component("show_hand")
async def show_hand(ctx: interactions.CommandContext):
    if len(game.turnOrder) != 0:
        if ctx.author.id == turnOrder[game.currentPlayer].id:
            await ctx.send(game.playerOrder[game.currentPlayer].printHand(game.emojis), ephemeral = True)
        else:
            await ctx.send("It's not your turn", ephemeral = True)
    else:
        await ctx.send("There is currently no game being played", ephemeral = True)

@bot.component("shout_uno")
async def shout_uno(ctx: interactions.CommandContext):
    playerIndex = findPlayer(ctx.message.mentions[0]["username"])
    player = game.playerOrder[playerIndex]
    unoPerson = game.turnOrder[playerIndex]
    type = None
    lock.acquire()
    try:
        if not player.isUnoCalled:
            if len(player.hand) == 1:
                clicker = ctx.user
                if clicker.id == unoPerson.id:
                    type = 0
                    player.isUnoCalled = True
                else:
                    type = 1
                    player.hand += (game.deck.cards[:2])
                    del game.deck.cards[:2]
                    player.isUnoCalled = False
                advancePlayer()
                nextUser = game.turnOrder[game.currentPlayer]
            else:
                type = 2
        else:
            type = 3
    except Exception:
        lock.release()
        return
    lock.release()
    if type == 0:
        await ctx.send(unoPerson.mention + " has announced UNO")
        await ctx.send("Your Turn! " + nextUser.mention + "\nCurrent card is " + game.pile.currentCard.toString(game.emojis), ephemeral = False, components = showHandButton)
    elif type == 1:
        await ctx.send(clicker.mention + " has called out UNO faster than " + unoPerson.mention)
        await ctx.send(unoPerson.mention + " has drew 2 cards")
        await ctx.send("Your Turn! " + nextUser.mention + "\nCurrent card is " + game.pile.currentCard.toString(game.emojis), ephemeral = False, components = showHandButton)
    elif type == 2:
        await ctx.send(unoPerson.mention + " no longer has UNO", ephemeral = True)
    elif type == 3:
        await ctx.send(unoPerson.mention + " has already been accounted for UNO", ephemeral = True)

bot.start()