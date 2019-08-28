示例03中我们使用了线程+协程的方式完成动态任务的添加, 但是仍然不方便, 线程间变量同步是个大问题.

之后在研究tornado时, 在ta的官方文档中得到了灵感, 就是示例04的代码. 

动态添加任务不一定要开线程, 使用异步队列, 和两个循环可以模拟生产者和消费者模型. 这个示例就是对示例03的改进.

------

`task_queue_timeout.py`还为每个任务添加了超时时间的限制. 因为`run_coroutine_threadsafe()`函数不能设置超时, 所以把`fetch_url`协程用`wait_for()`函数包装了一下, 完美.

`gather(coroutine1, coroutine2...])`: 同时执行多个协程函数, 每个协程算是一个参数;

`wait([coroutine1, coroutine2...], timeout)`: 与`gather`一样, 同时执行多个协程函数, 不过协程函数是以列表形式传入的, 还可以设置超时时间;

`wait_for(coroutine, timeout)`: 执行单个协程函数, 也可以设置超时.
