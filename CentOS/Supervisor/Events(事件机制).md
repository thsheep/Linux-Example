## Events

Events是Supervisor在3.0版引入的一项高级功能,
如果您只是想使用Supervisor作为重启崩溃进程的机制，
或者作为手动控制进程状态的系统，则无需了解Events。
如果要将Supervisor用作流程监视/通知框架的一部分，则需要了解Events。

#### Events监听器和Events通知

Supervisor提供了一种专门编写的程序的接口（它作为子进程运行），称为“Events监听器”，
用以订阅“Events通知”。
Events通知意味着发生了与Supervisord控制的子过程相关的Events或者监控Supervisord自身。
Events通知被分组为各种类型，以便Events监听器可以订阅Events通知的各种类别
即使没有配置listener，Supervisor也会持续发出事件通知。
如果listener被配置并订阅了在supervisord生命期内发出的事件类型，
那么该侦听器也能接到通知。
事件通知协议基于通过子进程stdin和stdout的通信。
Supervisor将特殊格式的输入发送到事件listener进程“stdin”，并且需要来自事件listener stdout的特殊格式的输出，
从而形成一个请求 - 响应循环。
监督者和监听者实现者之间达成的协议允许监听者处理事件通知，
 Event listeners可以用您用来运行Supervisor的平台支持的任何语言编写。
尽管Event listeners可以用任何语言编写，但是supervisor.childutils模块的形式存在对Python的特殊库支持，
这使得在Python中创建事件监听器比其他语言稍微容易一些。

#### 配置Event listeners

一个Supervisor Event listeners是通过配置文件中的 \[eventlistener：x\] 部分指定。
upervisor \[eventlistener：x\]部分的处理几乎与supervisor \[program：x\]部分一样，
除了Supervisor事件监听器进程的“捕获模式”输出外
（即事件监听器不能是PROCESS_COMMUNICATIONS_EVENT事件生成器）。
因此，在event listener的配置中指定stdout_capture_maxbytes或stderr_capture_maxbytes是错误的。
可以配置文件中的event listener部分的数量没有任何人为的限制。

当定义了\[eventlistener：x\]部分时，它实际上定义了一个“池”，其中池中的事件侦听器的数量由该部分中的numprocs值决定

\[eventlistener：x\]部分的events参数指定将发送到listener pool的事件,
一个写得很好的event listener将会忽略它不能处理的事件，
* 但是这并不能不能保证一个特定的event listener不会因为接收到一个不能处理的事件类型而崩溃，
因此，根据listener的实现，在配置中指定它可能只接收某些类型的事件有可能很重要。

可以放在supervisord.conf中的eventlistener配置示例如下：

```
[eventlistener:memmon]
command=memmon -a 200MB -m bob@example.com
events=TICK_60


[eventlistener:mylistener]
command=my_custom_listener.py
events=PROCESS_STATE,TICK_60
```


#### 注意
```
可以通过pkg_resources“entry point”字符串形式的[eventlistener：x]

部分的result_handler参数指定一个高级功能，为池指定备用“结果处理程序”。

默认的结果处理程序是supervisord.dispatchers：default_handler。创建一个替代结果交易者目前没有记录。
```


当Supervisor发送事件通知时，将会找到订阅接收事件类型的事件（由event listener部分中的事件值过滤）的所有事件侦听器池。
每个监听器池中的一个监听器将收到事件通知（任何“可用的”监听器）

Supervisor平均对待事件监听器池中的每个进程。
如果池中的某个进程不可用（要不它正在处理一个事件，要不它已经崩溃，或者已经从池中删除），
这样的话Supervisor将从池中选择另一个进程。
如果由于池中的所有侦听器都处于“忙”状态而无法发送事件，则事件将被缓冲，稍后将重试通知。
“稍后”定义为“下一次执行supervisord选择循环”。想要获得令人满意的事件处理性能，应该使用尽可能多的事件侦听器进程来配置池，以处理事件负载。
对于到底多少侦听器，这只能凭经验确定，并没有什么标准。但是为帮助你确定多少监听合适，在当由于池拥塞而无法立即发送事件时，Supervisor将向其活动日志写入消息堵塞的警告消息。
对可以在池中的进程数量没有做任何人为约束，它仅受限于平台约束。

监听器池有一个事件缓冲区队列。队列大小通过侦听器池的buffer_size配置文件选项。如果队列已满并且超级用户尝试缓冲事件，则超级用户将丢弃缓冲区中最早的事件并记录错误。

#### 编写一个Event listeners：

实现是一个Event listeners程序，它愿意接受stdin流的结构化输入，并在其stdout流上产生结构化的输出。
Event listeners应该以“无缓冲”模式运行，或者每当需要传回supervisord进程时都应该刷新stdout。
Event listeners可以被写成长时间运行，或者可以在单个请求之后退出（取决于实际环境和eventlistener配置中的autorestart参数）。

一个Event listeners可以发送任意的输出到它的stderr，这个输出将被supervisord记录或忽略，
具体取决于\[eventlistener：x\]部分中与stderr相关的日志文件配置。

#### Event Notification协议

当supervisord向事件监听器进程发送通知时，监听器将首先在其stdin上发送单个“header”行,
该行的组成是一组由冒号分隔的令牌（每个代表一个键值对）由一个空格相互分隔。
该行以\ n（换行符）字符结束。
线上的Tokens不保证以任何特定的顺序。目前定义的Tokens类型如下表所示。

#### Header Tokens：

| Key | 说明 |Example|
|-------|-------|-------|
| ver  | 事件系统协议版本  |3.0|
|server|发送事件的supervisord的标识符（请参阅config文件[supervisord]节标识符值。|
|serial|分配给每个事件的整数。在supervisord进程的生命周期中不会生成两个事件将具有相同的序列号。该值对功能测试和检测事件排序异常很有用。|30|
|pool|生成此事件的事件侦听器池的名称。|myeventpool|
|poolserial|由发件人的event listener池分配给每个事件的整数。在supervisord进程的生命周期中，同一个eventlister池所生成的两个事件将具有相同的poolserial号。这个值可以用来检测事件排序异常|30|
|eventname|特定的事件类型名称（请参阅事件类型）|TICK_5|
|len|指示事件有效内容中的字节数的整数，即PAYLOAD_LENGTH|22|

一个完整标题行的示例如下：
```
ver:3.0 server:supervisor serial:21 pool:listener poolserial:10 eventname:PROCESS_COMMUNICATION_STDOUT len:54
```

直接跟在标题中的换行字符是事件有效负载。它由代表事件数据序列的PAYLOAD_LENGTH字节组成。有关特定事件数据序列化定义，请参阅事件类型。

一个PROCESS_COMMUNICATION_STDOUT事件通知的示例负载如下所示：

```
processname:foo groupname:bar pid:123
This is the data that was sent between the tags
```

任何给定事件的有效负载结构仅由事件的类型决定。

#### Event Listener 状态

事件监听器进程有三种可能的状态，由supervisord维护：

|Name|说明|
|-------|-------|
|ACKNOWLEDGED|事件监听器已经确认（接受或拒绝）事件发送。|
|READY|事件通知可以发送给这个事件监听器|
|BUSY|事件通知可能不会发送到此事件侦听器。|

当事件监听器进程首次启动时，Supervisor会自动将其置于ACKNOWLEDGED状态以允许启动活动或防止启动失败（挂起）
在收听者发送READY \ n字符串到它的标准输出之前，它将保持这种状态。

当Supervisor向处于READY状态的监听者发送事件通知时，监听者将被置于BUSY状态，直到监听者收到OK或FAIL响应，此时监听者将转换回ACKNOWLEDGED状态。

#### Event Listener通知协议

Supervisor将通过向进程的stdin发送数据来通知事件的READY状态的事件监听器。
当进程处于BUSY或ACKNOWLEDGED状态时，Supervisor将永远不会向事件监听器进程的标准输入发送任何东西。Supervisor通过发送标题开始。

一旦它处理了Header，事件监听器实现应该从它的stdin中读取PAYLOAD_LENGTH个字节，
根据Header中的值和从序列化中解析出来的数据执行一个任意的操作。
这样做可以自由地阻塞任意时间。 Supervisor将在等待响应时继续正常处理，
并根据需要将同一类型的其他事件发送到同一池中的其他侦听器进程。

在事件监听器处理完事件序列化之后，为了通知supervisord结果，
它应该在其stdout上发回一个结果。其结构是单词“RESULT”，后面是空格，后面是结果长度，后面是换行符，后面是结果内容。
例如，RESULT 2\nOK是结果“OK”。通常，事件侦听器将使用OK或FAIL作为结果内容。这些字符串对默认的结果处理程序有特殊的意义。

如果默认结果处理程序收到OK作为结果内容，它将假定侦听程序成功处理事件通知。如果收到**FAIL**，则认为监听器未能处理事件，事件将被重新缓存并在稍后发送。
事件监听器可以通过返回FAIL结果来以任何理由拒绝该事件。
这并不表示事件数据或事件侦听器有问题。一旦supervisord接收到**OK**或**FAIL**结果，事件监听器就进入**ACKNOWLEDGED**状态。

一旦监听器处于**ACKNOWLEDGED**状态，它可以退出（如果监听器的autorestart配置参数为true，监听器随后可以重新启动），也可以继续运行。
如果它继续运行，为了被supervisord放回READY状态，它必须发送一个READY标记，然后立即发送一个换行到它的标准输出。


#### 事件监听器实现示例

* 一个“长时间运行”的事件监听器的Python实现，它接受一个事件通知，将标题和有效载荷打印到它的stderr，并以OK结果进行响应，然后READY。如下。
    ```
    import sys
    def write_stdout(s):
        # 只有event listener协议消息可能被发送到标准输出
        sys.stdout.write(s)
        sys.stdout.flush()

    def write_stderr(s):
        sys.stderr.write(s)
        sys.stderr.flush()

    def main():
        while 1:
            # 从ACKNOWLEDGED转换到READY
            write_stdout('READY\n')

            # 读取标题行并将其打印到stderr
            line = sys.stdin.readline()
            write_stderr(line)

            # 读取事件有效负载并将其打印到stderr
            headers = dict([ x.split(':') for x in line.split() ])
            data = sys.stdin.read(int(headers['len']))
            write_stderr(data)

            # 从READY转换到ACKNOWLEDGED
            write_stdout('RESULT 2\nOK')

    if __name__ == '__main__':
        main()

其他事件侦听器示例在 [superlance](http://supervisord.org/glossary.html#term-superlance) 软件包中，其中包括可以监控supervisor子进程的一个事件侦听器，以及在使用“太多”内存时重新启动进程的事件侦听器。

#### 事件监听器错误情况:

如果事件监听器进程在事件传输到stdin的过程中死亡，或者在将结果发送回supervisord之前死亡，则认为该事件不被处理，并且将由supervisord重新进行处理并在稍后再次发送。

如果事件侦听器根据事件侦听器处于的状态将其数据发送到其标准输出，但是该超级用户不能识别为适当的响应，事件侦听器将被置于未知状态，并且不会向其发送任何事件通知。
如果在此期间侦听器正在处理一个事件，那么它将被重新缓冲并在稍后再次发送。

#### 其它：

事件监听器可以使用管理器XML-RPC接口来调用“返回”给Supervisor。因此，事件监听器可以通过接收事件通知来影响Supervisor子进程的状态。
例如，您可能希望每隔几分钟就会生成一个与Supervisor控制的子进程的进程使用相关的事件，如果这些进程中的任何一个超过了某个内存阈值，则希望重新启动它。
你可以编写一个程序，让Supervisor每隔一段时间就产生一次PROCESS_COMMUNICATION事件，并在其中存储信息，还有一个事件监听器来处理从这些事件接收到的数据。

### 事件类型：
事件类型是由Supervisor自己定义的受控集合。如果不更改supervisord本身，则无法添加事件类型。
但是，这通常不是问题，因为元数据被附加到可以被事件监听器用作附加过滤标准的事件，并与其类型一起使用。
