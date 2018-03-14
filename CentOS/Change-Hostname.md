在CentOS 7中，有个叫hostnamectl的命令行工具，它允许你查看或修改与主机名相关的配置。

1.要查看主机名相关的设置：
[root@localhost ~]# hostnamectl  
  Static hostname: localhost.localdomain
        Icon name: computer
          Chassis: n/a
        Machine ID: 80a4fa4970614cf6be9597ecd6f097a9
          Boot ID: 28420e272e1847a583718262758bd0f7
    Virtualization: vmware
  Operating System: CentOS Linux 7 (Core)
      CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-123.el7.x86_64
      Architecture: x86_64
或

[root@localhost ~]# hostnamectl status
  Static hostname: localhost.localdomain
        Icon name: computer
          Chassis: n/a
        Machine ID: 80a4fa4970614cf6be9597ecd6f097a9
          Boot ID: 28420e272e1847a583718262758bd0f7
    Virtualization: vmware
  Operating System: CentOS Linux 7 (Core)
      CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-123.el7.x86_64
      Architecture: x86_64

2.只查看静态、瞬态或灵活主机名，分别使用“--static”，“--transient”或“--pretty”选项。
[root@localhost ~]# hostnamectl --static
localhost.localdomain
[root@localhost ~]# hostnamectl --transient
localhost.localdomain
[root@localhost ~]# hostnamectl --pretty

3.要同时修改所有三个主机名：静态、瞬态和灵活主机名：
[root@localhost ~]# hostnamectl set-hostname Linuxidc
[root@localhost ~]# hostnamectl --pretty
Linuxidc
[root@localhost ~]# hostnamectl --static
Linuxidc
[root@localhost ~]# hostnamectl --transient
Linuxidc


就像上面展示的那样，在修改静态/瞬态主机名时，任何特殊字符或空白字符会被移除，而提供的参数中的任何大写字母会自动转化为小写。一旦修改了静态主机名，/etc/hostname 将被自动更新。然而，/etc/hosts 不会更新以保存所做的修改，所以你每次在修改主机名后一定要手动更新/etc/hosts，之后再重启CentOS 7。否则系统再启动时会很慢。

4.手动更新/etc/hosts

vim /etc/hosts

127.0.0.1      Linuxidc  hunk_zhu
#127.0.0.1  localhost localhost.localdomain localhost4 localhost4.localdomain
::1        localhost localhost.localdomain localhost6 localhost6.localdomai

5.重启CentOS 7 之后（reboot -f ），
[root@Linuxidc ~]# hostname
Linuxidc
[root@hunk_zhu ~]# hostnamectl --transient 
Linuxidc
[root@hunk_zhu ~]# hostnamectl --static
Linuxidc
[root@hunk_zhu ~]# hostnamectl --pretty
Linuxidc

6.如果你只想修改特定的主机名（静态，瞬态或灵活），你可以使用“--static”，“--transient”或“--pretty”选项。
例如，要永久修改主机名，你可以修改静态主机名：
[root@localhost ~]# hostnamectl --static set-hostname Linuxidc
重启CentOS 7 之后（reboot -f ），
[root@Linuxidc ~]# hostnamectl --static
Linuxidc
[root@Hunk_zhu ~]# hostnamectl --transient
Linuxidc
[root@Hunk_zhu ~]# hostnamectl --pretty
Linuxidc
[root@Hunk_zhu ~]# hostname