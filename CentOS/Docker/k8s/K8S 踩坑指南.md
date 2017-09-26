K8S 踩坑指南

kube-apiserver报错： Unable to find suitable network address.error='Unable to select an IP.' . Try to set the AdvertiseAddress directly or provide a valid BindAddress to fix this

解决办法： 是默认网关没有配置的问题，比如默认网关是192.168.0.1 在命令行上添加默认网关:route add default gw  192.168.0.1确认网关已经配置好后，再一次启动apiserver（可以使用route -n查看默认网关是否已经配置好了）