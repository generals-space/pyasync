# pyasync

参考文章

1. [Python黑魔法 --- 异步IO（ asyncio） 协程](https://www.jianshu.com/p/b5e347b3a17c)
    - 参考文章1深入浅出地介绍了协程及其相关概念(loop事件循环, task任务, future结果对象), 层层递进, 容易理解. 相对于`廖雪峰`老师对`async/await`的两篇介绍文章, 更加系统, 且条理更加分明, 用作入门非常棒.

## 1. python异步与协程入门

首先要明确如下认知:

### 1.1 同步语言的异步库与原生标准库不兼容. 

以python为例, 原生标准库的`time.sleep(5)`将占用 CPU 5秒钟, 在此CPU调度到该程序时, 这5秒钟将被浪费; 而异步库`asyncio.sleep(5)`将会让出CPU, 在CPU调度到此程序时, 可以执行其他协程中的任务. 

同样, 异步库中的文件读写, 网络IO也与原生`read()`方法, `socket`及 http request 行为不同.

### 1.2 一般不同种类的异步库之间的方法不可混用

`gevent`是用`patch`的方法让原生标准库拥有异步能力, 但对于某些较为底层的第3方库(如psycopg2数据库驱动, C语言编写)不能很好的支持; 

`tornado`框架的`http`与`socket`使用的是其内置的事件循环, 且貌似没有提供异步文件操作. 

本系列文档着重讲解`asyncio`族的异步操作, 与`gevent`, `tornado`会有对比, 但不会详细介绍.

### 1.3 

常规同步库, 单线程连续发送5个请求请求.

```
  请求开始
    ↓
    |--5--|---7---|--5--|--5--|---7---|
                                      ↑
                                    请求结束
```

使用异步库.

```
  请求开始
    ↓
    |--5--|
     |---7---|
      |--5--|
       |--5--|
        |---7---|
                ↑
              请求结束
```

## 2. 概念解释

自从写过 golang, 了解了ta的`GMP`模型以后, 对于 python 中的各种异步概念总算有了一个大致的理解, 这里用一种更加通俗(但可能不太准确)的方式来描述一下.

1. 协程(coroutine): 通过`async`关键字声明, 但ta本身无法执行. 普通函数`abc()`就可以开始执行, 但是协程函数`abc()`就只能得到一个对象, 拥有有各种属性.

2. 任务(task): 任务是对协程进一步封装, 单纯的协程对象虽然可以直接被放到事件循环中去执行, 但是有很多异步特性没有办法使用(比如绑定回调函数). 想要使用这些特性, 只能将`coroutine`协程封装成`task`任务(参考`loop.create_task()`方法).

3. 事件循环(event loop): 因为`coroutine`和`task`都只是对象, 没有办法执行, 那么怎么执行呢? 就是将ta们丢到事件循环中去. 

------

其实`event loop`可以理解为非异步场景中的线程池, 里面内置n个 worker, 这些 worker 不断从 task/coroutine 任务列表中取任务并执行. 

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

我们在使用`asyncio`异步库时, 也只需要创建一个`event loop`, 并创建协程任务, 然后把任务放到事件循环中即可(`worker`都不用管了).

而且**回调**也没有那么可怕, 常规的多线程编程其实也算是异步, 想一想在那种场景下是怎么解决的? 其实就是回调函数, 或是结果队列, 总之解决方案很多.

### 2.1 await

`await`这个还是单独说一下, 这个关键字用于挂起阻塞的异步调用接口. 

一般来说, 需要`await`的都是`sleep`, 磁盘IO, 网络IO等需要 cpu 空转以等待的操作,. 在`await`后, 语句会正常执行, 但是 cpu 会让出, 去执行其他协程. 等到`await`的操作有了结果, 返回时异步框架会回到这个地方继续执行. 比如`await asyncio.sleep(5)`, `await aioSession.get(url)`等.

最初接触这个概念还是比较萌b的, 不懂ta在说什么...(＠_＠), 现在终于稍微明白一点了.

假设有如下协程函数, 创建两个协程对象并放入到事件循环中, 你猜会怎样?

```py
async def do_something():
    a = 0
    for i in range(10000000): a += i
```

这其实就是我们所说的 cpu 密集型任务, 一个协程任务一旦获取到 cpu 就不会让出了, 这就会导致另一个协程任务迟迟得不到执行机会而"饿死".

```
  请求开始                             直到 for 循环结束
    ↓                                   ↓
    |--------------------------------...|
                                        |------| // 第2个任务根本没机会执行.
```

适用于`asyncio`的是IO密集型的任务, 如下

```py
async def do_something(url):
    await aiohttpSession.get(url)
```

创建`10000000`个协程对象, 放入到事件循环, 程序会立刻创建`10000000`个 http 请求. 因为`aiohttpSession.get()`是一个异步的操作(由`aiohttp`提供), `await`在发出请求后让出 cpu, 不阻塞等待ta的执行结果, cpu 会立刻切换到**同线程的其他协程**, 实现 cpu 资源的最大利用.

...当然上面这种操作还是很危险的, 虽然协程很轻量, 占用 cpu 内存都很少, 但是`10000000`这个数值还是太大了, 会把服务器的其他资源耗尽的(比如打开文件数, 端口数量等). 而且目标服务器也一定会被搞崩溃的, 毕竟千万级并发了.

> 注意: 对于一个异步的协程对象, 如果不使用`await`执行ta, 那这个协程就根本不会执行.

> 另外也不要尝试`await sleep(5)`这种操作了, `await`后面只能接异步协程对象, 任何同步库的方法都不能与异步`await`共用的.

在 golang 中, 什么时候需要挂起协程(即`await`一个协程)是不需要开发者关心的, 因为 golang 在底层提供了对协程的支持, 在进行诸如文件读写, 睡眠等系统调用前就可以判断此操作是否需要让出 cpu 了(底层的系统调用函数是有限的, golang 只需要关注有限的几个就可以了).

而 python 本身并不支持协程, 目前所有的异步框架都是上层的封装, 前期`yield`关键字应该在底层借助了类似 linux 的`sched_yield`系统调用, 实现了主动让出 cpu 的行为.

------

还有一点, 如果你学过编译原理相关的东西, 了解`PC`寄存器存储着下一条指令的地址, 就会知道, 在`await`让出 cpu 后再让 ta 回到原来的位置继续执行大致是如何实现的了. 不只是`PC`, 协程在执行过程中各种局部变量等执行现场信息, 应该都是存储在`coroutine`对象中的, 其底层原理还有待探究.

## 3. 示例列表

下述示例中有多个示例都用到了`http://localhost:3000/aio`这个接口, 是用**示例14**提供的. 对于一个`/aio`请求, 它会随机沉睡`1-30`秒再返回(模拟服务端的处理耗时), 返回的内容是一个json字符串, 结构为`{delay: 沉睡的秒数}`.

1. [协程模型回显服务器](./01.协程模型回显服务器/readme.md)
    - 使用`asyncio`编写的简单的echo回显`socket`服务, 包括服务端与客户端.
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
