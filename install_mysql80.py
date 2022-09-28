from cmath import log
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


db_port = 3307
base_path = '/home/mysqls/'
version_path = base_path+'versions/'
paths = {'binlog_path': '{0}mysql{1}/binlog'.format(base_path, db_port), 'data_path': '{0}mysql{1}/data'.format(base_path, db_port),
         'log_path': '{0}mysql{1}/log'.format(base_path, db_port), 'undo_path': '{0}mysql{1}/undo'.format(base_path, db_port), 'slowlog_path': '{0}mysql{1}/slowlog'.format(base_path, db_port)}
cnf_path = '/etc/my{0}.cnf'.format(db_port)
plugin_str = '''
plugin_load = "rpl_semi_sync_master=semisync_master.so;rpl_semi_sync_slave=semisync_slave.so"
rpl_semi_sync_master_enabled = 1  
rpl_semi_sync_master_timeout = 3000  
rpl_semi_sync_slave_enabled = 1   
'''

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
        tools.tools_run_cmd(
            '{0}mysql{1}/service/bin/mysqld --defaults-file=/etc/my{1}.cnf --initialize-insecure'.format(base_path, db_port))
        if tools.tools_run_cmd('grep \'root@localhost is created with an empty password\' {0}mysql{1}/log/mysql.log'.format(base_path, db_port))[0] is not None:
            logger.info('初始化成功！！！')
            return True
        logger.error('初始化：fail')
        return False
    except:
        logger.error('初始化：fail')
        return False


def modify_passwd():
    os.system('/home/mysqls/mysql{0}/service/bin/mysql -uroot  -S /tmp/mysql{0}.sock -e \"alter user user() identified by \'123456\';update mysql.user set host = \'%\' where user = \'root\';flush privileges;\" --connect-expired-password'.format(db_port))
    logger.info('修改root账号密码')

def create_repl_account(passwd):
    os.system('/home/mysqls/mysql{0}/service/bin/mysql -uroot -p\'{1}\' -S /tmp/mysql{0}.sock -e \"create user \'repl\'@\'%\' identified by \'{2}\'; grant replication slave on *.* to \'repl\';flush privileges;\"'.format(db_port, '123456', passwd))
    logger.info('创建主备复制账号')

def rebuild_cnf_file():
    try:
        with open(cnf_path, 'a') as f:
            f.write(plugin_str)
        logger.info('配置文件修改成功')
        return True
    except:
        logger.error('配置文件修改失败')
        return False



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
    rebuild_cnf_file()
    if mysql_tools.start_mysql(db_port) is False:
        logger.error('MySQL安装失败！！！')
        return False
    sleep(10)
    modify_passwd()
    create_repl_account('replicator')
    logger.info('MySQL安装成功')
