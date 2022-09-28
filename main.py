from build_command import build_command
import ops_host
from save_log import Log
import re
import install_mysql57 as install_mysql57
import install_mysql56
import install_mysql80


log = Log('/tmp/test.log')
logger = log.get_log()
pattern_ipv4 = re.compile(
    r'^(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9])) .+')


def main():
    my_command = build_command()
    if (my_command.action == 'add_host' and pattern_ipv4.search(my_command.host_info) is not None) or (my_command.action == 'del_host' and my_command.host_info is not None) or (my_command.action == 'sync_host' and my_command.host_info is None):
        ops_host.run(my_command.action,
                    my_command.host_info)
        return True

    if my_command.action == 'create_db' and my_command.db_type == 'mysql' and my_command.db_version is not None:
        if my_command.db_version < '5.7':
            install_mysql56.run(str(my_command.db_version))
        elif my_command.db_version < '5.8':
            install_mysql57.run(str(my_command.db_version))
        else:
            install_mysql80.run(str(my_command.db_version))
        return True  
    else:
        return False


if __name__ == '__main__':
    main()
