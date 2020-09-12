# pyasync

参考文章

1. [Python黑魔法 --- 异步IO（ asyncio） 协程](https://www.jianshu.com/p/b5e347b3a17c)
    - 参考文章1深入浅出地介绍了协程及其相关概念(loop事件循环, task任务, future结果对象), 层层递进, 容易理解. 相对于`廖雪峰`老师对`async/await`的两篇介绍文章, 更加系统, 且条理更加分明. 只不过偏了一点, 并不完全适用我们`echo server`的使用场景. 但是入门的非常棒.

## python异步与协程入门

首先要明确如下认知:

1. 同步语言的异步库与原生标准库不兼容. 以python为例, 原生标准库的`time.sleep(5)`将占用 CPU 5秒钟, 在此CPU调度到该程序时, 这5秒钟将被浪费; 而异步库`asyncio.sleep(5)`将会让出CPU, 在CPU调度到此程序时, 可以执行其他协程中的任务. 同样, 异步库中的文件读写, 网络IO也与原生read, socket及http request行为不同.

2. 一般不同种类的异步库之间的方法不可混用, 比如gevent是用patch的方法让原生标准库拥有异步能力, 但对于某些较为底层(如psycopg2数据库驱动, C语言编写)不能很好的支持; tornado框架的http与socket使用的是其内置的事件循环, 且没有提供异步文件操作. 本系列文档着重讲解asyncio族的异步操作, 与gevent, tornado会有对比, 但不会详细介绍.

## 概念解释

写过 golang, 了解了ta的GMP模型以后, 对于 python 中的各种异步概念总算有了一个大致的理解, 这里用一种更加通俗(但可能不太准确)的方式来描述一下.

协程(coroutine): 通过`async`关键字声明, 但ta本身无法执行. 普通函数`abc()`就可以开始执行, 但是协程函数`abc()`就只能得到一个对象, 有各种属性.

任务(task): 任务是对协程进一步封装, 单纯的协程对象虽然可以直接被放到事件循环中去执行, 但是有很多异步特性没有办法使用, 比如绑定回调函数, . 想要使用这些特性, 只能将coroutine协程封装成task任务.

事件循环(event loop): 因为`coroutine`和`task`都只是对象, 没有办法执行, 那么怎么执行呢? 就是将ta们丢到事件循环中去. 其实`event loop`可以理解为非异步场景中的子线程, 里面内置一个 worker, 这个 worker 不断从 task/coroutine 任务列表中取任务并执行(我瞎掰的, 内部机理我并不了解, 但我觉得对于新手这样更容易理解).

下面一段代码是我工作中使用`threadpool`线程池的一小段示例.

```py
from threadpool import ThreadPool, makeRequests

## 创建任务, 这里 worker 是一个函数, clusterList 列表类型, 其成员是 worker 函数的参数.
## reqs 是一个任务列表
reqs = makeRequests(worker, clusterList)
## 将任务添加到线程池中
for req in reqs: tPool.putRequest(req)
logger.info('启动线程池... %d' % POOL_SIZE)
## 开始执行
tPool.wait()
```

使用`asyncio`时, 同样要开线程池(就是事件循环, 反正都是黑盒, 管ta内部机制多复杂), 同样要创建任务, 同样要把任务添加到池中, 同样要启动...

而且回调也没有那么可怕, 常规的多线程编程其实也算是异步, 要是不想用回调, 可以通过结果队列解决, 总之方法很多.

------

然后是`await`, `await`用于挂起阻塞的异步调用接口. 一般来说, 需要`await`的都是sleep, 磁盘IO, 网络IO等需要 cpu 空转以等待的操作, 在`await`后, 语句会正常执行, 但是 cpu 会让出, 去执行其他协程. 等到`await`的操作有了结果, 返回时异步框架会回到这个地方继续执行. 比如`await asyncio.sleep(5)`, `await aioSession.get(url)`等.

在 golang 中, 什么时候需要挂起是不需要开发者关心的, 因为 golang 在底层提供了协程的支持, 在进行诸如文件读写, 睡眠等系统调用前就可以判断此操作需不需要让出 cpu 了(毕竟底层的系统调用函数是有限的, 而 golang 只需要关注有限的几个就可以了).

而 python 本身并不支持协程, 目前所有的异步框架都是上层的封装, 前期`yield`关键字应该在底层借助了类似 linux 的`sched_yield`系统调用, 实现了主动让出 cpu 的行为.

------

还有一点, 如果你学过编译原理相关的东西, 了解`PC`寄存器存储着下一条指令的地址, 就会知道, 在`await`让出 cpu 后再让 ta 回到原来的位置继续执行大致是如何实现的了. 不只是`PC`, 协程在执行过程中各种局部变量等执行现场信息, 应该都是存储在`coroutine`对象中的, `coroutine`底层的实现细节应该比我想象的还要复杂.

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
    - `loop.run_in_executor()`的使用.
12. [asyncio的call_XX函数族](./12.asyncio的call_XX函数族/readme.md)
    - call_XXX函数族, 设置协程任务回调操作
13. [异步文件读写及异步数据库操作](./13.异步文件读写及异步数据库操作/readme.md)
    - 选用了两个异步库, 进行异步文件读写与异步数据库读写, 兼容于asyncio的事件循环.
14. [aiohttp.web 简单的异步web服务器](./14.aio_http_server/readme.md)
    - 其他示例请求的`http://localhost:3000/aio`接口, 就是这个服务器提供的.

上述示例中有多个示例使用到了`http://localhost:3000/aio`这个接口, 是用**示例14**提供的. 对于一个`/aio`请求, 它会随机沉睡`1-30`秒再返回, 返回的内容是一个json字符串, 结构为`{delay: 沉睡的秒数}`, 示例中用这个接口来学习协程的使用方法.

