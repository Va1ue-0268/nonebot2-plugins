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

#初始化次数
t = 0

#用来存储数据
dict={}

school_json_path = '/home/download/esp/IR.html'
home_json_path = '/home/download/esp/home/IR.html'
IRData_path = '/home/qqbot/plugindata/light/IRData.json'

async def reject(bot, event):
    global t
    t = t + 1
    if t == 1:
        await bot.send(event, message='这是主人才能碰的哦')
    elif t == 2:
        await bot.send(event, message='不听是吧？')
        await bot.send(event, Message('[CQ:image,file=bc24e53cc970222a6617e4440a47e0f8.image]'))
    elif t == 3:
        await bot.send(event, message='不理你了哦')
    elif t == 4:
        await bot.send(event, message='真的不理你了！哼！')
    elif t == 7:
        t = 0


async def IR(json_path, command):
#获取json里面数据
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
