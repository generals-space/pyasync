参考文章

1. [Python Asyncio 精选资源列表](https://github.com/chenjiandongx/awesome-asyncio-cn)

2. [异步文件操作库 aiofiles](https://github.com/Tinche/aiofiles)

3. [postgres异步数据库驱动 asyncpg](https://github.com/MagicStack/asyncpg)

异步编程中, 最能利用的就是CPU与IO的性能差异了. 而异步IO的应用场景一般包括如下几种

1. 网络请求(socket, http), 可以用asyncio和aiohttp完成.
2. 本地文件读写, 可以用aiofiles完成.
3. 各种数据库驱动.

`gevent`打的patch虽然可以让所有的标准库, 甚至包括一些第三方库(如requests)替换成异步操作, 但是用C作为底层的数据库驱动(比如`psycopg2`)是没办法起作用的;

`asyncio`, `aiohttp`虽然提供了简单的socket服务和http服务, 但并未提供像`ssh`, `ftp`等应用层的异步操作. 各种数据库驱动其实都是基于socket的编程, 与`ssh`, `ftp`等同级, 这些工具只要基于`asyncio`, 就可以配合使用(主要是共用同一个事件循环).

我不清楚gevent是否有办法提供类似的方法, 提供各种数据库驱动. 不过目前好像没有, 除非ta能像twists一样, 有勇气把所有的网络操作重新写一遍...

由于官方的大力支持, `asyncio`提供的异步前景应该很好. 参考文章1中列出了各个领域的异步操作库, 基本上可以满足简单应用的开发.

但毕竟python并不是天生异步的语言, 很多第三方库用的都是同步的方法, 所以一般也只能在这些可见的地方做一些性能上的弥补. 

## 1. 异步文件读写aiofiles

`writefile.py`: 同步的方式循环创建10000的文件, 耗时大概为50s(由主机的性能不同而有所差异)

`writefile_async.py.1`: (已废弃)使用`aiofiles`异步创建文件, 注意, 由于不做任何限制, `main()`函数中的for循环将在一瞬间完成, 会有10000个文件创建然后等待写入. 这样就会报如下错误

```
OSError: [Errno 24] Too many open files: 'data/9999'
```

所以在批量进行异步操作时, 务必要限制并发数量, 比如示例07中的`semaphore`, 示例08中的协程池.

`writefile_async.py`才是一个正确的示例. 只花了12s.

## 2. postgrse异步驱动asyncpg

`insert.py`: 同步的方式循环插入10000条数据, 耗时大概88s.

`insert_async.py.1`: (已废弃)使用`asyncpg`异步插入, 接受了上面的教训, 使用`semaphore`限制了并发数量, 但还是报了错, 如下

```
asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress
```

按照官方issue[cannot perform operation: another operation is in progress](https://github.com/MagicStack/asyncpg/issues/258)中提到的解决方案, 重新编写了`insert_async.py`, 发现可行, 花费15.34s.
