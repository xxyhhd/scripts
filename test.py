import argparse


def build_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', type=str, dest='action', choices=['create_db', 'start_db', 'stop_db', 'restart_db',
                        'rebuild_slave', 'list_db', 'delete_db', 'check_db', 'add_host', 'del_host', 'sync_host'], help='请选择你要执行的命令')
    parser.add_argument('--db_type', type=str, dest='db_type',
                        choices=['mysql', 'pg', 'redis'], help='选择数据库类型')
    parser.add_argument('--db_version', type=str,
                        dest='db_version', help='选择数据库版本')
    parser.add_argument('--db_name', type=str, dest='db_name', help='选择实例名')
    parser.add_argument('--host_info', type=str, dest='host_info',
                        help='填写需要添加或者删除的主机信息：127.0.0.1 localhost')
    parser = parser.parse_args()
    return parser


print(build_command().action)
