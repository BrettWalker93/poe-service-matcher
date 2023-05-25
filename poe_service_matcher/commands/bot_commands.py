from asyncio.windows_events import NULL
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '$', intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.content.startswith('$service'):

        def parse(m):
            return m.author == message.author
        
        try:
            response = await bot.wait_for('message', check=parse, timeout=300)
            await message.channel.send(f"{response.content}")
        except asyncio.TimeoutError:
            await message.channel.send("")
            