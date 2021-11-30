from re import A
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
import base64

async def func(session, url):
  fin = bytes()
  print(url)
  proxy = 'http://127.0.0.1:1080'
  #分块存入数据
  async with session.get(url, verify_ssl=False) as res:
    print('res ok')
    while True:
      data = await res.content.read(1048576)
      fin = fin + data
      if not data:
        break
    print('finok')
    return fin

async def get_pic(url, name):
  async with aiohttp.ClientSession() as s:
    done = await func(s, url)
    #转换成base64发送
    pic = open(name, "wb")
    pic.write(done)
    return name
    