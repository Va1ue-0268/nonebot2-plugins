import time
import json
import os
import nonebot
import json
import uuid
from nonebot import on_command
from controller.db import add_device, check_if_exist, update_state
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (Event, MessageEvent)
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State
import db

LOCATION = ['学校', '家']

register = on_command('t注册', aliases=None)
@register.handle()
async def register_handle(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    _uuid = uuid.uuid1()
    _id = str(event.user_id)
    if command[0] and command[1] in LOCATION:
        location = command[0]
        type = command[1]
        if command[2]:
            nickname = command[2]
        else:
            num = count_device(_id, type) + 1
            nickname = f"{type}" + f"{num}"
        add_device(_id, _uuid, location, type, nickname)
        await register.finish(f'[CQ:at,qq={_id}]注册完成，设备名为 {nickname}，设备uuid为 {_uuid}，请妥善保管')
    else:
        await register.finish('参数不完整，用法为“注册 地点 设备类型 (设备名)”')

set_default_device = on_command('t默认设备', aliases=None)
@set_default_device.handle()
async def set_default_device(bot: Bot, event: Event, state: T_State):
    command = str(event.get_message()).split()
    _id = str(event.user_id)
    if command[0] and command[1]:
        type = command[0]
        update_state(_id, )

    