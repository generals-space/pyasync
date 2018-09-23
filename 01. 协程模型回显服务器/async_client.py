#!/usr/bin/env python
#!encoding: utf-8

import socket
import asyncio

loop = asyncio.get_event_loop()

async def echo_client():
    conn_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_fd.setblocking(0)
    await loop.sock_connect(conn_fd, ('127.0.0.1', 7777))
    print('已连接到服务器...')

    msg = await loop.sock_recv(conn_fd, 1024)
    msg = msg.decode()
    print(msg)

    while True:
        data = input('发送: ')
        await loop.sock_sendall(conn_fd, data.encode())
        if data == 'exit':
            conn_fd.close()
            break
        else:
            msg = await loop.sock_recv(conn_fd, 1024)
            msg = msg.decode()
            print('收到: ' + msg)

loop.create_task(echo_client())
loop.run_forever()