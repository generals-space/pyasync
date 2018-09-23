参考文章

1. [python:利用asyncio进行快速抓取](https://blog.csdn.net/jb19900111/article/details/22692231)

2. [python并发2：使用asyncio处理并发](http://blog.gusibi.com/post/python-asyncio/)

3. [爬取博客详细页面的标题(python3.5以上,async/await,aiohttp)](https://blog.csdn.net/u013055678/article/details/54172693)

虽然协程比线程更轻量, 占用资源更少, 但也不能无限制的增加. 如果每个协程任务不只占用IO, 如果协程还消耗了较多了CPU/内存呢? 按照生产者/消费者模型, 生产者不停向队列里添加任务, 消费者不停从队列里取任务并向循环中添加, 如果没有限制, 终究会耗尽服务器资源的.

没错, 就类似线程池, 我们也需要协程池. `asyncio`提供了`semaphore`机制, 来限制同时执行的协程数量.

引用参考文章2中一段话:

> `Semaphore` 对象维护着一个内部计数器, 若在对象上调用 `.acquire()` 协程方法, 计数器则递减; 若在对象上调用 `.release()` 协程方法, 计数器则递增. 计数器的值是在初始化的时候设定.  如果计数器大于0, 那么调用 `.acquire()` 方法不会阻塞, 如果计数器为0, `.acquire()` 方法会阻塞调用这个方法的协程, 直到其他协程在同一个 `Semaphore` 对象上调用 `.release()` 方法, 让计数器递增. 

不过网上大部分示例都没有调用过`acquire()`和`release()`方法, 而是直接把`semaphore`对象当作上下文管理器来用.

```py
#asyncio.Semaphore(),限制同时运行协程数量
sem = asyncio.Semaphore(5)
with (await sem):
    result = await co_func()
```