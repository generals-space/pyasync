python是同步语言, 许多原生方法也是按同步方式写的. 异步协程库比如`twisted`, `tornado`框架, 3.5+的`asyncio`库, 都提供了各自的异步方法.

需要说明的是, 异步操作中`yield`, `await`可以在耗时IO操作中交出CPU使用权, 但是无法与原生同步IO操作结合使用. 

比如, `await urllib.urlopen(url)`是无法异步进行的, 它将仍然是阻塞的同步方法.

要想`await`一个异步的http请求, 或是异步的文件读写操作, 都必须使用异步框架/库提供的异步函数, 否则是没用的.

想想, 网上大部分教程都拿`await asyncio.sleep(n)`来模拟耗时IO操作, 这是因为`asyncio.sleep(n)`是异步方法, 对于当前协程当会交出CPU, n秒之后会切换回来继续, 但在同一个线程里的其他协程能够开始执行, 不会造成资源浪费. 如果使用`await time.sleep(n)`呢? 原生`sleep`是一个同步方法, 无法实现CPU切换.

本章`02. 协程流程示例`中, 使用了一个`http://note.generals.space/aio`接口, 对于一个请求, 它会随机沉睡`1-30`秒再返回, 返回的内容是一个json字符串, 结构为`{delay: 沉睡的秒数}`, 示例中用这个接口来学习协程的使用方法.

正如我上面所说, `await urllib.urlopen(url)`没有任何意义, 所以这些示例都将使用`aiohttp`库提供的异步函数.

## 线程 & 协程

参考文章

1. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673627.html)

2. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673646.html)

3. [asyncio - how to stop loop?](https://mail.python.org/pipermail/python-list/2014-June/673682.html)

相关示例

- asyncio_with_thread_demo.py

- asyncio_with_thread_production.py

`demo`展示了在子线程中运行协程基本流程, 但是无法正常关闭, 包括aiohttp的ClientSession和asyncio的loop. `production`修复了这个问题. 其中最重要的`loop.call_soon_threadsafe(loop.stop)`是根据参考文章1, 2, 3的python邮件列表.
