import aiohttp
import asyncio

CONCURRENCY = 5
semaphore = asyncio.Semaphore(CONCURRENCY)
session = None
async def aaa():
    async with session.get('https://baidu.com') as response:
        print(response.headers)
        print(response.text())
        return await response.text()

async def scrape_api():
    url = 'https://baidu.com'
    async with semaphore:  # 控制最大并发量
        print('scraping', url)
        async with session.get(url) as response:
            await asyncio.sleep(1)
            print(response.headers)
            return await response.text()

async def main():
    global session
    session = aiohttp.ClientSession()
    tasks = [asyncio.ensure_future(aaa()) for i in range(3)]
    await asyncio.wait(tasks)
    # await session.close()
    for i in tasks:
        print(i)

# async def aaa_thre():
#     global session
#     session = aiohttp.ClientSession()
#     tasks = [asyncio.ensure_future(scrape_api()) for _in in range(100)]
#     # await asyncio.gather(*tasks)
#     await asyncio.wait(tasks)

def ddd():
    asyncio.get_event_loop().run_until_complete(main())

if __name__ == '__main__':
    ddd()
