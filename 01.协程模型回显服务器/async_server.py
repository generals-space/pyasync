#!/usr/bin/env python
#!encoding: utf-8
## python版本3.5+才有await, async

import socket
import asyncio

loop = asyncio.get_event_loop()

async def handler(conn_fd):
    with conn_fd:
        await loop.sock_sendall(conn_fd, str.encode('欢迎!'))
        ## 循环接受客户端发送的消息
        while True:
            data = await loop.sock_recv(conn_fd, 1024)
            data = data.decode()
            print(data)

            if data == 'exit':
                print('客户端 %s:%d 断开连接...' % (conn_fd.getpeername()[0], conn_fd.getpeername()[1]))
                conn_fd.close()
                break
            else:
                await loop.sock_sendall(conn_fd, 'Hello, '.encode() + data)

async def echo_server():
    listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_fd.setblocking(0)
    listen_fd.bind(('0.0.0.0', 7777))
    listen_fd.listen(2)
    print('开始监听...')

    while True:
        ## accept是一个阻塞方法, 如果没有客户端连接进入就停在这里
        ## addr是一个元组, 格式为 ('客户端IP', 客户端端口)
        conn_fd, addr = await loop.sock_accept(listen_fd)
        print('收到来自 %s:%d 的连接' % (conn_fd.getpeername()[0], conn_fd.getpeername()[1]))
        coroutine = handler(conn_fd)
        loop.create_task(coroutine)

loop.create_task(echo_server())
loop.run_forever()