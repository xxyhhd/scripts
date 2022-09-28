import sys
import getopt


def variables():
    action = 'list'
    db_type = 'mysql'
    host = '127'
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "a:b",
                                   ["list=",
                                    "db_type=",
                                    "host="])  # 长选项模式
    except:
        pass

    for opt, arg in opts:
        if opt == '--list':
            action = arg
        elif opt == '--db_type':
            db_type = arg
        elif opt == '--host':
            host = arg

    return ({'action': action, 'db_type': db_type, 'host': host})
