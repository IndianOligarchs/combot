import discord
from discord.ext import commands, tasks
import datetime
from datetime import date
import regex as re
import os
import json
import asyncpg
import time

class Economy(commands.Cog, command_attrs=dict(hidden=True)):
    """These commands are all meant for the economy system, type !help [command] for a more in depth explanation."""
    def __init__(self, bot):
        self.bot = bot
        self.econtask.start()
        self.channel = self.bot.get_channel(799002935206871103)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        async with self.bot.pg_con.acquire() as con:
            await con.execute('INSERT INTO economy (user_id, total_coins) VALUES ($1, $2)', member.id, 0)



    @tasks.loop(seconds=60)
    async def econtask(self):
        timeout = 57   # [seconds]
        timeout_start = time.time()
        typed = []
        while time.time() < timeout_start + timeout:
            mes = await self.bot.wait_for('message')
            print(mes.content)
            if mes.author not in typed:
                typed.append(mes.author)
                async with self.bot.pg_con.acquire() as con:
                    val = await con.fetch('SELECT total_coins FROM economy WHERE user_id = $1', member.id)
                    if val == []:
                        await con.execute('INSERT INTO economy (user_id, total_coins) VALUES ($1, $2)', member.id, 0) 
                        await con.execute('UPDATE economy SET total_coins = total_coins + 10 WHERE user_id = $1', member.id)
                    else:
                        await con.execute('UPDATE economy SET total_coins = total_coins + 10 WHERE user_id = $1', member.id)


def setup(bot):
   bot.add_cog(Economy(bot))



