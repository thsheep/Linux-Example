启动、停止、查看日志

docker  start java210
docker  stop java210
docker logs redis205

进入容器：docker exec -it redis205 bash（netstat -tunpl）
批量操作：


docker images | grep none | awk '{print $3}'|xargs docker rmi
docker ps -a | grep war|awk '{print $1}'|xargs docker rm

查看网络：docker network ls

查看容器配置：docker inspect redis201



镜像类
docker build --rm=true . 构建镜像
docker pull ${IMAGE} 安装镜像
docker images 显示已经安装的镜像
docker images --no-trunc 显示已经安装镜像的详细内容
docker rmi ${IMAGE_ID} 删除指定镜像
docker rmi $(docker images | grep “^” | awk “{print $3}”) 删除所有没有标签的镜像
docker rm $(docker ps -aq) 删除所有的镜像
docker rmi $(docker images --quiet --filter &quot;dangling=true&quot;) 删除未使用的镜像
容器类
docker run 运行容器
docker ps 显示正在运行的容器
docker ps -a 显示所有的容器
docker stop ${CID} 停止指定容器
docker stop docker ps -q 停止所有正在运行的容器
docker ps -a --filter &quot;exited=1&quot; 显示所有退出状态为1的容器
docker rm ${CID} 删除指定容器
docker ps -a | grep wildfly | awk '{print $1}' | xargs docker rm -f 使用正则表达式删除容器
docker rm -f $(docker ps -a | grep Exit | awk '{ print $1 }') 删除所有退出的容器
docker rm $(docker ps -aq) 删除所有的容器
docker inspect --format '{{ .NetworkSettings.IPAddress }}' ${CID} 显示指定容器的IP
docker attach ${CID} 进入容器
docker exec -it ${CID} bash 进入容器打开一个shell
docker ps | grep wildfly | awk '{print $1}' 通过正则表达式查找容器的镜像ID




使用阿里云镜像安装Docker：


# step 1: 安装必要的一些系统工具
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
# Step 2: 添加软件源信息
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# Step 3: 更新并安装 Docker-CE
sudo yum makecache fast
sudo yum -y install docker-ce
# Step 4: 开启Docker服务
sudo service docker start

# 安装指定版本的Docker-CE:
# Step 1: 查找Docker-CE的版本:
# yum list docker-ce.x86_64 --showduplicates | sort -r
#   Loading mirror speeds from cached hostfile
#   Loaded plugins: branch, fastestmirror, langpacks
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            docker-ce-stable
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            @docker-ce-stable
#   docker-ce.x86_64            17.03.0.ce-1.el7.centos            docker-ce-stable
#   Available Packages
# Step2 : 安装指定版本的Docker-CE: (VERSION 例如上面的 17.03.0.ce.1-1.el7.centos)
# sudo yum -y install docker-ce-[VERSION]