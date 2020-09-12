参考文章

1. [python:利用asyncio进行快速抓取](https://blog.csdn.net/jb19900111/article/details/22692231)

2. [python并发2：使用asyncio处理并发](http://blog.gusibi.com/post/python-asyncio/)

3. [爬取博客详细页面的标题(python3.5以上,async/await,aiohttp)](https://blog.csdn.net/u013055678/article/details/54172693)

4. [python 3.7 Semaphore官方文档](https://docs.python.org/3/library/asyncio-sync.html?highlight=semaphore#semaphore)

## 1. 引言

虽然协程比线程更轻量, 占用资源更少, 但也不能无限制的增加. 如果每个协程任务不只占用IO, 如果协程还消耗了较多了CPU/内存呢? 按照生产者/消费者模型, 生产者不停向队列里添加任务, 消费者不停从队列里取任务并向循环中添加, 如果没有限制, 终究会耗尽服务器资源的.

没错, 就类似线程池, 我们也需要协程池. `asyncio`提供了`semaphore`机制, 来限制同时执行的协程数量.

引用参考文章2中一段话:

> `Semaphore` 对象维护着一个内部计数器, 若在对象上调用 `.acquire()` 协程方法, 计数器则递减; 若在对象上调用 `.release()` 协程方法, 计数器则递增. 计数器的值是在初始化的时候设定.  如果计数器大于0, 那么调用 `.acquire()` 方法不会阻塞, 如果计数器为0, `.acquire()` 方法会阻塞调用这个方法的协程, 直到其他协程在同一个 `Semaphore` 对象上调用 `.release()` 方法, 让计数器递增. 

不过网上大部分示例都没有调用过`acquire()`和`release()`方法, 而是直接把`semaphore`对象当作上下文管理器来用.

参考文章4中展示了semaphore对象的两种不同的使用方式.

```py
sem = asyncio.Semaphore(10)

# ... later
async with sem:
    # work with shared resource
```

和

```py
sem = asyncio.Semaphore(10)

# ... later
await sem.acquire()
try:
    # work with shared resource
finally:
    sem.release()
```

## 2. 实践

在本示例中, `producer`生产者创建了50个任务, 添加到异步队列中, 然后`customer`消费者从队列中取得任务并执行. 创建的过程很快就完成了, 因为本示例只是通过协程池来限制`customer`消费者的行为.

`customer`的行为表现就如同多线程一样, 只能同时执行5个任务, 但是只有等一个任务完成, 才能处理下一个.

在试验过程中, 我曾尝试在`customer`函数的`while`循环中添加`semaphore`锁, 但是无效, 然后注释掉了. 猜测`semaphore`只在事件循环内部才有效, 单纯的`await`一个协程任务是没有用的.

...那什么是事件循环内部?

我们通过`run_coroutine_threadsafe`添加协程任务到事件循环, 通过`wait`等待一堆任务在事件循环中执行完毕...类似这种, 在协程中调用`semaphore`锁才有意义.
