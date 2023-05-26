import os
from this import s
import discord
import discord.utils
from discord.ext import commands
import asyncio

from poe_service_matcher import db, app
from ..services import database_services as dbs

from ..session_context import create_session

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '$', intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    with app.app_context():
        if message.author == bot.user:
            return

        print(f'received message: {message.content} from {message.author}')

        user = None
        with create_session(db.engine) as session:
            user = dbs.get_user(str(message.author.id), session)

        if message.content.startswith('$service'):
            def parse(m):
                valid = False

                mm = [item.strip() for item in m.content.split(',')]

                if len(mm) == 4 and m.author == message.author:
                    valid = True
                    with create_session(db.engine) as session:
                        dbs.list_service(mm, user, session)
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
                with create_session(db.engine) as session:
                    valid = dbs.service_exists(m.content, session)

                    if valid:
                        response_message = dbs.parse_request(m.content, session)
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
                with create_session(db.engine) as session:
                    dbs.clear_listings(session)
