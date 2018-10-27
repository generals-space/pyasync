参考文章

1. [python并发3：使用asyncio编写服务器](https://segmentfault.com/a/1190000010009295)
    - asyncio.start_server()的C/S示例

2. [Prompt for user input using python asyncio.create_server instance](https://stackoverflow.com/questions/29081929/prompt-for-user-input-using-python-asyncio-create-server-instance)

3. [Asyncio persisent client protocol class using queue](https://stackoverflow.com/questions/30937042/asyncio-persisent-client-protocol-class-using-queue/30940625#30940625)

此示例是`01.协程模型回显服务器`的进一步扩展.

在示例`01`中, 使用原生`socket`库创建socket套接字, 然后使用`loop.sock_accept()`处理连接, 使用`loop.sock_recv()`和`loop.sock_sendall()`收发数据.

我以为之后的异步socket就是要用这种方式了, 然后我发现了`loop.create_server()`和`asyncio.start_server()`这两个东西...

`server.py`与`client.py`这一对还比较常规, 参考了参考文章1, 用`asyncio.start_server()`代替原生socket创建server, 也不必再像示例01中使用`sock_accept()`去等待客户端连接. `start_server()`的使用方法非常简单, 类似于web框架中的路由与处理函数的关系, 处理函数会传入reader, writer两个参数, 通过ta们进行数据的读写.

然后是`protocol_server.py`与`protocol_client.py`这一对, 使用了`loop.create_server()`方法. 其实点进`asyncio.start_server()`的源码中你会发现ta调用的正是`loop.create_server()`. 但是直接使用还是比较麻烦的.

`create_server`方法需要传入一个工厂类(`asyncio.Protocol`的实例), 用作客户端连接的处理. 我们需要在其中重写各种钩子函数, 类似于nodejs中的`socket.on('connect'|'data'|'close')`这种. 本来我以为这样会很简单的, 但是在客户端程序中, 命令行异步读取用户输入的时候遇到了问题. 

原生`input`方法无疑是一个阻塞的同步方法, 在`connection_made()`方法中使用`while`循环读取用户输入然后发送给服务端. 这个流程是没错的, 但是由于while + 同步input, 使得`data_received()`的处理函数无法被调用(因为while循环一直占用着CPU不会让出), 这就导致回显的`print`语句无法打印.

为了解决这个问题, 我们需要使用一个异步的标准输入的读取函数, 然后我找到了参考文章2. 与我们的情况相同, 题主也是想扩展asyncio官方文档中的回显服务器, 希望用户能自行输入信息传入服务端再回显. 而答主提供了一个asyncio中异步读取一个文件描述符的函数`got_stdin_data`, 很合用. 但是答主的例子是服务端的, 我只采用了这个函数和异步队列的想法.

之后又遇到一个问题, 用户的输入传入到队列里了, 但是Protocol的成员方法全是同步的, 非`asaync`定义的函数没法使用`await`...

为此又找到了参考文章3, 答主给出的解决方案正是针对客户端逻辑的. 其基本原理是, 将用户输入的消息队列传入给工厂类的构造函数, 然后定义一个协程任务作为工厂类的成员函数, 在与服务端建立连接后开始执行这个任务, 而在这个任务中, 就是用while循环不停从队列中取数据然后发送出去的逻辑了. 

good, 队列真是个好东西.

------

总结一下, 我本以为`create_server`的工厂模型会简单一些, 但仔细想来, ta使用类似于nodejs的处理方法, 把读与写独立在两个函数中, 会显得有些割裂. 当读写操作相互依赖时, 这个模式必然会带来一些麻烦. 日后根据业务逻辑再进行选择吧.