import os
from this import s
import discord
import discord.utils
from discord.ext import commands
import asyncio
from ..models import User, ServiceListing
from sqlalchemy.orm import scoped_session

from poe_service_matcher import app

from datetime import datetime
from tabulate import tabulate

from .services import database_services as dbs

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '$', intents = intents)

session = scoped_session(app.session_factory)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    print(f'received message: {message.content} from {message.author}')

    user = dbs.get_user(str(message.author.id))

        #print(f'{user.username}')

    if message.content.startswith('$service'):

        def parse(m):
            valid = False

            mm = [item.strip() for item in m.content.split(',')]

            if len(mm) == 4 and m.author == message.author:
                valid = True

                dbs.list_service(mm, user)

            return valid
        
        try:
            await message.channel.send('service name, map provided (y/n), slots, price in chaos \n example: \'uber sirus, y, 1, 50\'' )
            response = await bot.wait_for('message', check=parse, timeout=300)
            await message.channel.send(f'{response.content}')
        except asyncio.TimeoutError:
            await message.channel.send('poop de pewp de pantzes')

    elif message.content.startswith('$request'):

        def parse_wrapper(m):
            return asyncio.ensure_future(parse(m))

        async def parse(m):

            #print(f'parsing: {m.content}')

            valid = dbs.service_exists(m.content)

            if valid:
                response_message = dbs.parse_request(m.content)
                await message.channel.send(m.content)
                await message.channel.send(response_message)
            else:
                await message.channel.send('Service not currently listed.')

            return valid

        try:
            await message.channel.send('service name?')
            #print("Before bot.wait_for")
            response = await bot.wait_for('message', check=parse_wrapper, timeout=300)
            #print("After bot.wait_for")
            #await message.channel.send(f'{response.content}')
        except asyncio.TimeoutError:
            await message.channel.send('poop de pewp de pantzes?')

    elif message.content.startswith('$clear'):

        if user.username == '168865934675542016':
            dbs.clear_listings()
