#!/bin/python

import asyncio
import time
from aiohttp import ClientSession
import functools

url = 'https://note.generals.space/aio'
start = time.time()

## 需要接收task，如果要接收其他的参数就需要用到partial(偏函数),参数需要放到前面
def callback(order, url, future):
    print('request {:d} to {:s} success'.format(order, url))

async def main(loop):
    session = ClientSession(loop = loop)
    ## session.get()是异步操作, 但是只有一个任务时, 无法体现其优势
    ## 这里await等待mytask执行结束和直接使用urllib.urlopen()时间上没什么区别...
    ## 可以设置回调函数
    coroutines = []
    for i in range(5):
        co = loop.create_task(session.get(url))
        co.add_done_callback(functools.partial(callback, i, url))
        coroutines.append(co)
    ## coroutines = [loop.create_task(session.get(url)) for i in range(5)]
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
## request 1 to https://note.generals.space/aio success
## request 4 to https://note.generals.space/aio success
## request 2 to https://note.generals.space/aio success
## task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
## result read type:  <class 'bytes'>
## result content:  b'{"delay":9}'
## task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
## result read type:  <class 'bytes'>
## result content:  b'{"delay":8}'
## task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
## result read type:  <class 'bytes'>
## result content:  b'{"delay":3}'
## timeout...
## <Task pending coro=<<_RequestContextManager without __name__>()> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x038F1390>()]> cb=[callback(3, 'https://note.generals.space/aio')() at .\multi_get_timeout.py:13]>
## <class '_asyncio.Task'>
## timeout...
## <Task pending coro=<<_RequestContextManager without __name__>()> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x038DF810>()]> cb=[callback(0, 'https://note.generals.space/aio')() at .\multi_get_timeout.py:13]>
## <class '_asyncio.Task'>
## cost 10.005833