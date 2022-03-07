import time
import json
import os
import nonebot
import json
from nonebot import on_command, get_driver, get_bots, require
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import (Event, MessageEvent)
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State

#以后用数据库，现在先用着
user_data_path = get_driver().config.plugin_data + 'flask_light/user_data.json'
check_data_path = get_driver().config.plugin_data + 'flask_light/data.json'

#初始化次数
t = 0

#用来存储数据
dict={}
user_id = 0
place = ''
check_data = {}

scheduler = require('nonebot_plugin_apscheduler').scheduler
group = [1048058406]

with open(check_data_path) as f:
    check_data = json.load(f)
f.close()
###拒绝请求，已经不用了
# async def reject(bot, event):
#     global t
#     t = t + 1
#     if t == 1:
#         await bot.send(event, message='这是主人才能碰的哦')
#     elif t == 2:
#         await bot.send(event, message='不听是吧？')
#         await bot.send(event, Message('[CQ:image,file=bc24e53cc970222a6617e4440a47e0f8.image]'))
#     elif t == 3:
#         await bot.send(event, message='不理你了哦')
#     elif t == 4:
#         await bot.send(event, message='真的不理你了！哼！')
#     elif t == 7:
#         t = 0

#开灯
def light_on(user_id, place, R, G, B):
    with open(user_data_path) as f:
        params = json.load(f)
        params[user_id][place]['state'] = 1
        params[user_id][place]['red'] = R
        params[user_id][place]['green'] = G
        params[user_id][place]['blue'] = B
    f.close()
    with open(user_data_path,'w+') as r:
        tojson = json.dumps(params,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    return params

#关灯
def light_off(user_id, place):
    with open(user_data_path) as f:
        params = json.load(f)
        params[user_id][place]['state'] = "0"
    f.close()
    with open(user_data_path,'w') as r:
        tojson = json.dumps(params,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    return params

#获取用户信息
def get_user_data():
    with open(user_data_path) as f:
        params = json.load(f)
    f.close()
    return params

def get_check_data():
    with open(check_data_path) as f:
        params = json.load(f)
    f.close()
    return params

#更改信息，key为关键词，value为值
def change_user_data(user_id, location, key, value):
    with open(user_data_path) as f:
        params = json.load(f)
    f.close()
    params[user_id][location][key] = value 
    with open(user_data_path,'w+') as r:
        tojson = json.dumps(params,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    return params

def get_user_color(user_id, location):
    data = get_user_data()
    return data[user_id][location]

#检查是否在线
@scheduler.scheduled_job('cron', minute='*/1', id='online_check', misfire_grace_time=10, coalesce=True)
async def online_check():
    data = get_check_data()
    for bot in get_bots().values():
        for user_id in data:
            for check_location in data[user_id]['check_location']:
                if(data[user_id][check_location]['is_online'] == 0 and check_data[user_id][check_location]['is_online'] == 1):
                    check_data[user_id][check_location]['is_online'] = 0
                    for gid in group:
                        msg = f'灯掉线了！[CQ:at,qq={user_id}]'
                        await bot.send_group_msg(group_id = gid, message=msg) 
                elif(data[user_id][check_location]['is_online'] == 1 and check_data[user_id][check_location]['is_online'] == 0):
                    check_data[user_id][check_location]['is_online'] = 1
                    for gid in group:
                        msg = f'灯上线了！[CQ:at,qq={user_id}]'
                        await bot.send_group_msg(group_id = gid, message=msg)

 
set_light_on_cn = on_command('开灯', aliases=None)
@set_light_on_cn.handle()
async def set_light_on_cn_handle(bot: Bot, event: Event, state: T_State):
    global user_id, place
    command = str(event.get_message()).split()
    del command[0]
    user_id = str(event.user_id)
    user_data = get_user_data()
    if user_id not in user_data:
        await set_light_on_cn.finish('你还没有注册哦')
    default_location = user_data[user_id]['default']
    if len(command) > 0:
        place = command[0]
        if place not in user_data[user_id]['location']:
            await set_light_on_cn.finish('没有这个位置哦')
    else:
        place = default_location
    color_data = get_user_color(user_id, place)
    print(color_data)
    R = color_data['red']
    G = color_data['green']
    B = color_data['blue']
    result = light_on(user_id, place, R, G, B)
    print(result)
    await bot.send(event, message='开灯啦～')
    await set_light_on_cn.finish()

set_light_off_cn = on_command('关灯', aliases=None)
@set_light_off_cn.handle()
async def set_light_off_cn_handle(bot: Bot, event: Event, state: T_State):
    global user_id, place
    command = str(event.get_message()).split()
    del command[0]
    user_id = str(event.user_id)
    user_data = get_user_data()
    if user_id not in user_data:
        await set_light_off_cn.finish('你还没有注册哦')
    default_location = user_data[user_id]['default']
    if len(command) > 0:
        place = command[0]
        if place not in user_data[user_id]['location']:
            await set_light_off_cn.finish('没有这个位置哦')
    else:
        place = default_location
    result = light_off(user_id, place)
    print(result)
    await bot.send(event, message='关灯啦～')
    await set_light_off_cn.finish()

set_light_color_cn = on_command('颜色', aliases=None)
@set_light_color_cn.handle()
async def set_light_color_cn_handle(bot: Bot, event: Event, state: T_State):
    global user_id, place
    command = str(event.get_message()).split()
    del command[0]
    user_id = str(event.user_id)
    user_data = get_user_data()
    if user_id not in user_data:
        await set_light_color_cn.finish('你还没有注册哦')
    default_location = user_data[user_id]['default']
    if len(command) > 0:
        if command[0][0].isdigit() == 1:
            place = default_location
            R = command[0]
            G = command[1]
            B = command[2]
            result = light_on(user_id, place, R, G, B)
            print(result)
            await set_light_color_cn.finish('调好啦～')
        else:
            place = command[0]
            if place not in user_data[user_id]['location']:
                await set_light_color_cn.finish('没有这个位置哦')
            if command[1][0].isdigit() == 1:
                R = command[1]
                G = command[2]
                B = command[3]
                result = light_on(user_id, place, R, G, B)
                print(result)
                await set_light_color_cn.finish('调好啦～')
    else:
        place = default_location

@set_light_color_cn.got('color', prompt="颜色是")
async def set_light_color_cn_got(bot: Bot, event: Event, state: T_State):
    color = state['color'].split()
    R = color[0]
    G = color[1]
    B = color[2]
    print(R, G, B)
    result = light_on(user_id, place, R, G, B)
    print(result)
    await set_light_color_cn.finish('调好啦～')

