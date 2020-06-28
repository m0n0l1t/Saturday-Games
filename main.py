import asyncio

import discord
import random
from discord.ext import commands
from config.settings import *
from models import *
from collections import deque

bot = commands.Bot(command_prefix='')
black_list = deque()
operation = 0


def last_letter(town):
    n = len(town)-1
    while town[n] == 'ы' or town[n] == 'ь' or town[n] == 'ъ' or town[n] == ')':
        n -= 1
    return town[n]


def search_last():
    last = session.query(City).filter_by(is_last=1).first()

    if last is not None:
        return last
    else:
        city_list = session.query(City).all()
        last = random.choice(city_list)
        last.is_used = 1
        last.is_last = 1
        session.commit()
        return last


def clear_base():
    while len(black_list) != 0:
        black_list.popleft()

    black_list.append(0)
    black_list.append(0)
    used = session.query(City).filter_by(is_used=1).all()
    for i in used:
        i.is_used = 0
        i.is_last = 0
        session.commit()






@bot.event
async def on_message(message):
    def check(user, reaction):
        return user == message.author and str(reaction.emoji) == '👍'

    async def del_self():
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.purge(limit=1)
        else:
            await message.channel.send('👍')

    if bot.user.id == message.author.id:
        return
    msg = message.content.lower()
    if msg == 'сначала':
        clear_base()
        last_city = search_last()
        await message.channel.send("Начнем с города **[" + last_city.name.upper() + "]**")
        await message.channel.send("Следующий город на букву [" + last_letter(last_city.name) + "]")
        return
    if msg == '.clear':
        await message.channel.purge(limit=100)
    if message.author.id in black_list:
        await message.channel.purge(limit=1)
        await message.channel.send(f'Вы уже загадали город {message.author.mention}, дождитесь следующих участников')
        await del_self()
    else:
        our_city = session.query(City).filter_by(name=msg).first()
        last_city = search_last()
        if our_city is None:
            await message.channel.purge(limit=1)
            await message.channel.send("Такого города не существует")
            await del_self()
        else:
            if last_letter(last_city.name) == our_city.name[0]:
                if our_city.is_used == 0:
                    our_city.is_used = 1
                    our_city.is_last = 1
                    last_city.is_last = 0
                    await message.channel.send("Следующий город на букву [" + last_letter(our_city.name) + "]")
                    session.commit()
                    black_list.popleft()
                    black_list.append(message.author.id)
                else:
                    await message.channel.send("Этот город уже был")
                    await del_self()
            else:
                await message.channel.send("Этот город не начинается на букву [" + last_letter(last_city.name) + "]")
                await del_self()

bot.run(settings["token"])
