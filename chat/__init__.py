import json
import os
import random
import time
import sys
import re
from . import aiopic

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent,MessageEvent, PokeNotifyEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State

# -global- #
repeat_stop = False
trigger = {} #重复触发词判定
last_msg = "" #不重复发一个消息
data = {} #语料数据
ptalk = {} #群回复率
P = 1
focus_id = [] #特别对象 无视概率直接回复 user_id:int 
filter_list = []

gpath = '/home/qqbot/plugindata/chat'
path = gpath +'/data.json'
img_path = gpath + '/img'

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

def save_json(keys:str, values:str, id:str):
    '''
    写数据到json
    '''
    global data
    if id not in data:
        data[id] = {}
    if keys not in data[id]:
        data[id].setdefault(keys,[])
    if values not in data[id][keys]: 
        data[id][keys].append(values)
    with open(path, 'w+') as f :
        tojson = json.dumps(data,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
        f.write(tojson)

chat = on_message(priority=99)
@chat.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):
    message = str(event.raw_message)
    group_id = event.group_id
    user_id = event.user_id
    

    if 'CQ:image' in message:
        img_name = re.sub(']', '', message.split('=')[1])
        img_url = await bot.get_image(file=img_name)
        img_url = img_url['url']
        img_name = re.sub('image', 'png', img_name)
        img_name = img_path + '/' + img_name
        result = await aiopic.get_pic(img_url, img_name)
        print(result)
    global ptalk
    global last_msg
    ptalk.setdefault(group_id,P)
    trigger.setdefault(group_id,' ')
   
    for id in [1, group_id]:
        id = union(id, 1)
        for i in data[id]:
            if i in message :
                if len(i) > 3 or i == message:
                    # 重复回复的
                    if trigger[group_id] != i : 
                        if random.random() < ptalk[group_id] or user_id in focus_id:
                            if repeat_stop:
                                trigger[group_id] = i
                            print('ok')
                            #若消息不存在则删除
                            while True:
                                try:
                                    msg = ''.join(random.sample((data[id][i]), 1))
                                    if msg == last_msg:
                                        continue
                                    try:
                                        if 'image' in msg:
                                            img_msg = img_path + '/' + re.sub(']', '', msg.split('=')[1])
                                            img_msg = re.sub('image', 'png', img_msg)
                                            img_msg = MessageSegment.image(f'file://{img_msg}')
                                            await bot.send(event,message=img_msg)
                                        else:
                                            await bot.send(event,message=Message(msg))
                                    except:
                                        await bot.send(event,message=Message(msg))
                                    last_msg = msg
                                    break
                                except:
                                    print("delete ", msg)
                                    data[id][i].remove(msg)
                            return



setp = on_command('setP', aliases={"setp"}, rule = to_me())
@setp.handle()
async def setp_handle(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    user_id = event.user_id
    if user_id in bot.config.master:
        args = str(event.get_message()).strip()
        global ptalk
        if args:
            ptalk[group_id] = float(args)
            await setp.finish(f'现在的回复率为：{ptalk[group_id]}')





set_respond = on_command('set',aliases={"setall"})
@set_respond.handle()
async def set_handle(bot: Bot, event: Event, state: T_State):
    '''
    设置的问答
    setall 时全覆盖
    '''
    key = str(event.raw_message).split()[0]
    print(key)
    if key == "/setall":
        state['gid'] = 1
        state['uid'] = 1
        if event.user_id not in bot.config.master: 
            await set_respond.finish(Message("[CQ:image,file=cab2ae806af6b0a7b61fdd8534b50093.image]"))
            return
    else:
        state['gid'] = event.group_id
        state['uid'] = event.user_id
    comman = str(event.get_message()).split()
    if comman:
        state["key"] = comman[0]
        if len(comman) >1:
            state["value"] = comman[1]

@set_respond.got('key', prompt="设置什么～")
async def set_got(bot: Bot, event: Event, state: T_State):

    if ",url=" in state["key"] :
        state["key"] = state["key"].split(",url=")[0]+']'
def filter(word):
    for i in filter_list:
        if i in word:
            return True
    return False

@set_respond.got('value', prompt="要答什么呢～")
async def set_got2(bot: Bot, event: Event, state: T_State):

        if ",url=" in state["value"] :
            state["value"] = state["value"].split(",url=")[0]+']'
        if filter(state["key"]):
            await set_respond.finish(Message("[CQ:image,file=cab2ae806af6b0a7b61fdd8534b50093.image]"))
        else:
            try:
                #录入库
                if 'CQ:image' in state["value"]:
                    img_name = re.sub(']', '', state["value"].split('=')[1])
                    img_url = await bot.get_image(file=img_name)
                    img_url = img_url['url']
                    img_name = re.sub('image', 'png', img_name)
                    img_name = img_path + '/' + img_name
                    result = await aiopic.get_pic(img_url, img_name)
                    print(result)
                save_json(state["key"], state["value"], union(state['gid'] , 1))
                await set_respond.finish(message='ok~')
            except:
                print('over')

