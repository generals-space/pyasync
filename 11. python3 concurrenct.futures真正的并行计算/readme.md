参考文章

1. [python异步并发模块concurrent.futures简析](http://lovesoo.org/analysis-of-asynchronous-concurrent-python-module-concurrent-futures.html)

2. [python concurrent.futures](https://www.cnblogs.com/kangoroo/p/7628092.html)

3. [python 3.7 官方文档 loop.run_in_executor](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)

1. `python 3.x`中自带了`concurrent.futures`模块.
2. `python 2.7`需要安装`futures`模块, 使用命令`pip install futures`安装即可.

实际上, `concurrent.futures`模块与异步毫无关系, 这只是一种并行操作的高级操作, ta提供的`ProcessPoolExecutor`与`ThreadPoolExecutor`比`multiprocess`与`threading`实现的多进程和多线程简单太多了(不过没那么灵活).

可以看一下这个模块的使用, 因为这个模块对`Future`的应用很...单纯, 没有事件循环协程对象task任务等概念的干扰.

另外, `asyncio`也有`loop.run_in_executor()`函数与`concurrent.futures`的`Executor`结合的使用方法, 可以查看参考文章3. 

在已经了解了`concurrent.futures`的情况下, 官方文档给出的示例就非常简单了. `main.py`就是示例代码. 不过这个代码在windows平台3.7.3版本下, `ProcessPoolExecutor`模型会出问题, 只能在linux下运行.

```
concurrent.futures.process.BrokenProcessPool: A process in the process pool was terminated abruptly while the future was running or pending.
```

另外, `run_in_executor()`貌似只能运行一个函数, 且必须通过`await`阻塞得到结果, 无法执行多个并行任务, 也无法后台执行...起码目前我还没有找到方法.
