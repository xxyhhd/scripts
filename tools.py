import os
import subprocess
from time import sleep
from save_log import Log


log = Log('/tmp/test.log')
logger = log.get_log()


def tools_mkdir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info('创建目录{}：success'.format(path))
            return True
        else:
            logger.error('由于目录已存在，创建目录{}：fail'.format(path))
            return False
    except:
        logger.error('由于未知原因，创建目录{}：fail'.format(path))
        return False


def tools_run_cmd(command):
    try:
        ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding="utf-8", timeout=300)
        logger.info('命令执行成功')
        return((ret.stdout, ret.stderr))
    except:
        logger.error('命令执行失败')
        return False

  