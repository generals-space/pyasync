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

## 创建异步socket服务器, 对每个客户端连接都使用echoHandler处理.
serverCoro = asyncio.start_server(echoHandler, host = '0.0.0.0', port = 6379)

try:
    server = loop.run_until_complete(serverCoro)
    loop.run_forever()
except KeyboardInterrupt:
    print('user entered Ctrl + C...')
    server.close()
    # server.wait_closed返回一个 future
    # 调用loop.run_until_complete 方法，运行 future
    loop.run_until_complete(server.wait_closed())
    # 终止事件循环
    loop.close() 

## 以下使用create_task() + run_forever(), 也是正确的做法
## try:
##     ## 使用create_task() + run_forever()也可以达到目的.
##     ## 但是create_task(协程)得到的是task对象(拥有pending, running状态的那种)
##     ## 而run_untile_complete(协程)可以启动事件循环并得到futurn的result对象.
##     task = loop.create_task(serverCoro)
##     loop.run_forever()
## except KeyboardInterrupt:
##     print('user entered Ctrl + C...')
##     server = task.result()
##     server.close()
##     # server.wait_closed返回一个 future
##     # 调用loop.run_until_complete 方法，运行 future
##     loop.run_until_complete(server.wait_closed())
##     loop.close()  # 终止事件循环