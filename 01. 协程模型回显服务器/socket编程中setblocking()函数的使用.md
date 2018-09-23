# socket编程中setblocking()函数的使用

参考文章

1. [“socket.error: [Errno 11] Resource temporarily unavailable” appears randomly](https://stackoverflow.com/questions/38419606/socket-error-errno-11-resource-temporarily-unavailable-appears-randomly)

```py
socket.setblocking(flag)
```

如果flag为0, 则将套接字设置为非阻塞模式. 否则, 套接字将设置为阻塞模式(默认值). 

在非阻塞模式下, 如果`recv()`调用没有发现任何数据或者`send()`调用无法立即发送数据, 那么将引发`socket.error`异常. 

在阻塞模式下, 这些调用在处理之前都将被阻塞. 