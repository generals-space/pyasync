#!/bin/python

import asyncio
import time
from aiohttp import ClientSession

url = 'https://note.generals.space/aio'
start = time.time()

async def main(loop):
    session = ClientSession(loop = loop)
    ## session.get()是异步操作, 但是只有一个任务时, 无法体现其优势
    ## 这里await等待mytask执行结束和直接使用urllib.urlopen()时间上没什么区别...
    mytask = loop.create_task(session.get(url))
    ## completed, pending都是task列表, 不过completed是已完成并且已经设置了result()的task列表.
    completed, pending = await asyncio.wait([mytask], loop = loop, timeout = 10)
    for i in completed:
        result = i.result()
        print('task result type: ', type(result))
        result = await result.read()
        print('result read type: ', type(result))
        print('result content: ', result)
    ## 超时的task被放在pending列表里
    for i in pending:
        print(i)
        ## task的执行状态只有4种, pending, running, done, cancelled
        ## 不过await过的task, 就只有done和cancelled两种.
        ## 这两种都不是, 那应该就是超时了.
        print('done ? ', i.done())          ## False
        print('cancelled ? ', i.cancelled())## False
        print(type(i))
        ## timeout的task是没有设置result()的
        ## print(i.result())
    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

end = time.time()
print('cost %f' % (end - start))
