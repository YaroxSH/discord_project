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
        except sqlite3.Error as err:
            await ctx.send(f'Запрос не был принят. {err.sqlite_errorname}')

    @commands.command(name='show')
    async def show(self, ctx, type, *args):
        con = sqlite3.connect('archive_bd')
        cur = con.cursor()
        no_res = False
        try:
            if type == 'rank':
                res = cur.execute("""SELECT name, context, rank FROM archive""").fetchall()
                res = sorted(res, key=lambda x: x[2], reverse=True)
                res = list(map(lambda x: (str(x[2]), x[0], x[1]), res))
            elif type == 'name':
                res = cur.execute("""SELECT name, context FROM archive WHERE name = ?""", args).fetchall()
            elif type == 'search':
                args = ' '.join(args)
                res = cur.execute("""SELECT name, context FROM archive""").fetchall()
                res = list(map(lambda x: x if args in x[0] else '', res))
            elif type == 'all':
                res = cur.execute("""SELECT name, context FROM archive""").fetchall()
        except sqlite3.Error as err:
            await ctx.send(f'Запрос не был принят. {err.sqlite_errorname}')
            no_res = True
        con.commit()
        cur.close()
        if not no_res:
            hum_res = '\n'.join(list(map(lambda x: ' : '.join(x), res)))
            await ctx.send(hum_res)

    @commands.command(name='delete')
    async def delete(self, ctx, *args):
        con = sqlite3.connect('archive_bd')
        cur = con.cursor()
        nm = ' '.join(args)
        try:
            self.reser = cur.execute("""SELECT * FROM archive WHERE name = ?""", (nm,))
            res = cur.execute("""DELETE FROM archive WHERE name = ?""", (nm,))
            await ctx.send(f'Данные под именем {nm} были успешно удалены.')
        except sqlite3.Error as err:
            await ctx.send(f'Запрос не был принят. {err.sqlite_errorname}')
        con.commit()
        cur.close()

    @commands.command(name='runback')
    async def runback(self, ctx):
        con = sqlite3.connect('archive_bd')
        cur = con.cursor()
        try:
            res = cur.execute("""INSERT INTO archive (id, name, context, rank) VALUES (?, ?, ?)""",
                              self.reser)
            await ctx.send('Удаленые было успешно удалено.')
        except sqlite3.Error as err:
            await ctx.send(f'Запрос не был принят. {err.sqlite_errorname}')
        con.commit()
        cur.close()


bot = commands.Bot(command_prefix='!#', intents=intents, help_command=commands.MinimalHelpCommand())


async def main():
    await bot.add_cog(Bot_things(bot))
    await bot.start(TOKEN)


asyncio.run(main())