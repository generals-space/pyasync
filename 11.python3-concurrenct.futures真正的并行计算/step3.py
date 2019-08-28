import time
import asyncio
import functools
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from aiohttp import ClientSession

## executor = ThreadPoolExecutor(max_workers = 4)
executor = ProcessPoolExecutor(max_workers = 4)

url = 'http://note.generals.space/aio'

def blocking_cpu(order, url):
    ## 这里是cpu密集型操作
    print('request {:d} to {:s} success'.format(order, url))
    time.sleep(30)
    print('request {:d} to {:s} complete'.format(order, url))

async def request_page(loop, order, session):
    resp = await session.get(url)
    result = await resp.read()
    print('order: {:d}, result: {:s}'.format(order, str(result)))

    await loop.run_in_executor(executor, functools.partial(blocking_cpu, order, url))

async def main():
    loop = asyncio.get_event_loop()
    session = ClientSession(loop = loop)
    coroutines = []
    for i in range(4):
        co = loop.create_task(request_page(loop, i, session))
        coroutines.append(co)

    await asyncio.wait(coroutines)
    await session.close()

start = time.time()

asyncio.run(main())

end = time.time()
print('cost %f' % (end - start))

## 输出
## order: 1, result: b'{"delay":3}'
## request 1 to http://note.generals.space/aio success
## order: 3, result: b'{"delay":5}'
## request 3 to http://note.generals.space/aio success
## order: 0, result: b'{"delay":13}'
## request 0 to http://note.generals.space/aio success
## order: 2, result: b'{"delay":25}'
## request 2 to http://note.generals.space/aio success
## request 1 to http://note.generals.space/aio complete
## request 3 to http://note.generals.space/aio complete
## request 0 to http://note.generals.space/aio complete
## request 2 to http://note.generals.space/aio complete
## cost 55.053128
