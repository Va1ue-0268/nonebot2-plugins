import time
import json
import os
import nonebot
import json
from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (Event, MessageEvent)
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State

#初始化次数
t = 0

#用来存储数据
dict={}

#以后用数据库，现在先用着
user_json_path = get_driver().config.plugin_data + 'light/user_data.json'
data_path = '/home/download/esp/'
#根据情况自己改
IRData_path = '/home/qqbot/plugindata/light/IRData.json'

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

#获取json里面数据
async def IR(json_path, command):
    #读取红外数据
    with open(IRData_path) as f:
            IRData = json.load(f)
    f.close()
    #print(IRData)
    # for i in IRData:
    #     print(i)
    if command not in IRData:
        return 0
    with open(json_path) as f:
        params = json.load(f)
        params['IR'] = 1
        params['IRCommandLenght'] = len(IRData[command])
        #print(len(IRData[command]))
        params['IRCommand'] = IRData[command]
        dict = params
    f.close()
    with open(json_path,'w+') as r:
        tojson = json.dumps(dict,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    f.close()
    params['IR'] = 0
    params['IRCommandLenght'] = 0
    params['IRCommand'] = 0
    dict = params
    time.sleep(2)
    with open(json_path,'w+') as r:
        tojson = json.dumps(dict,sort_keys=False, ensure_ascii=False, indent=4,separators=(',',': '))
        r.write(tojson)
    r.close()
    return dict

IR_control = on_command('IR', aliases=None)
@IR_control.handle()
async def IR_control_handle(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    IR_control.user_id = str(event.user_id)
    IR_control.user_data = get_user_data()
    if IR_control.user_id not in IR_control.user_data:
        await IR_control.finish('你还没有注册哦')
    default_location = IR_control.user_data[IR_control.user_id]['default']
    if command:
        IR_control.place = command[0]
        if IR_control.place not in IR_control.user_data[IR_control.user_id]['location']:
            await IR_control.finish('没有这个位置哦')
    else:
        IR_control.place = default_location
    json_path = get_json_path(IR_control.user_id, IR_control.place)
    result = IR(json_path, R, G, B)
    print(result)
    await bot.send(event, message='开灯啦～')
    await IR_control.finish()

#位置还没和light使用同一种方法，有时间改
IR_control = on_command('IR', aliases={'ir', '遥控'})
@IR_control.handle()
async def IR_control_handle(bot: Bot, event: Event, state: T_State):
    if event.user_id not in bot.config.controller:
        await reject(bot, event)
        await IR_control.finish()
    command = str(event.get_message()).split()
    if command:
        place = command[0]
        if place == "学校":
            result = await IR(school_json_path, command[1])
        elif place == "家":
            result = await IR(home_json_path, command[1])
        else:
            await IR_control.finish('暂时没有这个位置哦')
        if (result == 0):
            await IR_control.finish('指令错误')
        await IR_control.finish('调好啦～')
    for i in IRData:
        await bot.send(event, message=i)
    await bot.send(event, message='以上是家里空调的指令')
    await IR_control.finish()
