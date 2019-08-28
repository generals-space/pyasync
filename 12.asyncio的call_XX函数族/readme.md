参考文章

1. [asyncio并发编程](http://www.cnblogs.com/lyq-biu/p/10486148.html)

2. [Python黑魔法 --- 异步IO（ asyncio） 协程](https://www.jianshu.com/p/b5e347b3a17c)

`asyncio`的`call_XX`函数族中的函数有如下几个

- `call_at(when, callback, *args)`: 参数`when`是以`loop.time()`为基准的数值, 比如`loop.time() + 10`, 表示10s(协程中的时间, 不会阻塞其他协程的执行)后调用`callback`函数;
- `call_later(delay, callback, *args)`: 参数`delay`为整数, 以当前`loop.time()`为基准, 猜测`call_later(10, callback)`等价于`call_at(loop.time() + 10, callback)`;
- `call_soon(callback, *args)`: 猜测`call_soon(callback)`等价于`call_later(0, callback)`;
- `call_soon_threadsafe`: 线程安全的操作, 使用方法与`call_soon`一致.

ta们的作用个人感觉基本类似于js中的`setTimeout()`, 都是手动设置一个回调, 还可以控制回调的延迟时间, ta们都接受一个普通函数而非协程函数.

------

`call.py`为`call_XX`函数族的使用方法, 几乎相同.

~~ 关于`call_soon_threadsafe()`的使用场景, 一直没找到合适的, `call_safe.py.1`是使用子线程维护协程事件循环, 然后在主线程中动态添加任务. 但是在协程任务中无论使用`call_soon()`还是`call_soon_threadsafe()`都没有报错...先这样的, 以后再找找必须使用后者的情况. ~~

好吧, 按照参考文章2, 又重新编写了`call_safe.py`, 在这个程序中, `call_soon()`方法的确不好使.
