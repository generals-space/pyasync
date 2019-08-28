import time
import asyncio

import asyncpg

db_config = {
    'host': 'localhost',
    'port': '5432',
    'database': 'mydb',
    'user': 'my',
    'password': '123456',
}

db_pool = None
sem = asyncio.Semaphore(100)

async def initdb():
    async with db_pool.acquire() as db_conn:
        await db_conn.execute('create table if not exists test(id serial primary key, name varchar(50));')
        await db_conn.execute('delete from test;')

async def insert_async(i):
    ## 加锁
    async with sem:
        name = 'name-{:d}'.format(i)
        async with db_pool.acquire() as db_conn:
            await db_conn.execute('insert into test(name) values($1);', name)

async def main():
    global db_pool
    db_pool = await asyncpg.create_pool(**db_config)
    ## 先初始化数据库
    await initdb()

    cos = []
    ## cos = [insert_async(i) for i in range(10)]
    for i in range(10000): 
        co = asyncio.create_task(insert_async(i))
        cos.append(co)
    await asyncio.wait(cos)

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
end = time.time()

print('cost %f' % (end - start))
