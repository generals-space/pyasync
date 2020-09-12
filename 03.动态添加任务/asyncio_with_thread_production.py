import time
import threading
import asyncio
import aiohttp

url = 'http://localhost:3000/aio'

def keep_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def request_page(session, order):
    res = await session.get(url)
    ## resText = await res.text()
    resText = await res.json()
    print('order %d: %s' % (order, resText))
    return resText

try:
    loop = asyncio.get_event_loop()
    loopThread = threading.Thread(target = keep_loop, args = (loop, ))
    ## 子线程随主线程退出而退出
    loopThread.setDaemon(True)
    loopThread.start()

    aioSession = aiohttp.ClientSession(loop = loop)

    for i in range(0, 5):
        co = request_page(aioSession, i)
        ## future对象可以添加回调函数
        future = asyncio.run_coroutine_threadsafe(co, loop)

    ## 不再使用join(timeout=timeout)方法, 毕竟实际场景中timeout的时间无法控制. 
    ## 另外, 直接使用join()无法接受到ctrl-c信号, 这里使用while循环替代
    while True: time.sleep(1)

except KeyboardInterrupt as err:
    print('stoping...')
    ## 这里要将事件循环中的任务全部手动停止, 否则在loop.close()时会出现
    ## Task was destroyed but it is pending!
    for task in asyncio.Task.all_tasks():
        task.cancel()
    ## aioSession.close()是awaitable的协程对象
    asyncio.run_coroutine_threadsafe(aioSession.close(), loop)
    ## 事件循环的stop与close方法都是普通函数.
    loop.stop()
    ## 貌似不需要close(), 如果要调用close(), 需要在stop()后留出一点时间, 
    ## 否则会报RuntimeError: Cannot close a running event loop
    ## time.sleep(1)
    ## loop.close()


## 输出
## order 4: {'delay': 8}
## order 2: {'delay': 16}
## order 1: {'delay': 18}
## stoping...