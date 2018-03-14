FROM daocloud.io/centos:7
MAINTAINER Gtao@you_tell.me
COPY jdk-8u131-linux-x64.rpm /var/tmp/jdk-8u131-linux-x64.rpm
RUN rpm -ivh /var/tmp/jdk-8u131-linux-x64.rpm
CMD ["java", "-version"]