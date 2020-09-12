参考文章

5. [python 中的 asyncio 使用详解与异步协程的处理流程分析](https://testerhome.com/articles/19703)
    - 示例清晰, 代码很全
    - wait和gather有哪些区别: 
        - `gather`是需要所有任务都执行结束, 如果某一个协程函数崩溃了, 则会抛异常, 都不会有结果。
        - `wait`可以定义函数返回的时机(`return_when`参数), 可以是`FIRST_COMPLETED`(第一个结束的), `FIRST_EXCEPTION`(第一个出现异常的), `ALL_COMPLETED`(全部执行完, 默认的)
    - `run_in_executor()`的使用示例
    - `asyncio.run_coroutine_threadsafe()`返回的是`concurrent.futures._base.Future`对象, 不能使用`await`, 但是可以添加回调`add_done_callback()`


## `loop.run_xxx()`家族: 事件主循环

1. `loop.run_forever(coroutine)`
2. `loop.run_until_complete(coroutine)`
3. `loop.run_in_executor(executor, func)`: 类似于`run_until_complete`, 不过执行的方法为普通函数, 而不是协程对象. 需要`await`阻塞执行.
4. `asyncio.run(coroutine)`: 类似于`loop.run_until_complete()`, 但是不能混用.

## 创建异步任务

1. `loop.create_task(coroutine)`
2. `asyncio.create_task(coroutine)`: 其实是调用了`loop.create_task()`
3. `asyncio.ensure_future()`
创建异步任务到事件循环中(但并不执行, 需要使用`wait`方法), 参数`coroutine`为async函数执行后得到的协程对象.

## wait&gather等待执行

`asyncio.gather(coroutine1, coroutine2...)`: 同时执行多个协程函数, 每个协程算是一个参数;
`asyncio.wait([coroutine1, coroutine2...], timeout)`: 与`gather`一样, 同时执行多个协程函数, 不过协程函数是以列表形式传入的, 还可以设置超时时间;
`asyncio.wait_for(coroutine, timeout)`: 执行单个协程函数, 也可以设置超时.

## 

6. `loop.call_soon_threadsafe(coroutine, loop)`
5. `asyncio.run_coroutine_threadsafe(coroutine, loop)`: 跨线程执行协程, 调用了`loop.call_soon_threadsafe()`

## add_done_callback()

使用`async`声明的`coroutine`对象并不能直接执行, 也不能添加回调函数什么的, 需要事先将其包装成`task`对象.

```py
    co = fetch_url(aioSession, _order, _url)
    task = asyncio.ensure_future(co)
    task.add_done_callback(callback)
```
