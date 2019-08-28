#!/usr/bin/python
#!encoding:utf-8

import asyncio
import sys

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop, q):
        self.loop = loop
        self.queue = q
        ## 协程锁, 在建立好与服务端的连接后解除.
        self._ready = asyncio.Event()
        self.sendingTask = asyncio.ensure_future(self.sendMsg())

    async def sendMsg(self):
        await self._ready.wait()
        print('准备发送消息')
        while True:
            data = await self.queue.get()
            self.transport.write(data.encode())
            if data == 'exit': break
        self.transport.close()

    def connection_made(self, transport):
        print('已连接到服务器...')
        self.transport = transport
        ## 解开协程锁
        self._ready.set()

    def data_received(self, dataInRaw):
        data = dataInRaw.decode().strip()
        print('收到: ' + data)

    def connection_lost(self, exc):
        print('服务端断开连接, 终止事件循环...')
        self.sendingTask.cancel()
        self.loop.stop()

q = asyncio.Queue()
loop = asyncio.get_event_loop()

## 异步读取标准输入, 将输入值添加到队列中
def got_stdin_data(q):
    asyncio.ensure_future(q.put(sys.stdin.readline()))

loop.add_reader(sys.stdin, got_stdin_data, q)

## 注意create_connection的第一个参数, 其实是一个函数.
clientCoro = loop.create_connection(lambda : EchoClientProtocol(loop, q), host='127.0.0.1', port=6379)

loop.run_until_complete(clientCoro)
loop.run_forever()
loop.close()