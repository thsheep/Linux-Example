# SSH（Secure Shell）介绍



## SSH 安装

- 查看是否已安装：
 - CentOS：`rpm -qa | grep openssh`
 - Ubuntu：`dpkg -l | grep openssh`

- 安装：
 - CentOS 6：`sudo yum install -y openssh-server openssh-clients`
 - Ubuntu：`sudo apt-get install -y openssh-server openssh-client`


## SSH 修改连接端口

- 配置文件介绍（记得先备份）：`sudo vim /etc/ssh/sshd_config`
- 打开这一行注释：Port 22
	- 自定义端口选择建议在万位的端口，如：10000-65535之间，假设这里我改为 60001
- 给新端口加到防火墙中：
    - 添加规则：`iptables -I INPUT -p tcp -m tcp --dport 60001 -j ACCEPT`
    - 保存规则：`service iptables save`
    - 重启 iptables：`service iptables restart`

## 设置超时

- ClientAliveInterval指定了服务器端向客户端请求消息的时间间隔, 默认是0，不发送。而ClientAliveInterval 300表示5分钟发送一次，然后客户端响应，这样就保持长连接了。
- ClientAliveCountMax，默认值3。ClientAliveCountMax表示服务器发出请求后客户端没有响应的次数达到一定值，就自动断开，正常情况下，客户端不会不响应。
- 正常我们可以设置为：
	- ClientAliveInterval 300
	- ClientAliveCountMax 3
	- 按上面的配置的话，300*3＝900秒＝15分钟，即15分钟客户端不响应时，ssh连接会自动退出。

## SSH 允许 root 账户登录

- 编辑配置文件（记得先备份）：`sudo vim /etc/ssh/sshd_config`
 - 允许 root 账号登录
    - 注释掉：`PermitRootLogin without-password`
    - 新增一行：`PermitRootLogin yes`

## SSH 不允许 root 账户登录

- 新增用户和把新增的用户改为跟 root 同等权限方法：[Bash.md]
- 编辑配置文件（记得先备份）：`sudo vim /etc/ssh/sshd_config`
    - 注释掉这一句（如果没有这一句则不管它）：`PermitRootLogin yes`

## SSH 密钥登录

- 生成秘钥和公钥文件，命令：`sudo ssh-keygen`，在交互提示中连续按三次回车，如果看得懂交互的表达，那就根据你自己需求来。默认生成密钥和公钥文件是在：/root/.ssh。
- 进入生成目录：`cd /root/.ssh`，可以看到有两个文件：id_rsa (私钥) 和 id_rsa.pub (公钥)
- 在 .ssh 目录下创建 SSH 认证文件，命令：`touch /root/.ssh/authorized_keys`
- 将公钥内容写到SSH认证文件里面，命令：`cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys`
- 修改SSH认证文件权限，命令：
   - `sudo chmod 700 /root/.ssh`
   - `sudo chmod 600 /root/.ssh/authorized_keys`
- 重启服务：`sudo service sshd restart`
- 设置 SSH 服务默认启动：`sudo sysv-rc-conf ssh on`
- 现在 SSH 客户端可以去拿着 SSH 服务器端上的 id_rsa，在客户端指定秘钥文件地址即可，这个一般由于你使用的客户端决定的，我这里推荐的是 Xshell 软件。

## 限制只有某一个IP才能远程登录服务器

- 在该配置文件：`vim /etc/hosts.deny`
	- 添加该内容：`sshd:ALL`
- 在该配置文件：`vim /etc/hosts.allow`
	- 添加该内容：`sshd:123.23.1.23`

## 限制某些用户可以 SSH 访问

- 在该配置文件：`vim /etc/ssh/sshd_config`
	- 添加该内容：`AllowUsers root userName1 userName2`

## 修改完配置都要记得重启服务

- 命令：`service sshd restart`

## 常用 SSH 连接终端

- Windows -- Xshell：<http://www.youmeek.com/ssh-terminal-emulator-recommend-xshell-and-xftp/>
- Mac -- ZOC：<http://xclient.info/s/zoc-terminal.html>

## SSH 资料

- <http://www.jikexueyuan.com/course/861_1.html?ss=1> 
- <http://www.361way.com/ssh-autologout/4679.html> 
- <http://www.osyunwei.com/archives/672.html> 



SSH是我们登录VPS常用的方式，因此SSH账号的安全至关重要。常见的用户名+密码的登录方式很容易受到暴力破解的影响，为了避免影响，我们可以直接禁止用户名+密码登录VPS的方式，改用密钥登录，既保证了安全，又方便快捷。下面就介绍一下配置ssh key登录的方法。

一、PuttyGen以及Putty软件的下载
这一步看似简单，其实有着至关重要的作用。大家一定要到官方网站进行下载（putty官网可能被墙,请科学上网），一些中文版及不安全链接下载的软件可能会存有后门，带来极大的安全隐患。
我们需要下载的是putty.exe和puttygen.exe两个程序


二、密钥的生成
首先利用用户名+密码登录VPS，在终端中利用以下命令生成RSA密钥
[plain] view plain copy
ssh-keygen -t rsa  

生成密钥时选择默认位置即可，同时可以选择为密钥增加密码（设置密码后，使用密钥时还需要输入密码）
进入密钥生成的目录，可以看见两个文件id_rsa和id_rsa.pub，将这两个文件下载下来，保存好为后面做准备。

在密钥生成的目录中将其重命名，并且设置权限
[plain] view plain copy
mv id_rsa.pub authorized_keys  
chmod 600 authorized_keys  

编辑sshd_config，将RSAAuthentication和PubkeyAuthentication两行前面的 # 去掉
[plain] view plain copy
vi /etc/ssh/sshd_config  


为了安全还可以修改默认的SSH端口，找到#port 22，去掉前面的#，然后修改port后的数字。

保存后重启SSHD服务(CentOS7中为systemctl restart sshd.service)
[plain] view plain copy
/etc/init.d/sshd restart  

注：CentOS7中的firewall配置
firewall中默认ssh端口为22，在修改端口后需要对其进行设置才能正常登录
复制 firewalld 有关 sshd 的配置文件：
[plain] view plain copy
cp /usr/lib/firewalld/services/ssh.xml /etc/firewalld/services/  
[plain] view plain copy
vi /etc/firewalld/services/ssh.xml  
修改<port protocol="tcp" port="22"/>将“22”改为所需的端口
保存后重载sshd服务
[plain] view plain copy
firewall-cmd --reload  



拷贝秘钥和shhd_config 到其他服务器

ssh-copy-id -i /root/.ssh/id_rsa.pub 10.10.1.41   会提示输入密码

scp /etc/ssh/sshd_config 10.10.1.41:/etc/ssh/