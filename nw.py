import discord
from discord.ext import commands, tasks
import random
import asyncio
import json

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load your token from a secure place
TOKEN = 'YOUR_BOT_TOKEN'

# Snipe feature
snipe_message_content = {}
snipe_message_author = {}

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    snipe_message_content[message.channel.id] = message.content
    snipe_message_author[message.channel.id] = message.author

@bot.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        embed = discord.Embed(title="Snipe", description=snipe_message_content[channel.id], color=0x00ff00)
        embed.set_footer(text=f"Deleted by {snipe_message_author[channel.id]}")
        await ctx.send(embed=embed)
    except KeyError:
        await ctx.send("No message to snipe!")

# Giveaway feature
@bot.command()
@commands.has_permissions(manage_roles=True)
async def giveaway(ctx, duration: int, *, prize: str):
    await ctx.send(f"Giveaway started! Prize: {prize}. Duration: {duration} seconds.")
    await asyncio.sleep(duration)
    await ctx.send(f"Giveaway ended! Winner: {random.choice(ctx.guild.members)}")

# Echo feature
@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

# Ban feature
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")

# Timeout feature
@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int):
    await member.timeout(duration=discord.utils.utcnow() + timedelta(seconds=duration))
    await ctx.send(f"{member.mention} has been timed out for {duration} seconds.")

# Avatar feature
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=0x00ff00)
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

# Auto Responder
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "trigger" in message.content.lower():
        embed = discord.Embed(title="Auto Response", description="This is an auto response!", color=0x00ff00)
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

# Music feature (basic)
@bot.command()
async def play(ctx, url: str):
    # Implement music playing logic here
    await ctx.send(f"Playing music from {url}")

# AI feature (basic)
@bot.command()
async def chatgpt(ctx, *, question: str):
    # Implement AI chat logic here
    await ctx.send(f"ChatGPT response to: {question}")

# Reaction role feature
@bot.command()
async def reaction_role(ctx, role: discord.Role):
    await ctx.send(f"React with 👍 to get the {role.name} role!")

# Purge feature
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)

# Leveling feature (basic)
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Implement leveling logic here

    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
