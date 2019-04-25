参考文章

1. [python异步并发模块concurrent.futures简析](http://lovesoo.org/analysis-of-asynchronous-concurrent-python-module-concurrent-futures.html)

2. [python concurrent.futures](https://www.cnblogs.com/kangoroo/p/7628092.html)

3. [python 3.7 官方文档 loop.run_in_executor](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)

## 0. 关于concurrent.futures

1. `python 3.x`中自带了`concurrent.futures`模块.
2. `python 2.7`需要安装`futures`模块, 使用命令`pip install futures`安装即可.

实际上, `concurrent.futures`模块与异步毫无关系, 这只是一种并行操作的高级操作, ta提供的`ProcessPoolExecutor`与`ThreadPoolExecutor`比`multiprocess`与`threading`实现的多进程和多线程简单太多了(不过没那么灵活).

可以看一下这个模块的使用, 因为这个模块对`Future`的应用很...单纯, 没有事件循环,协程对象,Task任务等概念的干扰.

另外, `asyncio`也有`loop.run_in_executor()`函数与`concurrent.futures`的`Executor`结合的使用方法, 可以查看参考文章3. 

## 1. step1

在已经了解了`concurrent.futures`的情况下, 读官方文档给出的示例就非常简单了. `step1.py`就是(精简过)示例代码. 不过这个代码在windows平台3.7.3版本下, `ProcessPoolExecutor`模型会出问题, 只能在linux下运行.

```
concurrent.futures.process.BrokenProcessPool: A process in the process pool was terminated abruptly while the future was running or pending.
```

另外, `run_in_executor()`貌似只能运行一个函数, 且必须通过`await`阻塞得到结果, 无法执行多个并行任务, 也无法后台执行...起码目前我还没有找到方法.

## 2. step2和step3

本来以为`run_in_executor()`是个鸡肋, 毕竟无法做到后台执行和多任务并行, 打脸了.

想像一下, 在协程任务中有一部分操作是cpu密集型的工作, 比如计算一个大数, 或者用for循环对对象或是字符串做一些处理, 一定会对其他协程造成影响.

在`step2.py`中, 构造了如下流程: 请求一个网页, 这个地址会随机在0-30秒后返回, 请求完成后调用回调函数, 在回调中用`time.sleep()`模拟了cpu耗时操作. 

执行输出在`step2.py`底部给出, 不难看出`time.sleep()`对整个流程的影响.

`step3.py`就是使用`Executor`提供解决方案的代码. 将协程任务中的cpu密集型操作, 通过`loop.run_in_executor()`放到额外的线程/进程池中, 避免阻塞其他协程的运行, 效果显著.

`executor`初始化时`max_workers`值为4, 是因为我的电脑为4核, 可以最大限度地利用多核优势.

在使用`ProcessPoolExecutor()`时, 执行到`run_in_executor()`部分, 通过`ps`命令可以得到如下输出:

```
[root@b4e239c15bd1 /]# ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 12:05 pts/0    00:00:00 /bin/bash
root        31     0  0 12:05 pts/2    00:00:00 /bin/bash
root        50    31  0 12:06 pts/2    00:00:00 vim step3.py
root        61    50  0 12:08 pts/2    00:00:00 sh
root        62    61  5 12:08 pts/2    00:00:00 python step3.py
root        63    62  0 12:08 pts/2    00:00:00 python step3.py
root        64    62  0 12:08 pts/2    00:00:00 python step3.py
root        65    62  0 12:08 pts/2    00:00:00 python step3.py
root        66    62  0 12:08 pts/2    00:00:00 python step3.py
root        70    16  0 12:08 pts/1    00:00:00 ps -ef
```

而换成`ThreadPoolExecutor()`, 需要使用特定的`ps`选项, 才能看到关于线程的输出:

```
[root@b4e239c15bd1 /]# ps H -eo user,pid,ppid,tid,time,%cpu,cmd
USER       PID  PPID   TID     TIME %CPU CMD
root         1     0     1 00:00:00  0.0 /bin/bash
root        31     0    31 00:00:00  0.0 /bin/bash
root        79    31    79 00:00:00  0.6 python step3.py
root        79    31    88 00:00:00  0.0 python step3.py
root        79    31    89 00:00:00  0.0 python step3.py
root        79    31    90 00:00:00  0.0 python step3.py
root        79    31    91 00:00:00  0.0 python step3.py
root        93    16    93 00:00:00  0.0 ps H -eo user,pid,ppid,tid,time,%cpu,cmd
```

注意

1. 两者在`PID`列的不同.
2. `ProcessPoolExecutor()`在windows下仍然会出错.