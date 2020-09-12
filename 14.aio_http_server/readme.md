参考文章

1. [aio server 官方文档](https://docs.aiohttp.org/en/stable/web.html)
2. [aiohttp 一个用于asyncio和Python的异步HTTP客户端/服务器](https://github.com/aio-libs/aiohttp-demos)
    - 这个示例提供了一个使用`aiohttp`实现的 websocket 接口, 先记下来, 以后可能用的上.

本示例使用`aiohttp`库实现了一个简单的 web 服务器, 为其他示例提供接口(以前是用 nodejs 写了一个脚本运行在服务器上的, 不过现在服务器没了, 在本地运行一个也一样).

对于一个`/aio`请求, 它会随机沉睡`1-30`秒再返回, 返回的内容是一个json字符串, 结构为`{delay: 沉睡的秒数}`, 示例中用这个接口来学习协程的使用方法.

```
$ python3 server.py
======== Running on http://0.0.0.0:3000 ========
(Press CTRL+C to quit)
delay: 6
```
