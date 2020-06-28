import discord
import random
from discord.ext import commands
from config.settings import *
from models import *
import os

bot = commands.Bot(command_prefix='')
black_list = [0, 1, 2]
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
    used = session.query(City).filter_by(is_used=1).all()
    for i in used:
        i.is_used = 0
        i.is_last = 0
        session.commit()


@bot.event
async def on_message(message):
    if bot.user.id == message.author.id:
        return
    msg = message.content.lower()
    if msg == 'сначала':
        clear_base()
        last_city = search_last()
        await message.channel.send("Начнем с города **[" + last_city.name.upper() + "]**")
        await message.channel.send("Следующий город на букву [" + last_letter(last_city.name) + "]")

    if message.author.id not in black_list:

    else:

        our_city = session.query(City).filter_by(name=msg).first()
        last_city = search_last()
        if our_city is None:
            await message.channel.send("Такого города не существует")

        else:
            if last_letter(last_city.name) == our_city.name[0]:
                if our_city.is_used == 0:
                    our_city.is_used = 1
                    our_city.is_last = 1
                    last_city.is_last = 0
                    await message.channel.send("Следующий город на букву [" + last_letter(our_city.name) + "]")
                    session.commit()
                else:
                    await message.channel.send("Этот город уже был")
            else:
                await message.channel.send("Этот город не начинается на букву [" + last_letter(last_city.name) + "]")

bot.run(settings["token"])
