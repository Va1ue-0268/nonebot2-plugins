from nonebot import on_command, get_driver, on_notice
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, PokeNotifyEvent, Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State
from .data_source import generate_gif
import re
import requests
from PIL import Image
from io import BytesIO


try:
    master = get_driver().config.master
except:
    master = []

data_dir = get_driver().config.plugin_data + 'rua/data/'
img_src = 'rua/data/output.gif'
img = MessageSegment.image(f'file://{img_src}')


rua_me = on_notice()
'''
戳一戳事件
'''      
@rua_me.handle()
async def _t3(bot: Bot, event: PokeNotifyEvent):

    if event.target_id in master:
        creep_id = event.sender_id
    else: creep_id = event.target_id
    url = f'http://q1.qlogo.cn/g?b=qq&nk={creep_id}&s=160'
    resp = requests.get(url)
    resp_cont = resp.content
    avatar = Image.open(BytesIO(resp_cont))
    #<class 'PIL.JpegImagePlugin.JpegImageFile'>
    generate_gif(data_dir, avatar)
    await bot.send(event, message=img)


    
rua = on_command('rua')
@rua.handle()
async def rua_handle(bot: Bot, event: Event, state: T_State):

    try:
        msg = (str(event.raw_message).split('rua')[1].strip())
        if ':image' in msg:         
            state['url'] = (msg.split('url=')[-1][:-2])     
        elif msg.isdigit():
            id = int(msg)
            state['url'] = f'http://q1.qlogo.cn/g?b=qq&nk={id}&s=160'
    except:
        pass


@rua.got("url", prompt="要rua点什么～")
async def rua_got(bot: Bot, event: Event, state: T_State):
    msg = str(state['url'])
    state['url'] = (msg.split('url=')[-1][:-2])
    resp = requests.get(state['url'])
    resp_cont = resp.content
    try:
        avatar = Image.open(BytesIO(resp_cont))
        generate_gif(data_dir, avatar)
        await bot.send(event, message=img)
    except:
        
        await rua.finish('失败了..')

'''
三三酱的api平台
http://lkaa.top
'''
    
pa = on_command('爬')
@pa.handle()
async def pa_handle(bot:Bot, event: MessageEvent):
    try:
        qq = int(re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", str(event.message)).group(1))
        if qq in master:
            qq = event.user_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://lkaa.top/API/pa/api.php?QQ={qq}]"))
    except:
        pass

si = on_command('撕了')
@si.handle()
async def si_handle(bot:Bot, event: MessageEvent):
    try:
        qq = int(re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", str(event.message)).group(1))
        if qq in master:
            qq = event.user_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://lkaa.top/API/si/?QQ={qq}]"))
    except:
        pass

chi = on_command('吃了')
@chi.handle()
async def chi_handle(bot:Bot, event: MessageEvent):
    try:
        qq = int(re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", str(event.message)).group(1))
        if qq in master:
            qq = event.user_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://lkaa.top/API/chi/?QQ={qq}]"))
    except:
        pass

diu = on_command('去吧')
@diu.handle()
async def diu_handle(bot:Bot, event: MessageEvent):
    try:
        qq = int(re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", str(event.message)).group(1))
        if qq in master:
            qq = event.user_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://lkaa.top/API/diu/api.php?QQ={qq}]"))
    except:
        pass

jupai = on_command('举牌')
@jupai.handle()
async def jupai_handle(bot:Bot, event: MessageEvent):
    try:
        await bot.send(event, message = Message(f"[CQ:image,file=http://lkaa.top/API/pai/?msg={event.message}]"))
    except:
        pass

