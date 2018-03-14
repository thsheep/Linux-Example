Redis备份以及恢复：

redis_backup.sh 脚本为备份dump.rdb文件

每隔两个两个小时备份一次 目录为/var/cp_redis_backup/ （PS：只会有最新一次备份）

恢复方法：
		将从机上备份目录中的备份文件重命名为dump.rdb拷贝到master机上的目录（具体目录查看：redis-cli config get dir）
		重启master机服务即可。