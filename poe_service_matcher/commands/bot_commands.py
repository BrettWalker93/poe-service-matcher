import os
import discord
from discord.ext import commands
import asyncio
from ..models import User, ServiceListing
from poe_service_matcher import app
from poe_service_matcher.database import db

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

    print(f'received message: {message}')

    with app.app_context():
        user = User.query.filter_by(username=str(message.author.id)).first()

        if not user:
            new_user = User(username=str(message.author.id))
            with db.session.begin():
                db.session.add(new_user)
                db.session.commit()

    if message.content.startswith('$service'):

        def parse(m):
            valid = False

            mm = m.content.split(',')

            if len(mm) == 4 and m.author == message.author:
                valid = True

                with app.app_context():
                    new_service = ServiceListing(
                        user_id=user.id,
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
            