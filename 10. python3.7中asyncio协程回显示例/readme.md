参考文章

1. [asyncio — Asynchronous I/O](https://docs.python.org/3.7/library/asyncio.html)

之前的示例是在python3.6下的, 从来没有使用过`asyncio.coroutine`装饰器和`yield from`, 直接上的`async`和`await`. 

然而官网上很快就出现了3.7的链接. 这一版的其他更新就算了, `asyncio`库的可用性也有了很大的优化. 

首先就是不必再手动创建或获取事件循环了, 不必在`get_event_loop`然后`run_forever`或`run_until_complete`, 直接一个`asyncio.run(协程)`就可以了, 方便好多.

然后就是官方文档的条理变得很清晰, ta将`asyncio`提供的API分为了两部分, 高级接口和低级(底层)接口.

高级接口包括:

1. 协程coroutine和任务task
2. stream流(socket相关, 不是`sock_recv`或`sock_sendall`这种, 而是`reader`和`writer`)
3. 同步锁的异步实现(`Lock`, `Event`, `Semaphore`等)
4. 异步进程(异步的exec族, popen, shell等方法和异步进程间通信)
5. 异步队列(用协程间通信十分方便)
6. 异步异常

低级接口包括:

1. 事件循环(获取循环的方法, 回调处理, 服务器对象(socket), 事件循环的实现等)
2. `Future`对象
3. `Transport`和`Procotol`工厂类
4. `Policies`事件循环对象, 没用过
5. ~~平台支持~~ 呃, 这个不算, 只是讲了下不同平台下有些接口不太通用.

在3.7之前, `get_event_loop`等相关函数是属于低级接口中的事件循环的部分, 3.7中出现了`asyncio.run`并把这个方法归为高级接口中的协程coroutine和任务task这部分了, 并且建议使用高级接口.

示例10中使用`asyncio.run()`重写了示例09中的`asyncio.start_server()`示例...为什么不重写`loop.create_server()`? 官方都没有这个的示例...写起来太麻烦了, 不写了.