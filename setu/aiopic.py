from re import A
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
import base64
header = {
  'Referer': 'https://www.pixiv.net',
  }


async def func(session, url):
  fin = bytes()
  print(url)
  proxy = 'http://127.0.0.1:1080'
  async with session.get(url, verify_ssl=False, proxy=proxy) as res:
    print('res ok')
    while True:
      data = await res.content.read(1048576)
      fin = fin + data
      if not data:
        break
    print('finok')
    return fin
  
async def get_pic(url_list):
  async with aiohttp.ClientSession(headers=header) as s:
    done = await func(s, url_list)
    pic = base64.b64encode(done).decode()
    return pic
    
    