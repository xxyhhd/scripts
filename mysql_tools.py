from re import T
import tools
import os
from time import sleep
from save_log import Log


log = Log('/tmp/test.log')
logger = log.get_log()

def check_mysql(db_port):
    try:
        if tools.tools_run_cmd('ps -ef |grep \'mysql{0}/service\' |grep -v grep'.format(db_port))[0] != '':
            logger.info('检查MySQL-{0}进程是否存在：存在'.format(db_port))
            return 1
        else:
            logger.info('检查MySQL-{0}进程是否存在：不存在'.format(db_port))
            return 2
    except:
        logger.error('检查MySQL-{0}进程是否存在：由于未知错误，检查失败'.format(db_port))
        return False

def start_mysql(db_port):
    check_result = check_mysql(db_port)
    if check_result is False:
        logger.error('请检查代码')
        return False
    if check_result == 1:
        logger.error('MySQL-{0}进程已存在，无法再次拉起'.format(db_port))
        return False
    if check_result == 2:
        start_command = '/home/mysqls/mysql{0}/service/bin/mysqld_safe --defaults-file=/etc/my{0}.cnf &'.format(db_port)
        os.system(start_command)
    sleep(5)
    check_result = check_mysql(db_port)
    if check_result == 1:
        logger.info('MySQL-{0}服务启动：success'.format(db_port))
        return True
    else:
        logger.error('MySQL-{0}服务启动：fail'.format(db_port))
        return False 


def stop_mysql(post, passwd):
    stop_command = '/home/mysqls/mysql{0}/service/bin/mysqladmin -uroot -P{0} -p{1} -h127.0.0.1 shutdown'


# check_mysql(3307)