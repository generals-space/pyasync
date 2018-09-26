#!/usr/bin/env python

import asyncpool
import logging
import asyncio
from aiohttp import ClientSession

async def fetch_url(order, url, result_queue):
    session = ClientSession(loop=loop)
    print('fetching...', order)
    res = await session.get(url)
    resText = await res.json()
    await result_queue.put(resText)

async def result_reader(queue):
    while True:
        value = await queue.get()
        if value is None:
            break
        print("Got value! -> {}".format(value))

async def run():
    result_queue = asyncio.Queue()
    reader_future = asyncio.ensure_future(result_reader(result_queue), loop=loop)

    ## 启动一个可以运行10个协程的协程池
    pool = asyncpool.AsyncPool(loop, num_workers=10, worker_co=worker, max_task_time=300)
    pool.start()

    for i in range(50):
        ## 这里push的是工作协程worker的参数, 
        ## 在协程池中, 每个工作协程从队列里获取参数, 
        ## 传给worker_co, 即worker函数去执行.
        ## result_queue是结果队列, 工作协程执行完毕后会把结果放进去.
        await pool.push(i, result_queue)

    await pool.join()
    await result_queue.put(None)
    await reader_future

loop = asyncio.get_event_loop()
loop.run_until_complete(run())