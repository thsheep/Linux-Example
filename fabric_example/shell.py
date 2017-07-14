from fabric.api import *
from IP import all_server
import os, tarfile


@roles('server')
def upload_files(filename):
    """上传文件
    :return:
    """
    bash_path = os.getcwd()
    bash_path = bash_path + "\shell\\" + filename
    make_targz_one_one(filename, bash_path)
    os.chdir(bash_path)
    run("mkdir /var/script")
    put_name = filename + '.tar.gz'
    put(put_name, '/var/script')
    with cd("/var/script"):
        run('tar -xzvf {}.tar.gz'.format(put_name))


def make_targz_one_one(output_filename, bash_path):
    """打包目录
    :return:
    """
    tar = tarfile.open(output_filename + '.tar.gz', "w:gz")
    for root, dir, files in os.walk(bash_path):
        for file in files:
            fullpath = os.path.join(root, file)
            tar.add(fullpath, arcname=file)
    tar.close()


# @roles('all_server')
def run_shell():
    """执行shell命令 可将命令按照顺序依次写入commands列表中
    :return:
    """
    commands = ['systemctl disable chronyd', "systemctl start ntpd"]
    if isinstance(commands, list):
        for command in commands:
            print(run(command))
    if isinstance(commands, str):
        print(run(commands))


if __name__ == "__main__":

    env.hosts = [
        "root@10.10.1.190:22",
        "root@10.10.1.191:22",
        "root@10.10.1.194:22",
        "root@10.10.1.195:22",
        "root@10.10.1.196:22",
        "root@10.10.1.197:22",
        "root@10.10.1.200:22"
    ]
    env.password = 'toor'
    results = execute(run_shell)
    print(results)