#!/usr/bin/env python

import asyncpool
import logging
import asyncio
import sys

async def worker(initial_number, result_queue):
    print("Processing Value! -> {} * 2 = {}".format(initial_number, initial_number * 2))
    await asyncio.sleep(1)
    await result_queue.put(initial_number * 2)

async def result_reader(queue):
    while True:
        value = await queue.get()
        if value is None:
            break
        print("Got value! -> {}".format(value))

async def run():
    result_queue = asyncio.Queue()

    reader_future = asyncio.ensure_future(result_reader(result_queue), loop=loop)

    # Start a worker pool with 10 coroutines, invokes `worker` and waits for it to complete or 5 minutes to pass.
    ## 启动一个可以运行10个协程的协程池
    async with asyncpool.AsyncPool(loop, num_workers=10, 
                             logger_name=logger_name,
                             worker_co=worker, max_task_time=300,
                             log_every_n=10) as pool:
        for i in range(50):
            ## 这里push的是工作协程worker的参数, 
            ## 在协程池中, 每个工作协程从队列里获取参数, 
            ## 传给worker_co, 即worker函数去执行.
            ## result_queue是结果队列, 工作协程执行完毕后会把结果放进去.
            await pool.push(i, result_queue)

    await result_queue.put(None)
    await reader_future
logger_name = 'mypool'
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logger = logging.Logger(logger_name)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

loop = asyncio.get_event_loop()
loop.run_until_complete(run())