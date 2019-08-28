import time
import asyncio

from aiohttp import ClientSession

url = 'http://note.generals.space/aio'

async def request_page(order, session):
    resp = await session.get(url)
    result = await resp.read()
    print('order: {:d}, result: {:s}'.format(order, str(result)))

    ## 这里是cpu密集型操作
    ## print('request {:d} to {:s} success'.format(order, url))
    ## time.sleep(30)
    ## print('request {:d} to {:s} complete'.format(order, url))

async def main():
    loop = asyncio.get_event_loop()
    session = ClientSession(loop = loop)
    coroutines = []
    for i in range(4):
        co = loop.create_task(request_page(i, session))
        coroutines.append(co)

    await asyncio.wait(coroutines)
    await session.close()

start = time.time()

asyncio.run(main())

end = time.time()
print('cost %f' % (end - start))

## 注释掉time.sleep()部分
## order: 0, result: b'{"delay":11}'
## order: 3, result: b'{"delay":14}'
## order: 2, result: b'{"delay":18}'
## order: 1, result: b'{"delay":19}'
## cost 19.040582

## 解开time.sleep()的注意
## order: 2, result: b'{"delay":15}'
## request 2 to http://note.generals.space/aio success
## request 2 to http://note.generals.space/aio complete
## order: 3, result: b'{"delay":17}'
## request 3 to http://note.generals.space/aio success
## request 3 to http://note.generals.space/aio complete
## order: 0, result: b'{"delay":20}'
## request 0 to http://note.generals.space/aio success
## request 0 to http://note.generals.space/aio complete
## order: 1, result: b'{"delay":18}'
## request 1 to http://note.generals.space/aio success
## request 1 to http://note.generals.space/aio complete
## cost 135.050332