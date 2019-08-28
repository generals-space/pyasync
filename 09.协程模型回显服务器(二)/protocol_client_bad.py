#!/usr/bin/python
#!encoding:utf-8

import asyncio

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        print('已连接到服务器...')
        while True:
            data = input('发送: ')
            transport.write(data.encode())
            if data == 'exit': break

        print('发送结束, 连接断开...')
        transport.close()

    def data_received(self, dataInRaw):
        data = dataInRaw.decode().strip()
        print('收到: ' + data)

    def connection_lost(self, exc):
        print('服务端断开连接, 终止事件循环...')
        self.loop.stop()

loop = asyncio.get_event_loop()

## 注意create_connection的第一个参数, 其实是一个函数.
clientCoro = loop.create_connection(lambda : EchoClientProtocol(loop), host='127.0.0.1', port=6379)

loop.run_until_complete(clientCoro)
loop.run_forever()
loop.close()


## 运行测试

## 已连接到服务器...
## 发送: get
## 发送: go
## 发送: exit
## 发送结束, 连接断开...
## 服务端断开连接, 终止事件循环...
