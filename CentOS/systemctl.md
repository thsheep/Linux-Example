启动一个服务：systemctl start postfix.service
关闭一个服务：systemctl stop postfix.service
重启一个服务：systemctl restart postfix.service
显示一个服务的状态：systemctl status postfix.service
在开机时启用一个服务：systemctl enable postfix.service
在开机时禁用一个服务：systemctl disable postfix.service
查看服务是否开机启动：systemctl is-enabled postfix.service;echo $?
查看已启动的服务列表：systemctl list-unit-files|grep enabled