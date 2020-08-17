import asyncio
import discord
from discord.ext import commands
from models import *
from collections import deque

bot = commands.Bot(command_prefix='')
black_list = deque()
operation = 0

lit = {
    'а': 567,
    'б': 902,
    'в': 703,
    'г': 441,
    'д': 399,
    'е': 96,
    'ж': 65,
    'з': 169,
    'и': 266,
    'й': 30,
    'к': 1211,
    'л': 455,
    'м': 637,
    'н': 460,
    'о': 286,
    'п': 558,
    "р": 337,
    'с': 855,
    'т': 455,
    'у': 170,
    'ф': 227,
    'х': 338,
    'ц': 31,
    'ч': 217,
    'ш': 177,
    'щ': 12,
    'э': 137,
    'ю': 37,
    'я': 68
}


def fmtw(literal):
    lit = {
        'а': literal.l1,
        'б': literal.l2,
        'в': literal.l3,
        'г': literal.l4,
        'д': literal.l5,
        'е': literal.l6,
        'ж': literal.l7,
        'з': literal.l8,
        'и': literal.l9,
        'й': literal.l10,
        'к': literal.l11,
        'л': literal.l12,
        'м': literal.l13,
        'н': literal.l14,
        'о': literal.l15,
        'п': literal.l16,
        "р": literal.l17,
        'с': literal.l18,
        'т': literal.l19,
        'у': literal.l20,
        'ф': literal.l21,
        'х': literal.l22,
        'ц': literal.l23,
        'ч': literal.l24,
        'ш': literal.l25,
        'щ': literal.l26,
        'э': literal.l27,
        'ю': literal.l28,
        'я': literal.l29
    }
    return lit


def equally_lit(literal, lit):
    literal.l1 = lit['а']
    literal.l2 = lit['б']
    literal.l3 = lit['в']
    literal.l4 = lit['г']
    literal.l5 = lit['д']
    literal.l6 = lit['е']
    literal.l7 = lit['ж']
    literal.l8 = lit['з']
    literal.l9 = lit['и']
    literal.l10 = lit['й']
    literal.l11 = lit['к']
    literal.l12 = lit['л']
    literal.l13 = lit['м']
    literal.l14 = lit['н']
    literal.l15 = lit['о']
    literal.l16 = lit['п']
    literal.l17 = lit['р']
    literal.l18 = lit['с']
    literal.l19 = lit['т']
    literal.l20 = lit['у']
    literal.l21 = lit['ф']
    literal.l22 = lit['х']
    literal.l23 = lit['ц']
    literal.l24 = lit['ч']
    literal.l25 = lit['ш']
    literal.l26 = lit['щ']
    literal.l27 = lit['э']
    literal.l28 = lit['ю']
    literal.l29 = lit['я']
    session.commit()


def lit_count(channel_id, city_id):
    city = session.query(Town).filter_by(id=city_id).first()
    print(city.name)
    literal = session.query(Literals).filter_by(channel_id=channel_id).first()
    lit = fmtw(literal)
    for i in lit:
        if city.first_literal == i:

            lit[i] -= 1

    equally_lit(literal, lit)




def lit_zero():
    for i in session.query(Literals).order_by(Literals.id):
        i.count = 0
    session.commit()


def count_lit():
    lit_zero()


def last_letter(town, channel_id):
    n = len(town) - 1
    literal = session.query(Literals).filter_by(channel_id=channel_id).first()
    lit_list = fmtw(literal)

    while town[n] == 'ы' or town[n] == 'ь' or town[n] == 'ъ' or town[n] == ')' or town[n] == 'ё' and lit_list[town[n]] == 0:
        n -= 1

    return town[n]


def out(channel_id):
    s = ""
    literal = session.query(Literals).filter_by(channel_id=channel_id).first()
    for i in fmtw(literal):
        s += f'{i} {fmtw(literal)[i]}\n'
    return s


def search_last(channel_id):
    lit = session.query(Literals).filter_by(channel_id=channel_id).first()
    last = session.query(Town).filter_by(id=lit.last).first()
    print(last.name)
    return last


def stop_game(channel_id):
    session.delete(session.query(Literals).filter_by(channel_id=channel_id).first())
    for i in session.query(Used).filter_by(channel_id=channel_id).order_by(Used.id):
        session.delete(i)
    session.commit()


def start_game(channel_id):
    lit = Literals(channel_id)
    session.add(lit)
    last = session.query(Town).filter_by(id=lit.last).first()
    print(last.name)
    used = Used(channel_id, lit.last)
    session.add(used)
    session.commit()
    lit_count(channel_id, lit.last)



