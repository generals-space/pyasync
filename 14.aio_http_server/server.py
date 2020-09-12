import random

import asyncio
from aiohttp import web

async def aio_api(req):
    ## 随机沉睡 1-30s 再返回
    delay = random.randint(1, 30)
    resp = {
        'delay': delay
    }
    print('delay: %d' % delay)
    ## 别用这个, 同步库的 sleep 不会让出 cpu, 协程服务器就没效果了.
    ## time.sleep(delay)
    await asyncio.sleep(delay)
    return web.json_response(resp)

async def path_param_handler(req):
    ## 从 uri 路径中获取参数
    ## get() 方法的第2个参数貌似为默认值, 不过好像没什么用?
    name = req.match_info.get('name', 'Anonymous')
    text = "Hello, " + name
    return web.Response(text=text)

route_list = [
    web.get('/aio', aio_api),
    web.get('/{name}', path_param_handler)
]

app = web.Application()
app.add_routes(route_list)
web.run_app(app, port = 3000)
