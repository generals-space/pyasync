#!/bin/python

import asyncio
import time
from aiohttp import ClientSession

url = 'https://note.generals.space/aio'
start = time.time()

async def main(loop):
    session = ClientSession(loop = loop)
    coroutines = [loop.create_task(session.get(url)) for i in range(10)]
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
## b'{"delay":29}'
## b'{"delay":29}'
## b'{"delay":2}'
## b'{"delay":15}'
## b'{"delay":22}'
## b'{"delay":10}'
## b'{"delay":8}'
## b'{"delay":22}'
## b'{"delay":1}'
## b'{"delay":7}'
## cost 30.105002