import asyncio
import threading
import aiohttp
from datetime import datetime
import time

url = 'https://note.generals.space/aio'

start = time.time()

def keep_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def waitTask(session, order):
    res = await session.get(url)
    ## resText = await res.text()
    resText = await res.json()
    print('order %d: %s' % (order, resText))
    return resText

async def closeSession(session):
    return await session.close()

def callback(future):
    print('calling callback...')
    print(future.result())

def main():
    loop = asyncio.get_event_loop()
    loopThread = threading.Thread(target = keep_loop, args = (loop, ))
    loopThread.setDaemon(True)

    loopThread.start()
    aioSession = aiohttp.ClientSession(loop = loop)

    for i in range(0, 10):
        coroutine = waitTask(aioSession, i)
        _concurrentFuture = asyncio.run_coroutine_threadsafe(coroutine, loop)
        ## 添加协程回调函数的方式
        _concurrentFuture.add_done_callback(callback)
    ## join()方法等待目标线程结束, 没有返回值, 只会阻塞
    ## 在timeout时间内如果线程没有结束, join()方法仍然会结束阻塞, 让主线程继续执行(子线程依然会存在)
    loopThread.join(timeout = 40)

    ## 协程执行完毕后关闭aiohttp.ClientSession, 注意方式, 要用协程完成.
    closeCoroutine = closeSession(aioSession)
    asyncio.run_coroutine_threadsafe(closeCoroutine, loop)
    time.sleep(0.5) ## 这里不知道有没有必要
    
    ## 注意stop与close的调用方式
    print(loop)
    loop.call_soon_threadsafe(loop.stop)
    ## 这里可能有必要, 在协程并没有完全执行完成时关闭事件循环, 会需要一点时间
    time.sleep(5)
    print(loop)
    loop.close()
    print(loop)

if __name__ == '__main__':
    main()


## order 6: {'delay': 1}
## order 8: {'delay': 2}
## order 5: {'delay': 3}
## order 9: {'delay': 3}
## order 3: {'delay': 5}
## order 7: {'delay': 7}
## order 2: {'delay': 15}
## order 4: {'delay': 19}
## order 0: {'delay': 27}
## order 1: {'delay': 28}
## <_WindowsSelectorEventLoop running=True closed=False debug=False>
## <_WindowsSelectorEventLoop running=True closed=False debug=False>
## <_WindowsSelectorEventLoop running=False closed=True debug=False>