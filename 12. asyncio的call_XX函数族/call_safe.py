import time
import asyncio
import threading

from aiohttp import ClientSession

url = 'http://localhost:3000/aio'

def keep_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def callback(order):
    print('request {:d} to {:s} success'.format(order, url))

async def request_page(order, session, loop):
    resp = await session.get(url)
    result = await resp.read()

    print('order: {:d}, result: {:s}'.format(order, str(result)))
    ## 这里两个函数没有区别...???
    ## loop.call_soon_threadsafe(callback, order)
    loop.call_soon(callback, order)

try:
    loop = asyncio.get_event_loop()
    loopThread = threading.Thread(target=keep_loop, args=(loop,))
    loopThread.setDaemon(True)
    loopThread.start()

    session = ClientSession(loop = loop)

    for i in range(5):
        co = request_page(i, session, loop)
        asyncio.run_coroutine_threadsafe(co, loop)

    ## join()时ctrl-c无法结束, 而while True可以.
    ## loopThread.join()
    while True:
        time.sleep(1)

except KeyboardInterrupt as e:
    ## 以下两行可以注释掉, 不会报错
    asyncio.run_coroutine_threadsafe(session.close(), loop)
    time.sleep(1)
    loop.stop()


## 输出
## order: 0, result: b'{"delay":9}'
## request 0 to http://localhost:3000/aio success
## order: 3, result: b'{"delay":12}'
## request 3 to http://localhost:3000/aio success
## order: 2, result: b'{"delay":18}'
## request 2 to http://localhost:3000/aio success
## order: 1, result: b'{"delay":24}'
## request 1 to http://localhost:3000/aio success
## order: 4, result: b'{"delay":28}'
## request 4 to http://localhost:3000/aio success
