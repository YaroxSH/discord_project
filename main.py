import asyncio
import sqlite3

import discord
from discord.ext import commands
import logging
from config import TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


class Bot_things(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='archivate')
    async def archivate(self, ctx, name, rank, *args):
        con = sqlite3.connect('archive_bd')
        cur = con.cursor()
        self.name = name
        self.rank = int(rank)
        self.message = ' '.join(args)
        try:
            insert = cur.execute(f'INSERT INTO archive (name, context, rank) VALUES (?, ?, ?)',
            (self.name, self.message, self.rank))
            con.commit()
            cur.close()
            await ctx.send('Данные успешно сохранены.')
        except sqlite3.Error:
            await ctx.send('Запрос не был принят, если вы не знаете как правильно писать команды введите "!#help_b".')

    @commands.command(name='help_b')
    async def help_b(self, ctx):
        await ctx.send('''Тут записан формат записи команд данного бота:
            !#archivate "имя архива"  "важность архива(от 1 до 10)"  "содержание архива"''')

    async def show(self, ctx, type, *args):
        con = sqlite3.connect('archive_bd')
        cur = con.cursor()
        if type == 'rank':
            pass
        elif type == 'name':
            pass
        elif type == 'search':
            pass


bot = commands.Bot(command_prefix='!#', intents=intents)


async def main():
    await bot.add_cog(Bot_things(bot))
    await bot.start(TOKEN)


asyncio.run(main())