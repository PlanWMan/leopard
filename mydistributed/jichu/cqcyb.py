"""
崔庆才 异步请求的教程
主要使用aiohttp框架
"""
import asyncio
import requests
import time


def sjc(func):
    def nh(*args, **kwargs):
        a_ = int(time.time() * 1000)
        a = func(*args, kwargs)
        b_ = int(time.time() * 1000)
        print(b_ - a_)
        return a

    return nh


# 使用aiohttp 异步的请求库
import aiohttp


async def get(url):
    req_session = aiohttp.ClientSession()
    try:
        response = await req_session.get(url)
    except Exception as e:
        print(e)
    # await response.text()
    # await response.close()
    return response


# requests 并不支持异步请求的所以还是顺序执行
async def myrequests(url):
    return requests.get(url, timeout=5)


async def execute():
    url = 'https://static4.scrape.cuiqingcai.com/'
    print("waiting for ", url)
    # await asyncio.sleep(1)
    response = await get(url)
    print('get respoonse from', url, 'response', response)


# def callback(task):
#     print('status:', task.result())


# print('coroutine:', cor)
# print('after calling execute')

# task = loop.create_task(cor)
# task = asyncio.ensure_future(execute())
# # task.add_done_callback(callback)
# print('task:', task)
# loop = asyncio.get_event_loop()
#
# loop.run_until_complete(task)
# print('task:', task)
# print('task result', task.result())


# 多任务协成
@sjc
def aaa(*args, **kwargs):
    tasks = [asyncio.ensure_future(execute()) for i in range(3)]
    # print(tasks)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    # for task in tasks:
    #     print(task.result())


# aiohttp 既提供服务端又提供客户端,在服务端搭建一个异步处理的服务器

async def fetch(session, url):
    async with session.get(url) as response:
        print(response.headers)
        return await response.text(), response.status


async def fetch_post(session, url):
    data = {'m': '1123'}
    url = 'https://httpbin.org/post'
    async with session.post(url, data=data) as response:
        print(response.headers)
        return await response.text(), response.status


async def san():
    async with aiohttp.ClientSession() as session:
        url = 'https://baidu.com'
        html, status = await fetch_post(session, url)
        print(f'html:{html[:100]}')
        print(f'status:{status}')


def aaa_two():
    loop = asyncio.get_event_loop()
    # asyncio.run(san())
    loop.run_until_complete(san())


# 控制aiohttp的并发量
CONCURRENCY = 5
semaphore = asyncio.Semaphore(CONCURRENCY)
session = None


async def scrape_api():
    url = 'https://baidu.com'
    async with semaphore:  # 控制最大并发量
        print('scraping', url)
        async with session.get(url) as response:
            await asyncio.sleep(1)
            print(response.headers)
            return await response.text()


async def aaa_thre():
    global session
    session = aiohttp.ClientSession()
    tasks = [asyncio.ensure_future(scrape_api()) for _in in range(100)]
    # await asyncio.gather(*tasks)
    await asyncio.wait(tasks)  # 和上面的一样


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(aaa_thre())


# aiohttp爬取一个网站

