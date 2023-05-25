import os
from this import s
import discord
import discord.utils
from discord.ext import commands
import asyncio
from ..models import User, ServiceListing
from poe_service_matcher import app
from poe_service_matcher.database import db
from datetime import datetime
from tabulate import tabulate

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '$', intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    print(f'received message: {message.content} from {message.author}')

    with app.app_context():
        user = User.query.filter_by(username=str(message.author.id)).first()

        if not user:
            user = User(username=str(message.author.id))
            db.session.add(user)
            db.session.commit()

        #print(f'{user.username}')

    if message.content.startswith('$service'):

        def parse(m):
            valid = False

            mm = [item.strip() for item in m.content.split(',')]

            if len(mm) == 4 and m.author == message.author:
                valid = True

                with app.app_context():
                    new_service = ServiceListing(
                        user_id=user.username,
                        service=mm[0],
                        map_provided=(True if mm[1] == 'y' else False),
                        slots=int(mm[2]),
                        price=int(mm[3])
                    )
                    db.session.add(new_service)
                    db.session.commit()

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

            valid = False
            
            service = None

            with app.app_context():
                service = ServiceListing.query.filter_by(service=m.content).first()

            if service is not None:
                valid = True

                services = None

                with app.app_context():
                    services = ServiceListing.query.filter_by(service=m.content).order_by(ServiceListing.time_listed).all()

                service_info = []
                for service in services:
                    username = f'<@{service.user_id}>'
                    service_info.append((username, service.price))

                table = tabulate(service_info, headers=["Provider", "Price"], tablefmt="simple")

                response_message = f"Services:\n\n{table}"

                await message.channel.send(service.service)
                await message.channel.send(response_message)

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
            with app.app_context():
                db.session.query(ServiceListing).delete()
                db.session.commit()
