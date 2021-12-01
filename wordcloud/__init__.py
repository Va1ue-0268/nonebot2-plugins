import os
import nonebot
import json
from nonebot import on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent,MessageEvent, PokeNotifyEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State
from wordcloud import WordCloud
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import base64

gpath = '/home/qqbot/plugindata/wordcloud'
path = gpath +'/data.json'
font = gpath + '/SourceHanSansHWSC-Regular.otf'
mask = np.array(Image.open(gpath + '/mask.png'))


data = {} #语料数据

def union(gid, uid):
    return str((gid << 32) | uid)
# 读取数据文件
try:
    with open(path) as f:
        data = json.load(f)
    with open(gpath +'/filter.json') as f:
        filter_list = json.load(f)['f']
except:
    pass

def save_json(values:str, id:str):
    '''
    写数据到json
    '''
    global data
    if id not in data:
        data[id] = {}
    if values not in data[id]:
        data[id].setdefault(values,1)
    elif values in data[id]:
        num = data[id][values]
        data[id][values] = num + 1
    with open(path, 'w+') as f :
        tojson = json.dumps(data,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
        f.write(tojson)

chat = on_message(priority=99)
@chat.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):
    message = str(event.raw_message)
    group_id = event.group_id
    user_id = event.user_id
    if '[CQ' in message:
        return
    save_json(message, union(group_id, 1))

generator = on_command('生成词云',aliases={"词云"})
@generator.handle()
async def generator_handle(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    id = union(group_id, 1)
    text = ''
    for i in data[id]:
        t = data[id][i]
        while t > 0:
            text = text + i + ' '
            t -= 1
    print(text)
    img = WordCloud(background_color='white',mask=mask,font_path=font).generate(text)
    img = WordCloud.to_image(img)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    pic = base64.b64encode(buffer.getvalue()).decode()
    await bot.send(event,message=MessageSegment.image(f'base64://{pic}'))