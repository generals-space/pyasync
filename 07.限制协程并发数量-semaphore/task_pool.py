#!/usr/bin/env python

import asyncio
import time
from aiohttp import ClientSession

url = 'http://localhost:3000/aio'
task_queue = asyncio.Queue()

## 为了能明显的看出semaphore的效果, 这里设置的小一些.
sem = asyncio.Semaphore(5)

async def fetch_url(session, order, url):
    async with sem:
        print('fetching...', order)
        res = await session.get(url)
        resText = await res.json()
        print('order %d: %s' % (order, resText))
        return resText

async def customer(loop):
    print('customer start...')
    aioSession = ClientSession(loop = loop)
    ## 在这里加semaphore锁是无效的...为啥?
    ## sem = asyncio.Semaphore(5)
    ## while True:
    ##     async with sem:
    ##         _order, _url = await task_queue.get()
    ##         asyncio.run_coroutine_threadsafe(fetch_url(aioSession, _order, _url), loop)
    while True:
        ## _order 任务序号, 用来标识任务的先后顺序
        _order, _url = await task_queue.get()
        asyncio.run_coroutine_threadsafe(fetch_url(aioSession, _order, _url), loop)
    print('customer complete...')

async def producer():
    print('producer start...')
    for i in range(50):
        await task_queue.put((i, url))

    print('producer complete...')

async def main(loop):
    co = [producer(), customer(loop)]
    await asyncio.wait(co)
    print('主线程结束...')

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

# customer start...
# producer start...
# producer complete...
# fetching... 0
# fetching... 1
# fetching... 2
# fetching... 3
# fetching... 4
# order 3: {'delay': 3}
# fetching... 5
# ...
# order 42: {'delay': 19}
# fetching... 49
# order 44: {'delay': 22}
# order 49: {'delay': 11}
# order 48: {'delay': 18}
# order 47: {'delay': 21}
# order 46: {'delay': 27}