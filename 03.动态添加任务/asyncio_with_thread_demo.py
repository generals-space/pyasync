import asyncio
import threading
import aiohttp
from datetime import datetime
import time

url = 'http://localhost:3000/aio'

start = time.time()

def keep_loop(loop):
    loop.run_forever()

async def request_page(session, order):
    res = await session.get(url)
    ## resText = await res.text()
    resText = await res.json()
    print('order %d: %s' % (order, resText))
    return resText

def main():
    loop = asyncio.get_event_loop()
    loopThread = threading.Thread(target = keep_loop, args = (loop, ))
    loopThread.setDaemon(True)

    loopThread.start()
    aioSession = aiohttp.ClientSession(loop = loop)

    for i in range(0, 10):
        coroutine = request_page(aioSession, i)
        _concurrentFuture = asyncio.run_coroutine_threadsafe(coroutine, loop)
    
    loopThread.join(timeout = 40)
    aioSession.close()  ## RuntimeWarning: coroutine 'ClientSession.close' was never awaited
    loop.stop()         ## RuntimeError: Cannot close a running event loop
    loop.close()

if __name__ == '__main__':
    main()


## order 0: {'delay': 2}
## order 2: {'delay': 3}
## order 3: {'delay': 7}
## order 1: {'delay': 7}
## order 7: {'delay': 9}
## order 5: {'delay': 10}
## order 9: {'delay': 14}
## order 6: {'delay': 14}
## order 4: {'delay': 16}
## order 8: {'delay': 29}