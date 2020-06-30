from loguru import logger
import sys

logger.debug("這是一條debug日誌")
# logger.add("file {time}.log")
# logger.debug("這是一條debug日誌")
# logger.info("這是一條info日誌")
logger.add(sys.stdout, colorize=True,
           format="<c>{time:YYYY-MM-DD at HH:mm:ss}</c> | {level} | <g>{message}</g>",
           filter=__name__,
           level="INFO")

logger.add("company_api.log", retention="3 days", enqueue=True)


logger.debug("这是一条debug日志")
logger.info('可以写日志了')
@logger.catch
def aa():
    try:
        print(1/0)
    except:
        pass
print("aaaa")

print(aa())

