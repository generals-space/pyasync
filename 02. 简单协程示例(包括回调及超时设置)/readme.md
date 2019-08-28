# 02. 简单协程示例(包括回调及超时设置)

## 1. 引言

python是同步语言, 许多原生方法也是按同步方式写的. 异步协程库比如`twisted`, `tornado`框架, 3.5+的`asyncio`库, 都提供了各自的异步方法.

需要说明的是, 异步操作中`yield`, `await`可以在耗时IO操作中交出CPU使用权, 但是无法与原生同步IO操作结合使用. 

比如, `await urllib.urlopen(url)`是无法异步进行的, 它将仍然是阻塞的同步方法.

要想`await`一个异步的http请求, 或是异步的文件读写操作, 都必须使用异步框架/库提供的异步函数, 否则是没用的.

想想, 网上大部分教程都拿`await asyncio.sleep(n)`来模拟耗时IO操作, 这是因为`asyncio.sleep(n)`是异步方法, 对于当前协程当会交出CPU, n秒之后会切换回来继续, 但在同一个线程里的其他协程能够开始执行, 不会造成资源浪费. 如果使用`await time.sleep(n)`呢? 原生`sleep`是一个同步方法, 会一直占用CPU, 无法切换.

本章`02. 协程流程示例`中, 使用了一个`http://note.generals.space/aio`接口, 对于一个请求, 它会随机沉睡`1-30`秒再返回, 返回的内容是一个json字符串, 结构为`{delay: 沉睡的秒数}`, 示例中用这个接口来学习协程的使用方法.

正如我上面所说, `await urllib.urlopen(url)`没有任何意义, 所以这些示例都将使用`aiohttp`库提供的异步函数.

## 2. 实践

回调的魅力在并发, 单个异步请求基本看不出其优势, 所以本节还给出了多个异步请求的示例.

不过这几个示例过于死板, 只能添加静态任务, 无法动态添加...

### 2.1 `simple_get.py`: 单个异步请求

输出

```
task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
result read type:  <class 'bytes'>
result content:  b'{"delay":3}'
cost 3.991998
```

### 2.2 `simple_get_timeout.py`: 单个异步请求+超时设置

单个异步请求, 使用`asyncio.wait`, 设置一个超时时间;

输出

```
task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
result read type:  <class 'bytes'>
result content:  b'{"delay":5}'
cost 6.382042
```

上面的输出中该请求并没有超时(因为服务端的响应是随机的, 你可以多次请求, 或者调整代码中的超时时间.) 下面的示例有超时的打印

### 2.3 `multi_get.py`: 异步请求列表+回调函数

这个示例同时发起多个请求并设置了回调函数;

输出

```
request 1 to https://note.generals.space/aio success
request 2 to https://note.generals.space/aio success
request 4 to https://note.generals.space/aio success
request 5 to https://note.generals.space/aio success
request 0 to https://note.generals.space/aio success
request 3 to https://note.generals.space/aio success
request 9 to https://note.generals.space/aio success
request 6 to https://note.generals.space/aio success
request 7 to https://note.generals.space/aio success
request 8 to https://note.generals.space/aio success
b'{"delay":24}'
b'{"delay":12}'
b'{"delay":28}'
b'{"delay":23}'
b'{"delay":17}'
b'{"delay":26}'
b'{"delay":29}'
b'{"delay":16}'
b'{"delay":17}'
b'{"delay":21}'
cost 29.044463
```

这结果很优秀, 10个请求中耗时最长的是29秒, 于是整个流程的时长也是29秒.

### 2.4 `multi_get_timeout.py`: 异步请求列表, 也设置了超时及回调函数

输出

```
request 1 to https://note.generals.space/aio success
request 4 to https://note.generals.space/aio success
request 2 to https://note.generals.space/aio success
task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
result read type:  <class 'bytes'>
result content:  b'{"delay":9}'
task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
result read type:  <class 'bytes'>
result content:  b'{"delay":8}'
task result type:  <class 'aiohttp.client_reqrep.ClientResponse'>
result read type:  <class 'bytes'>
result content:  b'{"delay":3}'
timeout...
<Task pending coro=<<_RequestContextManager without __name__>()> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x038F1390>()]> cb=[callback(3, 'https://note.generals.space/aio')() at .\multi_get_timeout.py:13]>
<class '_asyncio.Task'>
timeout...
<Task pending coro=<<_RequestContextManager without __name__>()> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x038DF810>()]> cb=[callback(0, 'https://note.generals.space/aio')() at .\multi_get_timeout.py:13]>
<class '_asyncio.Task'>
cost 10.005833
```

超时时间设置为10秒, 一共发起5个请求, 可以看到3个成功, 2个超时的结果.
