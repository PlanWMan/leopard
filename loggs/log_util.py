import sys
import os

log_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

from loguru import logger

logger.add(sys.stdout, colorize=True, format="<c>{time:YYYY-MM-DD at HH:mm:ss}</c> | {level} | <g>{message}</g>")
logger.add(f'{log_path}/logs/company.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
           enqueue=True, retention="3 days", backtrace=True, diagnose=True)


# 主要用于本地调试，替换print
class DevLogUtil:
    @staticmethod
    def info(msg, tag=None):
        if tag:
            logger.info("{} | {}".format(tag, msg))
        else:
            logger.info(str(msg))

    @staticmethod
    def debug(msg, tag=None):
        if tag:
            logger.debug("{} | {}".format(tag, msg))
        else:
            logger.debug(msg)

    @staticmethod
    def warning(msg, tag=None):
        if tag:
            logger.warning("{} | {}".format(tag, msg))
        else:
            logger.warning(msg)
