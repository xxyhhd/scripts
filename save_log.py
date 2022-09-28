import logging
import threading


class Log():
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, log_path, level="DEBUG"):
        # 日志器对象
        self.log = logging.getLogger('XX公司')
        self.log.setLevel(level)
        self.log_path = log_path

    def console_handle(self, level="DEBUG"):
        '''控制台处理器'''
        console_handle = logging.StreamHandler()
        console_handle.setLevel(level)
        # 处理器添加格式器
        console_handle.setFormatter(self.get_formatter()[0])
        return console_handle

    def file_handle(self, level="DEBUG"):
        '''文件处理器'''
        file_handler = logging.FileHandler(
            self.log_path, mode="a", encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(self.get_formatter()[1])
        return file_handler

    def get_formatter(self):
        '''格式器'''
        # 定义输出格式
        console_fmt = logging.Formatter(
            fmt="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s", datefmt='%a, %d %b %Y %H:%M:%S')
        file_fmt = logging.Formatter(
            fmt="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s", datefmt='%a, %d %b %Y %H:%M:%S')
        return console_fmt, file_fmt

    def get_log(self):
        if not self.log.handlers:
            # 日志器添加控制台处理器
            self.log.addHandler(self.console_handle())
            # 日志器添加文件处理器
            self.log.addHandler(self.file_handle())
        # 返回日志实例对象
        return self.log
