#!/usr/bin/env python

import asyncio
import time
from aiohttp import ClientSession

url = 'http://localhost:3000/aio'
task_queue = asyncio.Queue()

async def fetch_url(session, order, url):
    print('fetching...', order)
    res = await session.get(url)
    resText = await res.json()
    print('order %d: %s' % (order, resText))
    return resText

async def fetch_url_timeout(session, order, url, loop = None, timeout = 10):
    try:
        await asyncio.wait_for(fetch_url(session, order, url), timeout)
    except asyncio.TimeoutError:
        print(f'task {order} timeout')
    else:
        print(f'task {order} complete')

async def customer(loop):
    print('customer start...')
    aioSession = ClientSession(loop = loop)
    while True:
        _order, _url = await task_queue.get()
        asyncio.run_coroutine_threadsafe(fetch_url_timeout(aioSession, _order, _url, loop = loop, timeout = 10), loop)
        ## asyncio.run_coroutine_threadsafe(fetch_url(aioSession, _order, _url), loop)

    print('customer complete...')

async def producer():
    print('producer start...')
    for i in range(10):
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
# fetching... 9
# order 5: {'delay': 3}
# task 5 complete
# order 7: {'delay': 8}
# order 9: {'delay': 6}
# task 7 complete
# task 9 complete
# task 0 timeout
# ...
# task 8 timeout