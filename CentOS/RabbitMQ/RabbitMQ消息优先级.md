### 优先队列支持
从版本3.5.0开始，RabbitMQ在核心中实现优先队列。

您可以使用x-max-priority参数声明优先级队列。该参数应该是一个整数，指示队列应该支持的最大优先级。

例如Java客户端：

```java:n
Channel ch = ...;
Map<String, Object> args = new HashMap<String, Object>();
args.put("x-max-priority", 10);
ch.queueDeclare("my-priority-queue", true, false, false, args);
```

然后，您可以使用**basic.properties**的优先级字段发布优先消息。数字越大表示优先级越高。

因为优先级队列的磁盘格式不同，所以优先级队列只能由参数定义，而不能由策略定义。队列永远不会改变它们支持的优先级数量。

#### 特性：

AMQP 0-9-1规范对于优先级的工作方式有些模糊。它表示所有队列必须至少支持2个优先级，并且可以支持多达10个。它没有定义如何处理没有优先级属性的消息。

与AMQP 0-9-1规格相反，默认情况下，RabbitMQ队列不支持优先级。在创建优先级队列时，您可以根据需要指定任意数量的优先级。

**注意：**

每个队列的每个优先级有一些内存和磁盘上的成本。还有一个额外的CPU成本，特别是在消费时，所以最好不要创造太多的优先级队列。

消息**priority**字段被定义为无符号字节，所以实际上优先级应该在0到255之间。

没有**priority**属性的消息被视为优先级为0.**priority**高于队列最大值的消息被视为以最高优先级发布。

#### 使用注意事项：

如果需要优先级队列，​​建议在1到10之间使用。目前使用更多优先级将消耗更多资源（Erlang进程）。

#### 消费的影响：

理解消费者在处理优先级队列时的工作方式非常重要。

如果这样一个正在等待的消费者连接到随后发布消息的空队列，消息可能不会在队列中等待任何时间。在这种情况下，优先队列将不会有任何机会优先考虑它们。

在大多数情况下，您会希望在消费者手动确认模式下使用basic.qos方法，以限制可以随时发送的消息数量，从而允许优先化消息。

#### 其它功能影响：

通常，优先级队列具有标准RabbitMQ队列的所有功能：它们支持持久性，分页，镜像等。有几点需要注意的影响：

应该过期的消息仍然只会从队列的头部过期。这意味着与普通队列不同，即使是每队列TTL也会导致过期的低优先级消息滞留在未到期的高优先级消息后面。这些消息将永远不会传递，但它们将显示在队列统计信息中。

像正常情况一样，具有最大长度集合的队列将从队列头部强制删除消息。这意味着可能会丢弃更高优先级的消息，为低优先级的消息让路，这可能不是您所想要的。
