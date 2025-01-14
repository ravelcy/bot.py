import discord
from discord.ext import commands
from myserver import server_on

TOKEN = "bot-token" # ganti dengan token bot anda

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot {} telah online'.format(bot.user))

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, {}'.format(ctx.author.name.title()))

server_on()
bot.run(TOKEN)

sniped_messages = {}

@bot.event
async def on_message_delete(message):
    sniped_messages[message.channel.id] = message

@bot.command()
async def snipe(ctx):
    msg = sniped_messages.get(ctx.channel.id)
    if msg:
        await ctx.send(f"**{msg.author}**: {msg.content}")
    else:
        await ctx.send("Tidak ada pesan yang dapat disnipe.")

import random
import asyncio

@bot.command()
async def giveaway(ctx, duration: int, *, prize: str):
    await ctx.send(f"🎉 Giveaway dimulai! Hadiah: {prize}\nDurasi: {duration} detik.")
    await asyncio.sleep(duration)
    winner = random.choice(ctx.guild.members)
    await ctx.send(f"Selamat kepada {winner.mention} yang memenangkan **{prize}**!")

from youtube_dl import YoutubeDL

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()

    YDL_OPTIONS = {'format': 'bestaudio'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']

    vc.play(discord.FFmpegPCMAudio(url2))
    await ctx.send(f"Memutar musik dari {url}")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"Avatar {member.mention}: {member.avatar.url}")

import asyncio

@bot.event
async def on_message(message):
    if 'trigger' in message.content.lower():
        await asyncio.sleep(5)  # Delay 5 detik
        await message.channel.send("Auto response triggered!")
    await bot.process_commands(message)

import openai

openai.api_key = 'YOUR_API_KEY'

@bot.command()
async def ai(ctx, *, prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    await ctx.send(response.choices[0].text.strip())

