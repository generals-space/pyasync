## 线程 & 协程

参考文章

1. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673627.html)

2. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673646.html)

3. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673682.html)

示例03写了动态添加协程任务的方法, 线程 + 协程配合使用, 基本思路是启动一个子线程来维护事件循环, 主线程不停创建任务丢到事件循环.

示例

- `asyncio_with_thread_demo.py`: 展示了在子线程中运行协程基本流程, 但是无法正常关闭, 包括aiohttp的ClientSession和asyncio的loop. 
- `asyncio_with_thread_production.py`: 修复了demo的问题. 其中最重要的`loop.call_soon_threadsafe(loop.stop)`是根据参考文章1, 2, 3的python邮件列表.
