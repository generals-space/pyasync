#!/usr/bin/env python

import asyncio
import time
from aiohttp import ClientSession

url = 'https://note.generals.space/aio'
task_queue = asyncio.Queue()

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
    for i in range(10):
        await asyncio.sleep(2)
        await task_queue.put((i, url))

    print('producer complete...')

async def main(loop):
    co = [producer(), customer(loop)]
    await asyncio.wait(co)
    print('主线程结束...')

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

## customer start...
## producer start...
## fetching... 0
## fetching... 1
## fetching... 2
## order 1: {'delay': 2}
## fetching... 3
## fetching... 4
## fetching... 5
## fetching... 6
## fetching... 7
## order 2: {'delay': 10}
## fetching... 8
## producer complete...
## fetching... 9
## order 0: {'delay': 18}
## order 8: {'delay': 5}
## order 9: {'delay': 3}
## order 6: {'delay': 16}
## order 5: {'delay': 20}
## order 4: {'delay': 24}
## order 3: {'delay': 27}
## order 7: {'delay': 23}