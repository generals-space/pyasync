# 关于asyncio.run()的使用注意事项

asyncio.run()与`asyncio.get_event_loop()`不能同时使用...看看示例吧.

正确1:

```py
import asyncio
from aiohttp import ClientSession

url = 'http://note.generals.space/aio'

async def main(loop):
    session = ClientSession(loop = loop)
    resp = await session.get(url)
    await session.close()
    result = await resp.read()
    print(result)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

```

正确2:

```py
import asyncio
from aiohttp import ClientSession

url = 'http://note.generals.space/aio'

async def main():
    loop = asyncio.get_event_loop()
    session = ClientSession(loop = loop)
    resp = await session.get(url)
    await session.close()
    result = await resp.read()
    print(result)

asyncio.run(main())

```

错误3:

```py
import asyncio
from aiohttp import ClientSession

url = 'http://note.generals.space/aio'

async def main(loop):
    session = ClientSession(loop = loop)
    resp = await session.get(url)
    await session.close()
    result = await resp.read()
    print(result)


loop = asyncio.get_event_loop()
asyncio.run(main(loop))

```

报错如下

```
...
RuntimeError: Timeout context manager should be used inside a task
Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x03721810>
```

问题分析

查看`asyncio.run()`源码会发现, ta其中有一句通过`loop = events.new_event_loop()`自行创建loop, 这可能会与我们通过`asyncio.get_event_loop()`得到的loop发生冲突.
