#!/bin/python

import asyncio
import time
from aiohttp import ClientSession
import functools

url = 'https://note.generals.space/aio'
start = time.time()

## 需要接收task，如果要接收其他的参数就需要用到partial(偏函数),参数需要放到前面
def callback(order, url, future):
    print('request {:d} to {:s} success'.format(order, url))

async def main(loop):
    session = ClientSession(loop = loop)
    ## 可以设置回调函数
    coroutines = []
    for i in range(10):
        co = loop.create_task(session.get(url))
        co.add_done_callback(functools.partial(callback, i, url))
        coroutines.append(co)
    ## coroutines = [loop.create_task(session.get(url)) for i in range(10)]
    completed, pending = await asyncio.wait(coroutines)
    for c in completed:
        result = await c.result().read()
        print(result)
    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

end = time.time()
print('cost %f' % (end - start))

## 输出
## request 1 to https://note.generals.space/aio success
## request 2 to https://note.generals.space/aio success
## request 4 to https://note.generals.space/aio success
## request 5 to https://note.generals.space/aio success
## request 0 to https://note.generals.space/aio success
## request 3 to https://note.generals.space/aio success
## request 9 to https://note.generals.space/aio success
## request 6 to https://note.generals.space/aio success
## request 7 to https://note.generals.space/aio success
## request 8 to https://note.generals.space/aio success
## b'{"delay":24}'
## b'{"delay":12}'
## b'{"delay":28}'
## b'{"delay":23}'
## b'{"delay":17}'
## b'{"delay":26}'
## b'{"delay":29}'
## b'{"delay":16}'
## b'{"delay":17}'
## b'{"delay":21}'
## cost 29.044463