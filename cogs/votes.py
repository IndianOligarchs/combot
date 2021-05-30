from aiohttp import web
import discord
from discord.ext import commands, tasks
import datetime
from datetime import timedelta

class Votes(commands.Cog):
    """All commands dealing with the vote tracking system on top.gg"""
    def __init__(self, bot):
        self.bot = bot
        self.maindict = {}
        self.app = web.Application()
        self.routes = web.RouteTableDef()
        self.app.add_routes(routes)
        web.run_app(app)


    @self.routes.post('/webhook')
    async def viewpost(self, request):
        json = await request.json()
        self.maindict.update({json['user']: datetime.datetime.utcnow()})


    @tasks.loop(seconds=60)
    async def refresh(self):
        await self.bot.wait_until_ready()
        for key, value in self.maindict:
            voteagaintime = value + timedelta(seconds=10)
            votetruefalse = voteagaintime <= datetime.datetime.utcnow()
            if votetruefalse is True:
                member = await self.bot.fetch_user(key)
                await member.send('You can now vote again!')



def setup(bot):
    bot.add_cog(Votes(bot))

                
