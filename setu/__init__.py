from posixpath import expanduser
import threading
import re
from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

from nonebot.typing import T_State
import os
import sys
import requests
import random
sys.path.append(os.path.join(os.path.dirname(__file__)))
import Getpic
from aiopic import get_pic
setubot = Getpic.setubot()


try:
    master = get_driver().config.master
except:
    master = []
##变量##
path =os.path.abspath(__file__).split('__')[0]
datapath = '/home/qqbot/plugindata/setu/'


MAX = 2  # 冲的次数
times = {} # 记录冲的次数
r18type= ['关闭','开启']
choosen = 0


# async def getpic(setu_url, author, bot, event):
#     for i ,u in enumerate(setu_url):
#         img_path = datapath + f'data/{i}.jpg'
#         #+ f'data/{i}.jpg'
#         print(u)
#         os.system(f'wget -E --referer https://www.pixiv.net {u} -O {img_path}')
#         #os.system(f'curl {u} > {img_path}')
#         msg = await bot.send(event, message = MessageSegment.image(f'file://{img_path}'))
#         setubot.pic_id.append(msg['message_id'])
#         await bot.send(event, message = author[i])
#         os.system(f'rm {img_path} -f')    


##bot 指令
setu = on_command('setu',aliases={'Setu', 'SETU'})
@setu.handle()
async def setu_handle(bot: Bot, event: Event, state: T_State):
    user_id = event.user_id
    #获取关键词，数量 并处理
    comman = str(event.message).split(' ')
    del comman[0]
    keyword = ''
    num = 1
    print(comman[0])
    # 变量只有一个 判定是keyword还是num
    try:
        if len(comman) == 1: 
            if comman[0].isdigit():
                num = int(comman[0])
                print(num)
            else:
                keyword = (comman[0])
        else:
            keyword = comman[0]
            num = int(comman[1])
    except :
        pass
    if num > 10:
        num = 10
        await bot.send(event, message = f'一次最多10张哦～')

    setu_url, author = setubot.getpic(int(num), keyword)
    if len(setu_url) == 0:
        setu_url, author = setubot.getpic()  
        await bot.send(event, message = f'找不到{keyword}的色图哦,随机一张吧')
        
    ###获取到url
    # thread0 = threading.Thread(target=await getpic(setu_url, author, bot, event))
    # thread0.start()
    #pic_list = await get_pic(setu_url)

    # for i ,p in enumerate(setu_url):
    #     print(p)
    #     await get_pic(p)
    #     img_path = datapath + f'data/0.png'
    #     fail_path  = datapath + f'data/fail{i}.png'
    #     #p.save(fp=img_path)
    #     try:
    #         msg = await bot.send(event, message = MessageSegment.image(f'file://{img_path}'))
    #         setubot.pic_id.append(msg['message_id'])
    #         await bot.send(event, message = author[i])
    #         os.system(f'rm {img_path} -f')
    #     except:
    #         os.system(f'cp {img_path} {fail_path}')
    #         os.system(f'rm {img_path} -f')
    #         await bot.send(event, message = f'第{i}张发送失败')
    #         try:
    #             msg = await bot.send(event, message = MessageSegment.image(f'file://{fail_path}'))
    #             setubot.pic_id.append(msg['message_id'])
    #             await bot.send(event, message = author[i])
    #             os.system(f'rm {fail_path} -f')
    #         except:
    #             await bot.send(event, message = f'重新发送失败')
    for i, p in enumerate(setu_url):
        try:
            print(p)
            pic = await get_pic(p)
            msg = await bot.send(event, message = MessageSegment.image(f'base64://{pic}'))
            await bot.send(event, message = author[i])
            setubot.pic_id.append(msg['message_id'])
        except:
            await bot.send(event, message = '失败，重试中')
            try:
                pic = await get_pic(re.sub('.jpg', '_master1200.jpg', re.sub('img-original/', 'img-master/', p, count=0, flags=0), count=0, flags=0))
                msg = await bot.send(event, message = MessageSegment.image(f'base64://{pic}'))
                await bot.send(event, message = author[i])
                await bot.send(event, message = '成功！')
                setubot.pic_id.append(msg['message_id'])
            except:
                await bot.send(event, message = '没救了')

    times[user_id] += num
    print(setubot.pic_id)
    print(len(setubot.pic_id))



recall_setu = on_command('撤回')
@recall_setu.handle()
async def recall_setu_handle(bot: Bot, event: Event, state: T_State):

    for id in setubot.pic_id:
        try:
            await bot.delete_msg(message_id=int(id))
        except:
            pass
        print(id)
    img_src = path + '/recall.png'
    img = MessageSegment.image(f'file://{img_src}')
    await bot.send(event, message = img)
    setubot.pic_id = []

pic_r18 = on_command('r18')
@pic_r18.handle()
async def pic_r18_handle(bot: Bot, event: Event, state: T_State):
    global choosen
    user_id = event.user_id
    if(user_id not in master):
        await pic_r18.finish('不可以哦')
    if(setubot.R18 == 0 and choosen == 0):
        setubot.tR18()
        choosen = 1
        await bot.send(event, message = f'R18模式 小心行事！')
    elif(setubot.R18 == 1 and choosen == 0):
        choosen = 1
        await bot.send(event, message = f'R18模式 小心行事！')
    elif(setubot.R18 == 1 and choosen == 1):
        setubot.tR18()
        choosen = 0
        await bot.send(event, message = f'限制模式')
    elif(setubot.R18 == 0 and choosen == 1):
        choosen = 0
        await bot.send(event, message = f'限制模式')
    else:
        await bot.send(event, message = f'？？')
    print(setubot.R18)

    

##-----------------------------------------------_##

# @on_command('stype', only_to_me=False)
# async def mode(session: CommandSession):
#     await session.send(message = f'''Mode: {setubot.mode[setubot.mode_]}
# R18:{r18type[setubot.R18]}
# MAXTIME:{MAX}''')

# @on_command('setutime', only_to_me=False)
# async def showtimes(session: CommandSession):
#     s = ''
#     sum = 0
#     for i,j in times.items():
#         s = s + f'{i} : {j}\n'
#         sum += j
#     await session.send(message = f'{s}sum : {sum}' )
    
# @on_command('cmode', only_to_me=False)
# async def tcmode(session: CommandSession):
#     seq = ''
#     for i,j in enumerate(setubot.mode):
#         seq = seq + f'{i}: {j}\n'
#     seq = seq + f'当前mode: {setubot.mode[setubot.mode_]}\n----------\n选择rank mode～'
#     num=session.current_arg.strip()
#     if not num:
#         num = session.get('message', prompt=seq)
#     await session.send(message = f'mode change: {setubot.Cmode(int(num))}')

