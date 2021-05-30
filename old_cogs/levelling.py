import discord
from discord.ext import commands, tasks
import datetime
from datetime import date
import regex as re
import os
import json
import asyncpg
import time
import typing

class Exp(commands.Cog, command_attrs=dict(hidden=True)):
    """These commands are all meant for the economy system, type !help [command] for a more in depth explanation."""
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 60.0, commands.BucketType.user)



    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            bucket = self._cd.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                pass
            else:
                query = """
                        INSERT INTO xp (user_id, xpnum) 
                        VALUES ($1, 15)
                        ON CONFLICT (user_id) DO UPDATE SET xpnum = xp.xpnum + 15
                        """
                async with self.bot.pg_con.acquire() as con:
                    await con.execute(query, message.author.id)


def setup(bot):
   bot.add_cog(Exp(bot))
