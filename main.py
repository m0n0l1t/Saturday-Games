import discord
from discord.ext import commands
from config.settings import *
from models import *
from sqlalchemy import func

bot = commands.Bot(command_prefix='')


def last_letter(town):
    n = len(town)-1
    while town[n] == 'ы' or town[n] == 'ь' or town[n] == 'ъ':
        n -= 1
    return town[n]


@bot.event
async def on_message(message):
    message.content = message.content.lower()

    try:
        last = session.query(City).filter_by(is_last=1).first()

        try:
            ourCity = session.query(City).filter_by(name=message.content).first()
            if bot.user.id != message.author.id and ourCity is None:
                await message.channel.send("Такого города не существует")
            else:
                if last_letter(last.name) == ourCity.name[0]:
                    if ourCity.is_used == 0:
                        ourCity.is_used = 1
                        ourCity.is_last = 1
                        last.is_last = 0
                        session.commit()
                        channel = message.channel
                        await channel.send("Следующий город на букву ["+last_letter(ourCity.name)+"]")
                    else:
                        channel = message.channel
                        await channel.send("Этот город уже был")
                else:
                    channel = message.channel
                    await channel.send("Этот город не начинается на букву ["+last.name[len(last.name)-1]+"]")
        except ValueError:
            print("ошибка")
    except ValueError:
        print("ошибка")


bot.run(settings["token"])