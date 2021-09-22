import time
import json
import os
import nonebot
import json
from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (Event, MessageEvent)
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State

#以后用数据库，现在先用着
user_json_path = '/home/qqbot/plugindata/light/user_data.json'
data_path = '/home/download/esp/'

#初始化次数
t = 0

#用来存储数据
dict={}

#默认配置
default = {
    "default": "学校",
    "location": ["学校"]
}

default_light = {
    "state": 1,
    "red": 255,
    "green": 200,
    "blue": 160
}

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
def light_on(json_path, R, G, B):
    with open(json_path) as f:
        params = json.load(f)
        params['state'] = 1
        params['red'] = R
        params['green'] = G
        params['blue'] = B
    f.close()
    with open(json_path,'w+') as r:
        tojson = json.dumps(params,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    return params

#关灯
def light_off(json_path):
    with open(json_path) as f:
        params = json.load(f)
        params['state'] = "0"
    f.close()
    with open(json_path,'w') as r:
        tojson = json.dumps(params,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    return params

#根据ID位置生成路径
def get_json_path(ID, location):
    path = data_path + ID + "/" + location + "/light.json"
    return path

#获取用户信息
def get_user_data():
    global user_json_path
    with open(user_json_path) as f:
        params = json.load(f)
    f.close()
    return params

#更改信息，key为关键词，value为值
def change_user_data(ID, key, value):
    global user_json_path
    with open(user_json_path) as f:
        params = json.load(f)
    f.close()
    params[ID][key] = value 
    with open(user_json_path,'w+') as r:
        tojson = json.dumps(params,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    return params

#获取当前状态颜色
def get_user_color(ID, location):
    global data_path
    path = data_path + ID + "/" + location + "/light.json"
    with open(path) as f:
        params = json.load(f)
    f.close()
    return params

#添加用户
def add_user(ID):
    global user_json_path
    global default
    global default_light
    with open(user_json_path) as f:
        params = json.load(f)
    f.close()
    params[ID] = default
    print(params[ID])
    with open(user_json_path,'w+') as r:
        tojson = json.dumps(params,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    path = get_json_path(ID, params[ID]['location'][0])
    print(path)
    os.makedirs(path.replace('light.json', ''))
    with open(path, 'w+') as r:
        tojson = json.dumps(default_light,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    return True

#添加位置
def add_location(ID, location):
    global user_json_path
    global data_path
    global default_light
    with open(user_json_path) as f:
        params = json.load(f)
    f.close()
    if location in params[ID]['location']:
        return 0
    params[ID]['location'].append(location)
    with open(user_json_path,'w+') as r:
        tojson = json.dumps(params,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    path = get_json_path(ID, location)
    os.makedirs(path.replace('light.json', ''))
    with open(path, 'w+') as r:
        tojson = json.dumps(default_light,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()

#注册用户并生成文件
register = on_command('注册')
@register.handle()
async def register_handle(bot: Bot, event: Event, state: T_State):
    user_id = str(event.user_id)
    user_data = get_user_data()
    if user_id in user_data:
        await set_light_on_cn.finish('你已经注册过了')
    else:
        result = add_user(user_id)
        await set_light_on_cn.finish('注册完成')


set_light_on_cn = on_command('开灯', aliases=None)
@set_light_on_cn.handle()
async def set_light_on_cn_handle(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    set_light_on_cn.user_id = str(event.user_id)
    set_light_on_cn.user_data = get_user_data()
    if set_light_on_cn.user_id not in set_light_on_cn.user_data:
        await set_light_on_cn.finish('你还没有注册哦')
    default_location = set_light_off_cn.user_data[set_light_on_cn.user_id]['default']
    if command:
        set_light_on_cn.place = command[0]
        if set_light_on_cn.place not in set_light_on_cn.user_data[set_light_on_cn.user_id]['location']:
            await set_light_on_cn.finish('没有这个位置哦')
    else:
        set_light_on_cn.place = default_location
    color_data = get_user_color(set_light_on_cn.user_id, set_light_on_cn.place)
    print(color_data)
    R = color_data['red']
    G = color_data['green']
    B = color_data['blue']
    json_path = get_json_path(set_light_on_cn.user_id, set_light_on_cn.place)
    result = light_on(json_path, R, G, B)
    print(result)
    await bot.send(event, message='开灯啦～')
    await set_light_on_cn.finish()

set_light_off_cn = on_command('关灯', aliases=None)
@set_light_off_cn.handle()
async def set_light_off_cn_handle(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    set_light_off_cn.user_id = str(event.user_id)
    set_light_off_cn.user_data = get_user_data()
    if set_light_off_cn.user_id not in set_light_off_cn.user_data:
        await set_light_off_cn.finish('你还没有注册哦')
    default_location = set_light_off_cn.user_data[set_light_off_cn.user_id]['default']
    if command:
        set_light_off_cn.place = command[0]
        if set_light_off_cn.place not in set_light_off_cn.user_data[set_light_off_cn.user_id]['location']:
            await set_light_off_cn.finish('没有这个位置哦')
    else:
        set_light_off_cn.place = default_location
    json_path = get_json_path(set_light_off_cn.user_id, set_light_off_cn.place)
    result = light_off(json_path)
    print(result)
    await bot.send(event, message='关灯啦～')
    await set_light_off_cn.finish()

set_light_color_cn = on_command('颜色', aliases=None)
@set_light_color_cn.handle()
async def set_light_color_cn_handle(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    set_light_color_cn.user_id = str(event.user_id)
    set_light_color_cn.user_data = get_user_data()
    if set_light_color_cn.user_id not in set_light_color_cn.user_data:
        await set_light_on_cn.finish('你还没有注册哦')
    default_location = set_light_color_cn.user_data[set_light_color_cn.user_id]['default']
    if command:
        if command[0][0].isdigit() == 1:
            set_light_color_cn.place = default_location
            set_light_color_cn.color = command[1:-1]
            R = set_light_color_cn.color[0]
            G = set_light_color_cn.color[1]
            B = set_light_color_cn.color[2]
        else:
            set_light_color_cn.place = command[0]
            if set_light_color_cn.place not in set_light_color_cn.user_data[set_light_color_cn.user_id]['location']:
                await set_light_on_cn.finish('没有这个位置哦')
    else:
        set_light_color_cn.place = default_location

@set_light_color_cn.got('set_light_color_cn.color', prompt="颜色是")
async def set_light_color_cn_got(bot: Bot, event: Event, state: T_State):
    color = state['set_light_color_cn.color'].split()
    R = color[0]
    G = color[1]
    B = color[2]
    print(R, G, B)
    json_path = get_json_path(set_light_color_cn.user_id, set_light_color_cn.place)
    result = light_on(json_path, R, G, B)
    print(result)
    await set_light_color_cn.finish('调好啦～')

set_default_location = on_command('默认位置', aliases=None)
@set_default_location.handle()
async def set_default_location_handle(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    set_default_location.user_id = str(event.user_id)
    set_default_location.user_data = get_user_data()
    if set_default_location.user_id not in set_light_color_cn.user_data:
        await set_default_location.finish('你还没有注册哦')
    set_default_location.default_location = set_default_location.user_data[set_default_location.user_id]['default']
    if command:
        if command[0][0].isdigit() == 0:
            set_default_location.location = command[0]
            print(set_default_location.location)
            print(set_default_location.user_data[set_default_location.user_id]['location'])
            if set_default_location.location not in set_default_location.user_data[set_default_location.user_id]['location']:
                await set_default_location.finish('没有这个位置哦')
            result = change_user_data(set_default_location.user_id, 'default', set_default_location.location)
            print(result)
            await set_default_location.finish('默认位置从 %s 改为 %s'%(set_default_location.default_location, set_default_location.location))
        else:
            await set_default_location.finish('位置开头不能为数字')
@set_default_location.got('set_default_location.location', prompt="默认位置改为？")
async def set_default_location_got(bot: Bot, event: Event, state: T_State):
    place = state['set_default_location.location'].split()
    set_default_location.location = place[0]
    if set_default_location.location[0][0].isdigit() == 0:
        if set_default_location.location not in set_default_location.user_data[set_default_location.user_id]['location']:
            await set_default_location.finish('没有这个位置哦')
        result = change_user_data(set_default_location.user_id, 'default', set_default_location.location)
        print(result)
        await set_default_location.finish('默认位置从 %s 改为 %s'%(set_default_location.default_location, set_default_location.location))
    else:
        await set_default_location.finish('位置开头不能为数字')

register_location = on_command('添加位置')
@register_location.handle()
async def register_location_handle(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    register_location.user_id = str(event.user_id)
    register_location.user_data = get_user_data()
    if register_location.user_id not in set_light_color_cn.user_data:
        await register_location.finish('你还没有注册哦')
    if command:
        if command[0][0].isdigit() == 0:
            register_location.location = command[0]
            result = add_location(register_location.user_id, register_location.location)
            if result == 0:
                await register_location.finish('位置已存在')
            await register_location.finish('添加位置 %s'%(register_location.location))
        else:
            await register_location.finish('位置开头不能为数字')
@register_location.got('register_location.location', prompt="要添加什么位置呢")
async def register_location_got(bot: Bot, event: Event, state: T_State):
    place = state['register_location.location'].split()
    register_location.location = place[0]
    if register_location.location[0][0].isdigit() == 0:
        result = add_location(register_location.user_id, register_location.location)
        if result == 0:
            await register_location.finish('位置已存在')
        await register_location.finish('添加位置 %s'%(register_location.location))
    else:
        await register_location.finish('位置开头不能为数字')