# pyasync

## python异步与协程入门

首先要明确如下认知:

1. 同步语言的异步库与原生标准库不兼容. 以python为例, 原生标准库的`time.sleep(5)`将占用 CPU 5秒钟, 在此CPU调度到该程序时, 这5秒钟将被浪费; 而异步库`asyncio.sleep(5)`将会让出CPU, 在CPU调度到此程序时, 可以执行其他协程中的任务. 同样, 异步库中的文件读写, 网络IO也与原生read, socket及http request行为不同.

2. 一般不同种类的异步库之间的方法不可混用, 比如gevent是用patch的方法让原生标准库拥有异步能力, 但对于某些较为底层(如psycopg2数据库驱动, C语言编写)不能很好的支持; tornado框架的http与socket使用的是其内置的事件循环, 且没有提供异步文件操作. 本系列文档着重讲解asyncio族的异步操作, 与gevent, tornado会有对比, 但不会详细介绍.

## 示例列表

1. [协程模型回显服务器](./01.协程模型回显服务器/readme.md)
    - 使用asyncio编写的简单的echo回显socket服务, 包括服务端与客户端.
    - 原生socket, asyncio提供的`sock_accept()`, `sock_recv()`与`sock_send()`收发函数.
2. [简单协程示例](./02.简单协程示例/readme.md)
    - 使用aiohttp库进行简单的http get请求
    - 进阶示例, 多http请求并发调用.
    - asyncio中的回调函数(`add_done_callback()`)与超时时间(`asyncio.wait()`)设置
3. [动态添加任务](./03.动态添加任务/readme.md)
    - 线程+协程, 动态生成异步协程任务放到事件循环
4. [tornado事件循环初试](./04.tornado事件循环初试/readme.md)
    - tornado实现的事件循环, 极简示例
5. [动态添加任务改进](./05.动态添加任务改进/readme.md)
    - 使用asyncio提供的异步队列, 实现生产者消费者模型
6. [协程超时-装饰器](./06.协程超时-装饰器/readme.md)
    - 一时无聊, 将异步请求中的超时设置抽象成了装饰器, 可重复使用.
7. [限制协程并发数量-semaphore](./07.限制协程并发数量-semaphore/readme.md)
    - 类似于进程间同步机制的`asyncio.Semaphore()`, 限制协程任务的并发数量, 可防止过载.
8. [协程池-asyncpool](./08.协程池-asyncpool/readme.md)
    - 还没来得及写, 但觉得很有必要, 协程虽然占用资源少, 但也不能无限创建.
9. [协程模型回显服务器(二)](./09.协程模型回显服务器(二)/readme.md)
    - asyncio的`start_server()`与loop的`create_server()`, 替换原生socket()来启动服务端.
10. [python3.7中asyncio协程回显示例](./10.python3.7中asyncio协程回显示例/readme.md)
    - python3.7中与3.6相比 asyncio的api有些变化, 这里是一个简单示例.
11. [python3-concurrenct.futures真正的并行计算](./11.python3-concurrenct.futures真正的并行计算/readme.md)
    - `concurrenct.futures()`多进程模型对CPU密集型任务的作用, 最好先理解`concurrenct.futures()`本身的作用.
12. [asyncio的call_XX函数族](./12.asyncio的call_XX函数族/readme.md)
    - call_XXX函数族, 设置协程任务回调操作
13. [异步文件读写及异步数据库操作](./13.异步文件读写及异步数据库操作/readme.md)
    - 选用了两个异步库, 进行异步文件读写与异步数据库读写, 兼容于asyncio的事件循环.
