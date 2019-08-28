#!/usr/bin/env python
#!encoding: utf-8

import socket

conn_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_fd.connect(('127.0.0.1', 7777))
print('已连接到服务器...')

msg = conn_fd.recv(1024).decode()
print(msg)

while True:
    data = input('发送: ')
    conn_fd.send(data.encode())
    if data == 'exit':
        conn_fd.close()
        break
    else:
        msg = conn_fd.recv(1024).decode()
        print('收到: ' + msg)
