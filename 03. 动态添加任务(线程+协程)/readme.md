## 线程 & 协程

参考文章

1. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673627.html)

2. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673646.html)

3. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673682.html)

4. [PYTHON中的协程并发](https://www.cnblogs.com/MY0213/p/8985329.html)
    - 示例讲解的很清楚, 各种应用场景也很全面

示例03写了动态添加协程任务的方法, 线程 + 协程配合使用, 基本思路是启动一个子线程来维护事件循环, 主线程不停创建任务丢到事件循环.

- `asyncio_with_thread_demo.py`: 展示了在子线程中运行协程基本流程, 但是无法正常关闭, 包括aiohttp的ClientSession和asyncio的loop. 
- `asyncio_with_thread_production.py`: 修复了demo的问题, 可以作为参考.
