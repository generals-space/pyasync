#!/usr/bin/env python

import asyncio
import time
from aiohttp import ClientSession

url = 'https://note.generals.space/aio'
task_queue = asyncio.Queue()

## 带参装饰器
def timeout_it(timeout = 10):
    def __timeout_it(func):
        async def warappedFunc(*args, **kwargs):
            try:
                await asyncio.wait_for(func(*args, **kwargs), timeout)
            except asyncio.TimeoutError:
                print('task timeout...')
            else:
                print('task complete...')
        return warappedFunc
    return __timeout_it

@timeout_it(timeout = 20)
async def fetch_url(session, order, url):
    print('fetching...', order)
    res = await session.get(url)
    resText = await res.json()
    print('order %d: %s' % (order, resText))
    return resText

async def customer(loop):
    print('customer start...')
    aioSession = ClientSession(loop = loop)
    while True:
        _order, _url = await task_queue.get()
        asyncio.run_coroutine_threadsafe(fetch_url(aioSession, _order, _url), loop)

    print('customer complete...')

async def producer():
    print('producer start...')
    for i in range(20):
        ## await asyncio.sleep(2)
        await task_queue.put((i, url))

    print('producer complete...')

async def main(loop):
    co = [producer(), customer(loop)]
    await asyncio.wait(co)
    print('主线程结束...')

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

# producer start...
# producer complete...
# customer start...
# fetching... 0
# ...
# fetching... 19
# order 1: {'delay': 3}
# task complete...
# order 0: {'delay': 4}
# task complete...
# order 17: {'delay': 6}
# order 7: {'delay': 6}
# task complete...
# task complete...
# order 19: {'delay': 14}
# order 15: {'delay': 14}
# task complete...
# task complete...
# order 14: {'delay': 15}
# task complete...
# order 10: {'delay': 15}
# order 4: {'delay': 15}
# task complete...
# task complete...
# order 3: {'delay': 18}
# task complete...
# task timeout...
# ...
# task timeout...