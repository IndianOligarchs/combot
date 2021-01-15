from num2words import num2words
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

class Economy(commands.Cog, command_attrs=dict(hidden=True)):
    """These commands are all meant for the economy system, type !help [command] for a more in depth explanation."""
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 60.0, commands.BucketType.user)





#-----------------------------------------------------------------------------------------backend---------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            bucket = self._cd.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                pass
            else:
                query = """
                        INSERT INTO economy (user_id, coins) 
                        VALUES ($1, 1)
                        ON CONFLICT (user_id) DO UPDATE SET coins = economy.coins + 1
                        """
                async with self.bot.pg_con.acquire() as con:
                    await con.execute(query, message.author.id)

#-----------------------------------------------------------------------------------------backend-----------------------------------------
#-----------------------------------------------------------------------------------------frontend----------------------------------------
    @commands.command()
    async def top(self, ctx):
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color.blue(), title='Top Ten Richest Users in Comfy Gamers!')
        query = """
                SELECT * FROM economy 
                ORDER BY coins desc
                LIMIT 10
                """
        
        async with self.bot.pg_con.acquire() as con:
            results = await con.fetch(query)
        num = 1
        for user in results:
            member = await ctx.guild.fetch_member(user[0])
            embed.add_field(name=f'#{num} {member.name}#{member.discriminator} - {user[1]} coins', value = '\u200b', inline=False)
            num = num + 1
        await ctx.send(embed=embed)


    @commands.command()
    async def bal(self, ctx, user: typing.Optional[discord.User]):
        if user == None:
            user = ctx.author
        query = """
                SELECT * FROM economy 
                ORDER BY coins desc
                """
        async with self.bot.pg_con.acquire() as con:
            results = await con.fetch(query)
        for count, value in enumerate(results):
            if value[0] == user.id:
                rank = num2words(count + 1, to='ordinal_num')
                coins = value[1]
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color.blue(), title=f"{user.name}#{user.discriminator}'s Balance", description=f"{user.name}#{user.discriminator} has {coins} coins and is in {rank} place.")
        await ctx.send(embed=embed)


    @commands.command(aliases=['rcoins'])
    @commands.has_permissions(administrator=True)
    async def removecoins(self, ctx, user: discord.Member, amount: int):
        async with self.bot.pg_con.acquire() as con:
            await con.execute('UPDATE economy SET coins = coins - $1 WHERE user_id = $2', amount, user.id)
        await ctx.send(f"{ctx.author.mention}, :white_check_mark:, I removed {amount} coins from {user.mention}'s balance.")


    @commands.command(aliases=['acoins'])
    @commands.has_permissions(administrator=True)
    async def addcoins(self, ctx, user: discord.Member, amount: int):
        async with self.bot.pg_con.acquire() as con:
            await con.execute('UPDATE economy SET coins = coins + $1 WHERE user_id = $2', amount, user.id)
        await ctx.send(f"{ctx.author.mention}, :white_check_mark:, I added {amount} coins to {user.mention}'s balance.")


    @commands.command()
    async def pay(self, ctx, user: discord.Member, amount: int):
        async with self.bot.pg_con.acquire() as con:
            await con.execute('UPDATE economy SET coins = coins - $1 WHERE user_id = $2', amount, ctx.author.id)
            await con.execute('UPDATE economy SET coins = coins + $1 WHERE user_id = $2', amount, user.id)
        await ctx.send(f"{ctx.author.mention}, :white_check_mark:, I payed {user.mention} {amount} coins from your bank.")
 

    def is_guild_owner():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)


    @commands.command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def resetall(self, ctx):
        await ctx.send('Are you sure you want to reset the Economy System? Respond with "yes" if you are.')
        def check(message):
            return message.content.lower() in ["yes", "yes."] and message.author.id in [713979128969429012, 673716808574042143] and message.channel == ctx.channel
        await self.bot.wait_for('message', check=check)
        async with self.bot.pg_con.acquire() as con:
            await con.execute('DELETE FROM economy')
        await ctx.send('I have reset the Economy System.')

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(color=discord.Color.orange(), timestamp=datetime.datetime.now())
        embed.set_author(name='ComfyGamers Shop')
        embed.add_field(name='How to buy and item from the shop?', value='```c!buy [item id] [quantity]```', inline=False)
        embed.add_field(name='100 ComfyXP', value='Price: 20 ComfyCoins\nID: 1', inline=False)
        embed.add_field(name='250 ComfyXP', value='Price: 50 ComfyCoins\nID: 2', inline=False)
        embed.add_field(name='500 ComfyXP', value='Price: 100 ComfyCoins\nID: 3', inline=False)
        embed.add_field(name='1000 ComfyXP', value='Price: 200 ComfyCoins\nID: 4', inline=False)
        embed.add_field(name='2000 ComfyXP', value='Price: 400 ComfyCoins\nID: 5', inline=False)
        await ctx.send(embed=embed)
        #embed.add_field(name='Custom Role + Custom Role Color', value='Price: 7500 ComfyCoins\nID: 0')



def setup(bot):
   bot.add_cog(Economy(bot))



