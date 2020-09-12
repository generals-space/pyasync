import time
import asyncio
import threading

from aiohttp import ClientSession

url = 'http://localhost:3000/aio'

def keep_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def _request_page(order, session, loop):
    resp = await session.get(url)
    result = await resp.read()
    print('order: {:d}, result: {:s}'.format(order, str(result)))

def request_page(order, session, loop):
    co = _request_page(order, session, loop)
    asyncio.run_coroutine_threadsafe(co, loop)

try:
    loop = asyncio.get_event_loop()
    loopThread = threading.Thread(target=keep_loop, args=(loop,))
    loopThread.setDaemon(True)
    loopThread.start()

    session = ClientSession(loop = loop)

    for i in range(5):
        loop.call_soon_threadsafe(request_page, i, session, loop)
        ## loop.call_soon()会卡住
        ## loop.call_soon(request_page, i, session, loop)

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
## order: 3, result: b'{"delay":1}'
## order: 1, result: b'{"delay":9}'
## order: 0, result: b'{"delay":13}'
## order: 4, result: b'{"delay":22}'
## order: 2, result: b'{"delay":30}'
