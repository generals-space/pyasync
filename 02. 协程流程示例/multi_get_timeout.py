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
    coroutines = [loop.create_task(session.get(url)) for i in range(10)]
    ## completed, pending都是task列表, 不过completed是已完成并且已经设置了result()的task列表.
    completed, pending = await asyncio.wait(coroutines, loop = loop, timeout = 10)
    for i in completed:
        result = i.result()
        print('task result type: ', type(result))
        result = await result.read()
        print('result read type: ', type(result))
        print('result content: ', result)
    ## 超时的task被放在pending列表里
    for i in pending:
        print('timeout...')
        print(i)
        print(type(i))
        ## timeout的task是没有设置result()的
        ## print(i.result())
    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

end = time.time()
print('cost %f' % (end - start))

## 输出
## task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
## result read type:  <class 'bytes'>
## result content:  b'{"delay":5}'
## cost 6.382042