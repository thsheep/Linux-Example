RabbitMQ 安装配置指南

本安装为测试环境；生产环境需要注意权限问题以及其他问题


基础环境Erlang安装（需要注意RabbitMQ对Erlang版本有要求，请在官方文档中查看）
RabbitMQ 3.6.10版本需要Erlang 19.0.

安装Erlang：

[root@localhost ~]# rpm -ivh erlang-19.0.4-1.el7.centos.x86_64.rpm

安装RabbitMQ：

RabbitMQ依赖于socat

[root@localhost ~]# yum install socat (此包没有依赖，可以下载rpm安装)

[root@localhost ~]# rpm -ivh rabbitmq-server-3.6.10-1.el7.noarch.rpm


开启Web UI界面：
[root@localhost ~]# rabbitmq-plugins enable rabbitmq_management   
					 参考：http://www.rabbitmq.com/management.html


添加用户（RabbitMQ 3.6.10 默认guest用户只能本地登录）:

[root@localhost ~]# rabbitmqctl add_user web web     （添加一个密码为web的web用户）

赋予权限:

[root@localhost ~]# rabbitmqctl set_user_tags  web administrator    (赋予web  administrator权限)

权限列表参考如下：
(1) 超级管理员(administrator)

可登陆管理控制台(启用management plugin的情况下)，可查看所有的信息，并且可以对用户，策略(policy)进行操作。

(2) 监控者(monitoring)

可登陆管理控制台(启用management plugin的情况下)，同时可以查看rabbitmq节点的相关信息(进程数，内存使用情况，磁盘使用情况等)

(3) 策略制定者(policymaker)

可登陆管理控制台(启用management plugin的情况下), 同时可以对policy进行管理。但无法查看节点的相关信息(上图红框标识的部分)。

与administrator的对比，administrator能看到这些内容

(4) 普通管理者(management)

仅可登陆管理控制台(启用management plugin的情况下)，无法看到节点信息，也无法对策略进行管理。


放行fireWalld端口：

[root@localhost ~]# firewall-cmd --zone=public --add-port=5672/tcp --permanent （这是RabbitMQ的队列通讯端口）

[root@localhost ~]# firewall-cmd --zone=public --add-port=15672/tcp --permanent （Web服务端口）

[root@localhost ~]# firewall-cmd --reload （重载规则）

启动RabbitMQ节点：

[root@localhost ~]# rabbitmq-server -detached

停止RabbitMQ节点：

[root@localhost ~]# rabbitmqctl stop

加入开机启动项：

[root@localhost ~]# systemctl enable rebbitmq-server

常用命令：

添加用户：

rabbitmqctl add_user 用户名 密码

查看用户：

rabbitmqctl list_users

设置用户角色的命令为：

rabbitmqctl  set_user_tags  User  Tag

User为用户名， Tag为角色名(对应于上面的administrator，monitoring，policymaker，management，或其他自定义名称)。

一用户多角色：

rabbitmqctl  set_user_tags  hncscwc  monitoring  policymaker

设置用户权限

rabbitmqctl  set_permissions  -p  VHostPath  User  ConfP  WriteP  ReadP

{
	VHostPath  Vhost名字

	User为用户名

	ConfP 配置权限

	WriteP 写权限

	ReadP 读权限
}

例如：rabbitmqctl  set_permissions  -p  test_vhost  web  ".*"  ".*"  ".*" (赋予web用户对test_vhost的配置、读、写 全部权限)

".*" 代表所有权限（支持标准的Perl正则表达式）

例如：rabbitmqctl  set_permissions  -p  test_vhost -s all  web  ""  "test_*"  ".*"  

{

	"" 不允许web用户进行配置操作

	"test_" web只能对test_开始的交换机队列进行写操作

	".*" 允许web用户对所有交换机队列进行读操作
}

查看指定用户的权限信息

rabbitmqctl  list_user_permissions  User

清除用户的权限信息

rabbitmqctl  clear_permissions  [-p VHostPath]  User


日志：

RABBITMQ_NODNAME-sasl.log (erlang运行日志 可用于调试MQ节点无法启动)

RABBITMQ_NODNAME.log (服务器即时日志，可查看连接IP  队列 交换机操作等信息)

RABBITMQ_NODNAME 这个变量取决于你的配置文件

轮换日志：

rabbitmqctl rotate_logs suffix (suffix: 可为单词和数字)

例如 rabbitmqctl rotate_logs .1

