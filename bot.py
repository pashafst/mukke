import asyncio
import os
import discord
from dotenv import load_dotenv

from discord.ext import commands

import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

initial_extensions = ['Music']

bot = commands.Bot(command_prefix="!", intents=intents)
for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='deez')
async def deez(ctx):
    response = 'nuts' 
    await ctx.send(response)

@bot.command(name='alesan')
async def alesan(ctx):
    alesans = [
            'boker',
            'belanja gua',
            'masak',
            ]
    response = "sori coy tadi abis " + random.choice(alesans)
    await ctx.send(response)


challengers = []
sem_challengers = asyncio.Semaphore(1)

cards = []
for i in range(1,11):
    cards.append(str(i))
cards += ['J','Q','K','A']

@bot.command(name='hi_lo',help='Main hi lo card game')
async def hilo(ctx, user: discord.Member):
    if ctx.author.id in challengers:
        await ctx.send(f'{ctx.author.mention} sabar goblok dah nantang lu')
        return

    # add challenger to list
    async with sem_challengers:
        challengers.append(ctx.author.id)

    # Check if user exists, send challenge
    found = False
    for member in ctx.channel.members:
        if member == user:
            found = True
            break
    if not found:
        await ctx.send("Can't challenge, user not found")
        return

    await ctx.send(f'{user.mention} is challenged! type \'accept\' to accept the challenge 10 detik')

    def check(message):
        return message.author == user and message.content == 'accept'

    try:
        await bot.wait_for('message', check=check, timeout=10.0)
    except asyncio.TimeoutError:
        challengers.remove(ctx.author.id)
        await ctx.send(f'{user.mention} pengecut broh')
    else:
        challengers.remove(ctx.author.id)
        await ctx.send('RESULT:')
        hands = {ctx.author: random.choice(cards), user: random.choice(cards)}
        response = f'{ctx.author.mention}: {hands[ctx.author]}'
        await ctx.send(response)
        response = f'{user.mention}: {hands[user]}'
        await ctx.send(response)

        # check winner loser
        if hands[ctx.author] > hands[user]:
            await ctx.send(f'{ctx.author.mention} wins!')
        elif hands[ctx.author] < hands[user]:
            await ctx.send(f'{user.mention} wins!')
        else:
            await ctx.send('Draw')

@bot.command(name='debug')
async def debug(ctx):
    await ctx.send(challengers)

bot.run(TOKEN)