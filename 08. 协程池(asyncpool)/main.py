#!/usr/bin/env python

import asyncpool
import logging
import asyncio
from aiohttp import ClientSession

url = 'https://note.generals.space/aio'

async def fetch_url(order, url, result_queue):
    session = ClientSession(loop=loop)
    print('fetching...', order)
    res = await session.get(url)
    resText = await res.json()
    await session.close()
    await result_queue.put(resText)

async def result_reader(result_queue):
    print('start read...')
    while True:
        value = await result_queue.get()
        if value is None:
            break
        print("Got value! -> {}".format(value))

async def run():
    result_queue = asyncio.Queue()
    ## ensure_future()其实也是把一个协程任务丢到事件循环中, 且不阻塞.
    ## 有点像run_coroutine_threadsafe()
    asyncio.ensure_future(result_reader(result_queue), loop=loop)

    ## 启动一个可以运行10个协程的协程池
    pool = asyncpool.AsyncPool(loop, num_workers=10, worker_co=fetch_url, max_task_time=300)
    pool.start()

    for i in range(15):
        ## 这里push的是工作协程worker的参数, 
        ## 在协程池中, 每个工作协程从队列里获取参数, 
        ## 传给worker_co, 即worker函数去执行.
        ## result_queue是结果队列, 工作协程执行完毕后会把结果放进去.
        await pool.push(i, url, result_queue)

    await pool.join()
    await result_queue.put(None)
    print('put complete...')

loop = asyncio.get_event_loop()
loop.run_until_complete(run())