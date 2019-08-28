import time
import asyncio

from aiohttp import ClientSession

url = 'https://note.generals.space/aio'

def callback(loop, order):
    print('loop time: {:f}, request {:d} to {:s} success'.format(loop.time(), order, url))

async def request_page(loop, order, session):
    resp = await session.get(url)
    result = await resp.read()

    loop_time = loop.time()
    print('loop time: {:f}, order: {:d}, result: {:s}'.format(loop_time, order, str(result)))
    ## 指定时间后调用目标函数.
    ## loop.call_at(loop_time + 5, callback, loop, order)
    ## loop.call_later(5, callback, loop, order)
    ## loop.call_soon(callback, loop, order)
    loop.call_soon_threadsafe(callback, loop, order)

async def main(loop):
    session = ClientSession()
    coroutines = []
    for i in range(5):
        co = asyncio.create_task(request_page(loop, i, session))
        coroutines.append(co)

    await asyncio.wait(coroutines)
    await session.close()

start = time.time()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.stop()

end = time.time()
print('cost %f' % (end - start))


## 输出
## loop time: 371982.687000, order: 4, result: b'{"delay":4}'
## loop time: 371982.687000, request 4 to https://note.generals.space/aio success
## loop time: 371983.687000, order: 1, result: b'{"delay":5}'
## loop time: 371983.687000, request 1 to https://note.generals.space/aio success
## loop time: 371985.687000, order: 2, result: b'{"delay":7}'
## loop time: 371985.687000, request 2 to https://note.generals.space/aio success
## loop time: 371991.687000, order: 3, result: b'{"delay":13}'
## loop time: 371991.687000, request 3 to https://note.generals.space/aio success
## loop time: 371996.687000, order: 0, result: b'{"delay":18}'
## loop time: 371996.687000, request 0 to https://note.generals.space/aio success
## cost 18.041001
