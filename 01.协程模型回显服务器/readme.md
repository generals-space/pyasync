# 协程模型回显服务器

参考文章

1. [Python黑魔法 --- 异步IO（ asyncio） 协程](https://www.jianshu.com/p/b5e347b3a17c)
    - 参考文章1深入浅出地介绍了协程及其相关概念(loop事件循环, task任务, future结果对象), 层层递进, 容易理解. 相对于`廖雪峰`老师对`async/await`的两篇介绍文章, 更加系统, 且条理更加分明. 只不过偏了一点, 并不完全适用我们`echo server`的使用场景. 但是入门的非常棒.
2. [从 asyncio 简单实现看异步是如何工作的](https://ipfans.github.io/2016/02/simple-implement-asyncio-to-understand-how-async-works/)
    - 比较符合我们的项目, 尤其是对于`echo server`的协程模型, 提供了较为底层的代码, 而不是像网上大部分示例中使用`start_server`, `reader`, `writer`, 或是`asyncio.Procotol`这种更高级的工具.
3. [Low-level socket operations](https://docs.python.org/3.5/library/asyncio-eventloop.html#low-level-socket-operations)


server端`async_server.py`使用了`asyncio`自带的底层封装`sock_accept`, `sock_recv`和`sock_send`, 需要python3.5+. 

```
[root@efd527db107f ~]# python server.py 
开始监听...
收到来自 127.0.0.1:59148 的连接
get
收到来自 127.0.0.1:59150 的连接
get
```

`client`没什么较大的变化, 额外又写了一个`async_client.py`客户端(...好像没什么用)

> 除了python3中取消了`raw_input()`函数, byte str与普通str分成了两个不同的类型, 在`recv`与`send`前后需要调用`encode()`或`decode()`进行转换.

要使用`sock_accept`这些`asyncio`内置的异步函数, 需要设置`setblocking(False)`. 否则只有第一个客户端能与服务端进行通信, 在这个连接断开之前, 之后的客户端能与服务端建立连接但无法发送信息, 会一直阻塞.

------

`async_server.py.1`和`async_server.py.2`是我尝试不使用`asyncio`内置函数`sock_accept`这些, 而是自定义接收与发送协程的示例代码, 不过可惜运行不成功.

`async_server.py.1`甚至不能与客户端建立连接, 改用`sock_accept`后, 能与第一个接入的客户端进行正常通信, 但是之后的客户端还是会被阻塞.

个人感觉异步编程精髓在于异步处理流程以及如何定义协程函数, 但是`asyncio`的封装太强, 对更深入理解协程没有太大帮助.