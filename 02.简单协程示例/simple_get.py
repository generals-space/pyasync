#!/bin/python

import asyncio
import time
from aiohttp import ClientSession

url = 'http://localhost:3000/aio'
start = time.time()

async def main(loop):
    session = ClientSession(loop = loop)
    ## session.get()是异步操作, 但是只有一个任务时, 无法体现其优势
    ## 这里await等待mytask执行结束和直接使用urllib.urlopen()时间上没什么区别...
    ## mytask = loop.create_task(session.get(url))
    ## await mytask
    ## result = mytask.result()
    result = await session.get(url)
    print('task result type: ', type(result))
    result = await result.read()
    print('result read type: ', type(result))
    print('result content: ', result)
    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

end = time.time()
print('cost %f' % (end - start))
