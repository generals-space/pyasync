import time
import pathlib
import asyncio

import aiofiles

sem = asyncio.Semaphore(100)

async def writefile_async(i):
    ## 加锁
    async with sem:
        filepath = 'data/{:d}'.format(i)
        filecontent = 'hello world for the {:d} times'.format(i)
        async with aiofiles.open(filepath, mode='w') as file:
            await file.write(filecontent)

## 创建存储目录
p = pathlib.Path('data')
if not p.exists(): p.mkdir()

start = time.time()

async def main():
    cos = []
    ## cos = [writefile_async(i) for i in range(10)]
    for i in range(10000): 
        co = asyncio.create_task(writefile_async(i))
        cos.append(co)
    await asyncio.wait(cos)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

end = time.time()

print('cost %f' % (end - start))
