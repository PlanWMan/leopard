"""
使用asyncio实现异步io
从asyncio模块中直接获取一个eventLoop的引用，然后需要执行的协成搞到eventloop中执行就能实现异步
"""

import asyncio, threading
import time

# @asyncio.coroutine
# def hello():
#     print('Hello world! (%s)' % threading.currentThread())
#     yield from asyncio.sleep(1)
#     print('Hello again! (%s)' % threading.currentThread())
#
# # 获取loop
# loop = asyncio.get_event_loop()
# # 执行coroutine
# tasks = [hello(), hello()]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()

# 进阶版 async和await
# async def hello():
#     print("hello world")
#     r = await asyncio.sleep(1)
#     print("Hello again!")

# 使用asyncio的一波网络来连接获取sina，sohu，和163
# @asyncio.coroutine
# def wget(host):
#     print('wget %s' % host)
#     connect = asyncio.open_connection(host, 80)
#     reader, writer = yield from connect
#     header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
#     writer.write(header.encode('utf-8'))
#     yield from writer.drain()
#     while True:
#         line = yield from reader.readline()
#         if line == b'\r\n':
#             break
#         print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
#         # Ignore the body, close the socket
#     writer.close()
# loop = asyncio.get_event_loop()
# tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()

# 高阶班使用aiohttp 单线程+coroutine可以实现多用户的高并发支持
# aiohttp是基于asyncio是实现的http框架
# 编写一个http服务器
import asyncio
from aiohttp import web
async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
