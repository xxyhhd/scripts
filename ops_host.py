import subprocess
import sys
from save_log import Log


log = Log('/tmp/test.log')
logger = log.get_log()


path = '/etc/hosts'

def copy_host():
    with open(path, 'r', encoding='utf-8') as f1:
        for line in f1:
            scp_command = "scp -r {0} root@{1}:{0}".format(
                path, line.split(' ')[1].strip())
            cmd(scp_command)


def cmd(command):
    try:
        subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, encoding="utf-8")
        return True
    except:
        return False


def run(action, info_host=None):
    if action == 'add_host':
        cmd("echo {0} >> {1}".format(info_host, path))
        copy_host()
        logger.info('hosts信息添加成功')
    elif action == 'del_host':
        cmd("sed -i \'/{0}/d\' {1}".format(info_host, path))
        copy_host()
        logger.info('hosts信息删除成功')
    elif action == 'sync_host':
        copy_host()
        logger.info('hosts信息复制成功')
    else:
        logger.error('hosts信息操作失败')
        return False
    return True

