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

#获取用户信息
def get_user_data():
    global user_json_path
    with open(user_json_path) as f:
        params = json.load(f)
    f.close()
    return params

#根据ID位置生成路径
def get_json_path(ID, location):
    path = data_path + ID + "/" + location + "/light.json"
    return path

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

#注册用户并生成文件
register = on_command('注册')
@register.handle()
async def register_handle(bot: Bot, event: Event, state: T_State):
    user_id = str(event.user_id)
    user_data = get_user_data()
    if user_id in user_data:
        await register.finish('你已经注册过了')
    else:
        result = add_user(user_id)
        await register.finish('注册完成')

set_default_location = on_command('默认位置', aliases=None)
@set_default_location.handle()
async def set_default_location_handle(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    set_default_location.user_id = str(event.user_id)
    set_default_location.user_data = get_user_data()
    if set_default_location.user_id not in set_default_location.user_data:
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
    if register_location.user_id not in register_location.user_data:
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