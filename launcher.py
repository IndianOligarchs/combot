import datetime
import asyncio
import discord
import traceback
from discord.ext import commands
import asyncpg
from discord import Intents
intents = Intents.all()
token='Nzk5MDAzMjExMzcyNDI5Mzcz.X_9Pug.tgU5PBdfi4WFggdZt0rKaUiUD1M'
bot = commands.Bot(command_prefix='!', case_insensitive=True, activity=discord.Game(name='ComfyBot | !help'))
initial_extensions = [
#                    'cogs.economy',
                    'cogs.help',
#                    'cogs.levelling'
                    'cogs.votes'
                     ]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    print('All cogs have been loaded!')




@bot.event
async def on_ready():
    bot.channel = bot.get_channel(799002935206871103)
    print('Running')



async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database='comfybot', user='admin', password='kris1213A')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title='ERROR', description=f'You are missing the correct permissions to run this command. You need {error.missing_perms[0]}.')
        await ctx.send(embed=embed)
    elif isinstance(error, commands.NotOwner):
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title='ERROR', description=f'You are missing the correct permissions to run this command. You need to own this bot.')
        await ctx.send(embed=embed)
    else:
        etype = type(error)
        trace = error.__traceback__
        lines = traceback.format_exception(etype, error, trace)
        traceback_text = ''.join(lines)
        channel = bot.get_channel(799016100167024670)
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title='ERROR', description=f'An error has occured: ```{traceback_text}```')
        await channel.send(embed=embed)




bot.loop.run_until_complete(create_db_pool())    
bot.run(token)


