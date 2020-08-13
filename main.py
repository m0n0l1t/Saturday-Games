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


def lit_zero():
    for i in session.query(Literals).order_by(Literals.id):
        i.count = 0
    session.commit()


def count_lit():
    lit_zero()
    for i in session.query(Town).order_by(Town.id):
        lit = session.query(Literals).filter_by(name=i.first_literal).first()
        lit.count += 1
    session.commit()


def last_letter(town):
    n = len(town) - 1
    lit = session.query(Literals).filter_by(name=town[n]).first()
    while town[n] == 'ы' or town[n] == 'ь' or town[n] == 'ъ' or town[n] == ')' and lit.count == 0:
        n -= 1
        lit = session.query(Literals).filter_by(name=town[n]).first()

    return town[n]


def out():
    s = ""
    for instance in session.query(Literals).order_by(Literals.id):
        if instance is not None:
            s += f'{instance.name} {instance.count}\n'
    return s


def search_last():
    last = session.query(Town).filter_by(is_last=1).first()

    if last is not None:
        return last
    else:
        city_list = session.query(Town).all()
        last = random.choice(city_list)
        last.is_used = 1
        last.is_last = 1
        lit = session.query(Literals).filter_by(name=last.first_literal).first()
        lit.count = int(lit.count) - 1
        session.commit()
        return last


def clear_base():
    used = session.query(Town).filter_by(is_used=1).all()
    for i in used:
        i.is_used = 0
        i.is_last = 0
        session.commit()
    count_lit()


@bot.event
async def on_message(message):
    db()

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
    if msg == 'оставшиеся буквы':
        await message.channel.send(out())
    else:
        if msg == 'сначала':
            clear_base()
            last_city = search_last()
            await message.channel.send("Начнем с города **[" + last_city.name.upper() + "]**")
            await message.channel.send("Следующий город на букву [" + last_letter(last_city.name) + "]")
            return
        if msg == '.clear':
            await message.channel.purge(limit=100)
        our_city = session.query(Town).filter_by(name=msg).first()
        last_city = search_last()
        if our_city is None:
            await message.channel.purge(limit=1)
            await message.channel.send("Такого города не существует")
            await del_self()
        else:
            if last_letter(last_city.name) == our_city.first_literal:
                if our_city.is_used == 0:
                    our_city.is_used = 1
                    our_city.is_last = 1
                    last_city.is_last = 0
                    lit = session.query(Literals).filter_by(name=our_city.first_literal).first()
                    lit.count = int(lit.count) - 1
                    await message.channel.send("Следующий город на букву [" + last_letter(our_city.name) + "]")
                    session.commit()
                else:
                    await message.channel.send("Этот город уже был")
                    await del_self()
            else:
                await message.channel.send("Этот город не начинается на букву [" + last_letter(last_city.name) + "]")
                await del_self()


bot.run(settings["token"])
