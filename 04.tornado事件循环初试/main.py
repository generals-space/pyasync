#!/usr/bin/env python

from tornado import ioloop, queues, httpclient, gen

from datetime import timedelta
import time

url = 'http://localhost:3000/aio'
q = queues.Queue()
loop = None

async def fetch_url(url):
    print('fetching...')
    ## 默认请求超时时间为20s
    resp = await httpclient.AsyncHTTPClient().fetch(url, request_timeout = 30)
    html = resp.body.decode(errors = 'ignore')
    print(html)
    return html

async def customer():
    print('customer start...')
    ## 用协程代替线程做循环
    while True:
        _url = await q.get()
        ## html = await fetch_url(url)
        global loop
        
        ## loop.spawn_callback(fetch_url, url)
        loop.add_callback(fetch_url, url)
    print('customer complete...')

async def producer():
    print('producer start...')
    for _ in range(10):
        print('putting...')
        ## 异步队列, 异步存入
        await gen.sleep(1)
        await q.put(url)
    print('producer complete...')
async def main():
    ## 主协程中添加两个独立子协程
    ## 直接await一个带有循环的协程会阻塞, 这里直接同时启动两个
    ## await customer()
    await gen.multi([customer(), producer()])
    print('等待结束...')

## export PYTHONASYNCIODEBUG=1
if __name__ == '__main__':
    loop = ioloop.IOLoop.current()
    ## 主协程main
    loop.run_sync(main)