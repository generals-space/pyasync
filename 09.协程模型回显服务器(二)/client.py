#!/usr/bin/python
#!encoding:utf-8

import asyncio

async def echoClient():
    reader, writer = await asyncio.open_connection(host = '127.0.0.1', port = 6379)
    print('已连接到服务器...')

    while True:
        data = input('发送: ')
        writer.write(data.encode())
        if data == 'exit':
            writer.close()
            break
        else:
            msgRaw = await reader.read(1024)
            msg = msgRaw.decode().strip()
            print('收到: ' + msg)

loop = asyncio.get_event_loop()
loop.run_until_complete(echoClient())
loop.close()