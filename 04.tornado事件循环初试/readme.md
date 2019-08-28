## 关于tornado

在最近一次看了tornado官方文档后, 发现ta并没有什么优势可言.

tornado官方文档分为几个部分, 包括异步web框架, 异步http客户端与服务端, 异步socket函数工具集, 事件循环及协程定义工具集.

异步web框架可用sanic代替, 异步http客户端与服务端类似于aiohttp, 而异步socket与事件循环, 可以用asyncio代替. tornado只是这些库的集合而已, 原生库的出现让我觉得没必要使用tornado.

## 关于回调

参考文章

1. [tornado 中的异步调用模式](https://sanyuesha.com/2017/02/08/tornado-async-style/)

回调及获取返回值的示例没看懂, 不太想看了. 决定以后采用队列的形式在协程之间共享数据, 而不是用各种回调, 嵌套来完成.

## 关于示例

2018-09-17(02)

希望能有地方可以取到协程的返回值, 以便进一步处理(就像流水线一样). 查了很多文档, 但都不符合我的要求. 最终还是决定用golang相似的方式来处理协程间的数据共享.

这里发现了`add_callback()`函数...这个函数看起来像是为协程添加回调的, 但是源码中的注释为`Calls the given callback on the next I/O loop iteration.`. 其实和`spawn_callback`类似, 使用时没看到有什么不一样的地方.

2018-09-17(01)

tornado的示例03参考了官方示例[Queue example - a concurrent web spider](https://www.tornadoweb.org/en/stable/guide/queues.html), 模仿了示例02, 实现了类似生产者与消费者的过程. 不过这次没有通过单独开线程去维护一个事件循环, 而是用协程 + 队列实现. 

示例02是子线程维护事件循环, 主线程不停获取新任务, 然后创建协程对象丢给事件循环对象, 即, 两个线程间共享的是事件循环对象. 从这一点上看, 示例02其实是不太理想的. 需要改进.