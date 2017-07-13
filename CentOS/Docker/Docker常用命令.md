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