from function import *
import os

channel_list = []


@bot.event
async def on_ready():
    db()
    for i in session.query(Literals).order_by(Literals.id):
        channel_list.append(i.channel_id)
    print('Ready!')


@bot.event
async def on_message(message):
    channel_id = message.channel.id
    if bot.user.id == message.author.id:
        return
    msg = message.content.lower()

    if msg == 'clear':
        await message.channel.purge(limit=100)
    elif msg == 'help city':

        embed = discord.Embed(title="Команды",
                              color=0x45d370)
        embed.add_field(name='start city', value="начать игру на этом канале", inline=False)
        embed.add_field(name='stop city', value="закончить игру на этом канале", inline=False)
        embed.add_field(name='letter', value="оставшиеся буквы", inline=False)
        embed.add_field(name='clear', value="очистка 100 сообщений", inline=False)


        await message.channel.send(embed=embed)
    elif channel_id not in channel_list:
        if msg == 'start city':
            channel_list.append(channel_id)
            start_game(channel_id)

            last_city = search_last(channel_id)
            embed = discord.Embed(title=":green_square: Начнем с города **[" + last_city.name.upper() + "]**",
                                  description=f"Следующий город на букву [{last_letter(last_city.name, channel_id)}]",
                                  color=0x45d370)

            await message.channel.send(embed=embed)

            return
        else:
            return
    elif channel_id in channel_list:
        used_list = []
        for i in session.query(Used).filter_by(channel_id=channel_id).order_by(Used.id):
            used_list.append(i.used_city)
        lit = session.query(Literals).filter_by(channel_id=channel_id).first()
        if msg == 'stop city':
            channel_list.remove(channel_id)
            stop_game(channel_id)
            await message.channel.send('игра остановлена')
        elif msg == 'letter':
            embed = discord.Embed(title="Оставшиеся буквы",
                                  color=0x45d370)
            c = 0
            for i in fmtw(lit):
                c += 1
                if c == 24:
                    break
                else:
                    embed.add_field(name=i, value=fmtw(lit)[i], inline=True)
            await message.channel.send(embed=embed)
            embed = discord.Embed(color=0x45d370)
            embed.add_field(name='ш', value=fmtw(lit)['ш'], inline=True)
            embed.add_field(name='щ', value=fmtw(lit)['щ'], inline=True)
            embed.add_field(name='э', value=fmtw(lit)['э'], inline=True)
            embed.add_field(name='ю', value=fmtw(lit)['ю'], inline=True)
            embed.add_field(name='я', value=fmtw(lit)['я'], inline=True)
            await message.channel.send(embed=embed)
        else:
            our_city = session.query(Town).filter_by(name=msg).first()
            last_city = search_last(channel_id)
            if our_city is None:
                await message.channel.purge(limit=1)
                embed = discord.Embed(title=f":red_circle: **{msg.upper()}** Такого города не существует",
                                      description="Попробуй вспомнить другой",
                                      color=0xd34545)

                await message.channel.send(embed=embed)
                await del_self(message)
            else:
                if last_letter(last_city.name, channel_id) == our_city.first_literal:
                    if our_city.id not in used_list:
                        session.add(Used(channel_id, our_city.id))
                        lit.last = our_city.id
                        lit_count(channel_id, our_city.id)
                        embed = discord.Embed(
                            title=":green_square: В точку!",
                            description=f"Следующий город на букву [{last_letter(our_city.name, channel_id)}]",
                            color=0x45d370)

                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.purge(limit=1)
                        embed = discord.Embed(title=f":red_circle: **{msg.upper()}** Этот город уже был ",
                                              description="Попробуй вспомнить другой",
                                              color=0xd34545)
                        embed.set_footer(text=str(datetime.today()))
                        await message.channel.send(embed=embed)
                        await del_self(message)
                else:
                    await message.channel.purge(limit=1)
                    s = f"**{our_city.name.upper()} **Этот город не начинается на букву [{last_letter(last_city.name,channel_id)}]"
                    embed = discord.Embed(title=s,
                                          description="Попробуй вспомнить другой",
                                          color=0xd34545)
                    await message.channel.send(embed=embed)

                    await del_self(message)


token = os.environ.get('BOT_TOKEN')
bot.run(str(token))

