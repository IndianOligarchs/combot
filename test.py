import asyncio
import asyncpg


async def test():
    pg_con = await asyncpg.create_pool(database='comfybot', user='admin', password='kris1213K')
    async with pg_con.acquire() as con:
        val = await con.fetch('SELECT total_coins FROM economy WHERE user_id = $1', 713979128969429012)
        if val[0] == None:
            print('It works as expected')
        else:
            print('Unfortunately it does not work.')
asyncio.run(test())
