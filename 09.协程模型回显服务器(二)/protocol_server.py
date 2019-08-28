#!/usr/bin/python
#!encoding:utf-8

import asyncio

loop = asyncio.get_event_loop()

## 可以看作是客户端连接的处理逻辑的工厂类.
## 类似于nodejs中server的on事件绑定回调.
class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.addr = transport.get_extra_info('peername')
        self.transport = transport
        print('客户端 %s 接入', self.addr)

    def data_received(self, dataInRaw):
        dataIn = dataInRaw.decode().strip()
        print("Received %s from %s" % (dataIn, self.addr))

        self.transport.write(dataInRaw)
        if dataIn == 'exit':
            self.transport.close()
            print('客户端 %s 断开', self.addr)

serverCoro = loop.create_server(EchoServerProtocol, host = '0.0.0.0', port = 6379)

try:
    server = loop.run_until_complete(serverCoro)
    loop.run_forever()
except KeyboardInterrupt:
    print('user entered Ctrl + C...')
    server.close()
    # server.wait_closed返回一个 future
    # 调用loop.run_until_complete 方法，运行 future
    loop.run_until_complete(server.wait_closed())
    loop.close()  # 终止事件循环
