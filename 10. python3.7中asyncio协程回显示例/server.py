#!/usr/bin/python
#!encoding:utf-8

import asyncio

loop = asyncio.get_event_loop()

## 对每一个客户端连接都使用这个函数来处理
## 两个参数是asyncio.StreamReader 对象和 asyncio.StreamWriter 对象
async def echoHandler(reader, writer):
    addr = writer.get_extra_info('peername')
    print('客户端 %s 接入', addr)
    while True:
        ## StreamReader对象有多种read方法, 这里采用最直接的.
        dataInRaw = await reader.read(1024)
        dataIn = dataInRaw.decode().strip()     ## 使用strip()移除首尾空白字符
        ## 得到套接字的远程地址
        print("Received %s from %s" % (dataIn, addr))

        writer.write(dataInRaw)
        ## 刷新writer缓冲区
        await writer.drain()

        if dataIn == 'exit':
            break
    writer.close()
    print('客户端 %s 断开', addr)


async def echoServer():
    ## 创建异步socket服务器, 对每个客户端连接都使用echoHandler处理.
    serverCoro = await asyncio.start_server(echoHandler, host = '0.0.0.0', port = 6379)
    addr = serverCoro.sockets[0].getsockname()
    print('正在监听: ', addr)
    async with serverCoro:
        await serverCoro.serve_forever()

try:
    asyncio.run(echoServer())
except KeyboardInterrupt:
    print('user entered Ctrl + C...')
