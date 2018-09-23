#!/usr/bin/env python
#!encoding: utf-8
## python版本3.5+才有await, async

import socket
import asyncio

loop = asyncio.get_event_loop()

async def reader(conn_fd):
    while True:
        try:
            data = conn_fd.recv(1024).decode()
            return data
        except BlockingIOError as e:
            ## print(e)
            continue

async def writer(conn_fd, data):
    conn_fd.send(data.encode())

async def handler(conn_fd):
    ## await writer(conn_fd, str.encode('欢迎!'))
    conn_fd.send('欢迎!'.encode())
    ## 循环接受客户端发送的消息
    while True:
        data = await reader(conn_fd)
        print(data)

        if data == 'exit':
            print('客户端 %s:%d 断开连接...' % (conn_fd.getpeername()[0], conn_fd.getpeername()[1]))
            conn_fd.close()
            break
        else:
            await writer(conn_fd, 'Hello, ' + data)

async def echo_server():
    listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_fd.setblocking(0)
    listen_fd.bind(('0.0.0.0', 7777))
    listen_fd.listen(5)
    print('开始监听...')

    while True:
        ## accept是一个阻塞方法, 如果没有客户端连接进入就停在这里
        ## addr是一个元组, 格式为 ('客户端IP', 客户端端口)
        conn_fd, addr = await loop.sock_accept(listen_fd)
        print('收到来自 %s:%d 的连接' % (conn_fd.getpeername()[0], conn_fd.getpeername()[1]))
        loop.create_task(handler(conn_fd))

loop.create_task(echo_server())
loop.run_forever()
