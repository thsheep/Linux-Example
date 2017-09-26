docker ps -a | grep Exited | awk '{print $1}' | xargs docker rm

Exited 可为其它选项 比如 TAG  

rm 可为其它选项 比如 start