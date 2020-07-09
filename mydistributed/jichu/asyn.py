"""
对异步的学习
"""
import asyncio
import time

# 协成执行并发操作
async def say_after(delay, what):
    print(what)
    await asyncio.sleep(delay)
    print(delay)


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'word'))
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")


# asyncio.run(main())
# await 后面必须是可等待对象(协成， 任务，future)
# create_task 会将协成打包成一个task排入日程
# get_running_loop 会循环执行协成

import datetime
async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(display_date())
