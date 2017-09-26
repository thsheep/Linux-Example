启动参数：
docker run -d -p 8050:8050 --memory=5.0G --restart=always  --name splash       -v /root/proxy-profiles:/etc/splash/proxy-profiles       -v /root/js-profiles:/etc/splash/js-profiles       -v /root/lua_modules:/etc/splash/lua_modules       -v /root/filters:/etc/splash/filters       scrapinghub/splash:master --maxrss 4500

安装流程：
对于Scrapy处理Ajax 处理方式当然是同家兄弟Splash比较靠谱！

但是Splash有个很坑爹的毛病就是负载承受相对较小·· 一不留神就GG了·········· 然后也就没有然后了~~！

所以准备给Splash做一个负载均衡；后端放一大堆的Splash这样总不会GG了吧。

就算其中一个GG了还有其它的可替代不是？

废话不多少开整··

环境是基于：

CentOS 7.3

Docker 17.06.2-ce

Splash 3.0

HAproxy 1.7.9

（CentOS大家可以将yum切换为阿里云的yum源  Docker同理）

阿里yum源： http://mirrors.aliyun.com/help/centos  照葫芦画瓢做一遍（你是CentOS7啊！！！！不要选成其他版本了）

注意以下只需要在你需要运行splash的机器上安装即可

阿里Docker源：

# step 1: 安装必要的一些系统工具

sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# Step 2: 添加软件源信息

sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# Step 3: 更新并安装 Docker-CE

sudo yum makecache fast
sudo yum -y install docker-ce

# Step 4: 开启Docker服务

sudo service docker start
安装Docker加速器：

curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://8050f360.m.daocloud.io
重启Docker：

systemctl restart docker
这样可以极快的速度拉取镜像。

获取splash最新的docker镜像：

docker pull scrapinghub/splash:master
关闭所有机器防火墙firewalld(网络安全的环境关闭，不安全的环境请放行端口，自行百度):

systemctl disable firewalld

systemctl stop firewalld
创建Splash配置文件目录：

# 存放过滤规则文件的目录

[root@localhost ~]# mkdir filters

# 存放JavaScript文件目录

[root@localhost ~]# mkdir js-profiles

# 存放lua模块的目录

[root@localhost ~]# mkdir lua_modules

# 存放代理文件的目录

[root@localhost ~]# mkdir proxy-profiles

# 创建完成如下：

[root@localhost ~]# pwd
/root
[root@localhost ~]# ll
total 4
drwxr-xr-x. 2 root root   25 Sep 26 03:00 filters
drwxr-xr-x. 2 root root    6 Sep 25 21:08 js-profiles
drwxr-xr-x. 2 root root    6 Sep 25 21:08 lua_modules
drwxr-xr-x. 2 root root   32 Sep 25 21:08 proxy-profiles
[root@localhost ~]#
启动Splash：

docker run -d -p 8050:8050 --memory=5.0G --restart=always  --name splash       -v /root/proxy-profiles:/etc/splash/proxy-profiles       -v /root/js-profiles:/etc/splash/js-profiles       -v /root/lua_modules:/etc/splash/lua_modules       -v /root/filters:/etc/splash/filters       scrapinghub/splash:master --maxrss 4500
docker run  启动一个容器

-d 后台启动

-p 8050:8050  将容器的8050端口和物理机的8050端口绑定（可以从8050端口访问容器服务应用）

--memory=5.0G 容器最大使用内存为5.0GB，超出这个限制会被主进程杀死（使用free -mg  查看并酌情设置你的内存使用）

--restart=always 容器退出后无条件重启（满了5GB被杀死，然后重启 释放内存）

--name splash  容器的名字叫splash（可以忽略）

-v ******  三个-v参数是将宿主机的目录挂载进容器，便于容器能够直接访问挂载目录中的内容

scrapinghub/splash:master  用于启动容器的镜像

--maxrss 4500 Splash最大内存使用为4500MB

查看容器是否启动：

[root@localhost ~]# docker ps -a
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS              PORTS                              NAMES
1b34f7933095        scrapinghub/splash:master   "python3 /app/bin/..."   4 hours ago         Up 4 hours          5023/tcp, 0.0.0.0:8050->8050/tcp   splash
[root@localhost ~]#
访问Splash是否正常工作：



请注意：以上操作只需要在你需要运行splash的机器上安装即可



安装HAproxy实现负载均衡：



安装zlib-devel（HAproxy使用gzip功能）：

yum install zlib-devel -y


安装HAproxy：

# 个人喜好 源码放在这个目录
[root@localhost examples]# cd /usr/local/src/

# 安装wget
[root@localhost src]#yum install wget -y

# 下载HAproxy安装包
[root@localhost src]# wget http://www.haproxy.org/download/1.7/src/haproxy-1.7.9.tar.gz

# 解压
[root@localhost src]# tar -zxvf haproxy-1.7.9.tar.gz

# 进入目录
[root@localhost src]# cd haproxy-1.7.9

# 编译
[root@localhost src]# make TARGET=linux2628 PREFIX=/usr/local/haproxy-1.7.9 USE_ZLIB=yes

# 安装
[root@localhost src]# make install 

# 拷贝启动文件到目录
[root@localhost src]# cp /usr/local/sbin/haproxy /usr/sbin/

# 测试版本
[root@localhost src]# haproxy -v

# 拷贝启动文件到启动目录
[root@localhost src]# cp examples/haproxy.init /etc/init.d/haproxy

# 赋予可执行权限
[root@localhost src]# chmod 755 /etc/init.d/haproxy

# 创建配置文件目录
[root@localhost src]# mkdir /etc/haproxy

# 创建数据目录
[root@localhost src]# mkdir /var/lib/haproxy

# 创建运行文件目录
[root@localhost src]# mkdir /var/run/haproxy

# 设置日志
[root@localhost src]# vim /etc/rsyslog.conf
# 第15行  $ModLoad imudp #打开注释
# 第16行  $UDPServerRun 514 #打开注释
# 第74行  local3.* /var/log/haproxy.log #local3的路径

# 创建日志文件
[root@localhost src]# touch /var/log/haproxy.log

# 设置权限
[root@localhost src]#  chown -R haproxy.haproxy /var/log/haproxy.log 

# 启动日志服务
[root@localhost src]# systemctl restart rsyslog.service





配置HAproxy Conf：

[root@localhost src]# vim /etc/haproxy/haproxy.cfg
写入以下内容：

# HAProxy 1.7 config for Splash. It assumes Splash instances are executed
# on the same machine and connected to HAProxy using Docker links.
global
    # raise it if necessary
    maxconn 512
    # required for stats page
    stats socket /tmp/haproxy

userlist users
    user user insecure-password userpass

defaults
    log global
    mode http

    # remove requests from a queue when clients disconnect;
    # see https://cbonte.github.io/haproxy-dconv/1.7/configuration.html#4.2-option%20abortonclose
    option abortonclose

    # gzip can save quite a lot of traffic with json, html or base64 data
    # compression algo gzip
    compression type text/html text/plain application/json

    # increase these values if you want to
    # allow longer request queues in HAProxy
    timeout connect 3600s
    timeout client 3600s
    timeout server 3600s


# visit 0.0.0.0:8036 to see HAProxy stats page
listen stats
    bind *:8036
    mode http
    stats enable
    stats hide-version
    stats show-legends
    stats show-desc Splash Cluster
    stats uri /
    stats refresh 10s
    stats realm Haproxy\ Statistics
    stats auth    admin:adminpass


# Splash Cluster configuration
# 代理服务器监听全局的8050端口
frontend http-in
    bind *:8050
    # 如果你需要开启Splash的访问认证
    # 则注释default_backend splash-cluster
    # 并放开其余default_backend splash-cluster 之上的其余注释
    # 账号密码为user  userpass
    # acl auth_ok http_auth(users)
    # http-request auth realm Splash if !auth_ok
    # http-request allow if auth_ok
    # http-request deny

    # acl staticfiles path_beg /_harviewer/
    # acl misc path / /info /_debug /debug

    # use_backend splash-cluster if auth_ok !staticfiles !misc
    # use_backend splash-misc if auth_ok staticfiles
    # use_backend splash-misc if auth_ok misc
    default_backend splash-cluster


backend splash-cluster
    option httpchk GET /
    balance leastconn

    # try another instance when connection is dropped
    retries 2
    option redispatch
    # 将下面IP地址替换为你自己的Splash服务IP和端口
    # 按照以下格式一次增加其余的Splash服务器
    server splash-0 10.10.1.41:8050 check maxconn 5 inter 2s fall 10 observe layer4
    server splash-1 10.10.1.42:8050 check maxconn 5 inter 2s fall 10 observe layer4
    server splash-2 10.10.1.32:8050 check maxconn 5 inter 2s fall 10 observe layer4

backend splash-misc
    balance roundrobin
    # 将下面IP地址替换为你自己的Splash服务IP和端口
    # 按照以下格式一次增加其余的Splash服务器
    server splash-0 10.10.1.41:8050 check fall 15
    server splash-1 10.10.1.42:8050 check fall 15
    server splash-2 10.10.1.32:8050 check fall 15
启动HAproxy：

# 启动HAproxy
[root@localhost src]# /etc/init.d/haproxy start
Restarting haproxy (via systemctl):                        [  OK  ]

# 如果出现错误则使用：
[root@localhost examples]# systemctl status haproxy.service

# 查看报错


查看HAproxy状态：

http://10.10.1.40:8036/haproxy?stats

用户名和密码为： admin  adminpass

查看HAproxy负载是否生效：

http://10.10.1.40:8050

完美！！！收工！！



注意：HAproxy这台服务器没有安装Splash服务，是负载到其余安装有Splash的服务器上提供的服务器哦！