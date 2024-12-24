import os
import sys
import datetime
import logging
import colorlog
from logging.handlers import RotatingFileHandler


def create_logger(
    logger_name: str,
    log_file: str = "",
    level: int = logging.DEBUG,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
):
    """
    创建并配置一个logger对象，并设置带颜色的输出格式。

    :param logger_name: Logger的名称
    :param log_file: 日志文件的路径
    :param level: 日志级别，默认为DEBUG
    :param max_bytes: 日志文件的最大大小，默认为10MB
    :param backup_count: 保留的日志文件备份数量，默认为5
    :return: 配置好的logger对象
    """
    # 创建logger对象
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    main_path = "/".join(
        os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").split("/")[:-1]
    )
    if not log_file:
        log_file = (
            f"{main_path}/logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
        )
    if not os.path.exists(f"{main_path}/logs"):
        os.makedirs(f"{main_path}/logs")
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("")
    # 创建文件处理器并设置格式
    if not os.path.exists("../logs"):
        os.makedirs("../logs")
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("")
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setLevel(level)
    file_format = (
        "%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    )
    file_formatter = logging.Formatter(file_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 创建控制台处理器并设置带颜色的格式
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    # 注意：colorlog的颜色名称是有限的，这里使用最接近的颜色
    custom_format = (
        "%(log_color)s%(asctime)s [%(levelname)s"
        "]%(reset)s [%(name)s] [%(filename)s:%(lineno)d] => %(message)s"
    )
    log_colors = {
        "DEBUG": "cyan",  # 接近天蓝色，但用cyan代替
        "INFO": "blue",  # 更接近标准的蓝色，而不是天蓝色
        "WARNING": "yellow",  # 黄色
        "ERROR": "magenta",  # 粉红色，虽然不完全是，但最接近的标准颜色
        "CRITICAL": "red",  # 红色，也称为血红色
    }
    logger_formatter = colorlog.ColoredFormatter(
        custom_format,
        log_colors=log_colors,
        reset=True,
        style="%",
    )
    console_handler.setFormatter(logger_formatter)
    logger.addHandler(console_handler)

    return logger


# 示例使用
if __name__ == "__main__":
    logger = create_logger("my_logger", "my_log_file.log")
    logger.debug(
        f"debug是cyan色，说明是调试的，代码ok "
    )  # 注意：这里的{log_colors["DEBUG"]}不会实际替换颜色，只是说明
    logger.info(
        "info是蓝色，日志正常 "
    )  # 注意：这里的“蓝色”是文字说明，实际颜色由log_colors设置
    logger.warning("黄色yello，有警告了 ")
    logger.error("粉红色说明代码有错误 ")
    logger.critical("血红色，说明发生了严重错误 ")
