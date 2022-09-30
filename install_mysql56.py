from cmath import log
from mimetypes import init
import mysql_tools as mysql_tools
import os
import subprocess
from time import sleep
from save_log import Log
from temp_cnf import temp_cnf
import random
import tools
from save_log import Log

log_1 = Log('/tmp/test.log')
logger = log_1.get_log()


db_port = 3306
base_path = '/home/mysqls/'
version_path = base_path+'versions/'
paths = {'binlog_path': '{0}mysql{1}/binlog'.format(base_path, db_port), 'data_path': '{0}mysql{1}/data'.format(base_path, db_port),
         'log_path': '{0}mysql{1}/log'.format(base_path, db_port), 'undo_path': '{0}mysql{1}/undo'.format(base_path, db_port), 'slowlog_path': '{0}mysql{1}/slowlog'.format(base_path, db_port)}
cnf_path = '/etc/my{0}.cnf'.format(db_port)


def mkdirs():
    try:
        for path in paths.values():
            mkdir_result = tools.tools_mkdir(path)
            if mkdir_result is False:
                return False
        open('{0}mysql{1}/log/mysql.log'.format(base_path, db_port), 'a').close()
        logger.info('创建mysql.log日志文件成功')
        return True
    except:
        logger.error('由于未知原因，工作目录创建失败')
        return False


def build_ln(db_version):
    version_list = []
    try:
        for version in os.listdir(version_path):
            if str(db_version) in version:
                version_list.append(version)
        os.symlink(version_path+max(version_list),
                   '{0}mysql{1}/service'.format(base_path, db_port))
        logger.info('软链接创建成功')
        return True
    except:
        logger.error('软链接创建失败')
        return False


def build_cnf_file():
    try:
        with open(cnf_path, 'w') as f:
            f.write(temp_cnf.format(base_path, db_port, random.randint(1, 10000)))
        logger.info('配置文件创建成功')
        return True
    except:
        logger.error('配置文件创建失败')
        return False


def change_files_owner_priv():
    if os.system('chown -R mysql.mysql  {0}mysql{1}/'.format(base_path, db_port)) != 0:
        logger.error('修改文件属组失败')
        return False
    logger.info('修改文件属组成功')
    if os.system('chmod -R 755  {0}mysql{1}/'.format(base_path, db_port)) != 0:
        logger.error('修改文件权限失败')
        return False
    logger.info('修改文件权限成功')
    return True


def init_mysql():
    logger.info('开始初始化')
    try:

        init_command = '{0}mysql{1}/service/scripts/mysql_install_db --defaults-file=/etc/my{1}.cnf --basedir={0}mysql{1}/service/ --datadir={0}mysql{1}/data/ --user=mysql'.format(base_path, db_port)

        tools.tools_run_cmd(init_command)
        logger.info('初始化：success')
        return True
    except:
        logger.error('初始化：fail')
        return False


def modify_passwd():
    os.system('/home/mysqls/mysql{0}/service/bin/mysql -uroot -S /tmp/mysql{0}.sock -P{0} -e \"update mysql.user set password = PASSWORD(\'123456\') where user = \'root\';flush privileges;\"'.format(db_port))
    logger.info('修改root账号密码')

def create_repl_account(passwd):
    os.system('/home/mysqls/mysql{0}/service/bin/mysql -uroot -p\'{1}\' -S /tmp/mysql{0}.sock -e \"grant replication slave on *.* to \'repl\'@\'%\' identified by \'{2}\';flush privileges;\"'.format(db_port, '123456', passwd))
    logger.info('创建主备复制账号')


def run(db_version):
    if mkdirs() is False:
        logger.error('MySQL安装失败！！！')
        return False
    if build_ln(db_version) is False:
        logger.error('MySQL安装失败！！！')
        return False
    if build_cnf_file() is False:
        logger.error('MySQL安装失败！！！')
        return False
    if change_files_owner_priv() is False:
        logger.error('MySQL安装失败！！！')
        return False
    # return True
    if init_mysql() is False:
        logger.error('MySQL安装失败！！！')
        return False
    if mysql_tools.start_mysql(db_port) is False:
        logger.error('MySQL安装失败！！！')
        return False
    modify_passwd()
    create_repl_account('replicator')
    logger.info('MySQL安装成功')
