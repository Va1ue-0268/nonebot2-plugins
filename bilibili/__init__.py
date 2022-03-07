
from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event
from .dynamic import *
from .live import *

try:
    master = get_driver().config.master
except:
    master = []

push_dynamic = on_command("更新推送")
'''
直接修改数据库的对应字段
mid filter(动态|直播|过滤) value([0,1],[0,1],['过滤字段'])
'''
@push_dynamic.handle()
async def push_dynamic_handle(bot: Bot, event):
    uid = event.user_id
    gid = event.group_id
    member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    if member_info['role'] == "owner" or member_info['role'] == "admin" or uid in master:
        try:
            content = str(event.get_message()).split(' ')
            del content[0]
            key = content[0]

            if content[1] == "动态":
                filter = "dynamic"
            if content[1] == "过滤":
                filter = "dy_filter"
            if content[1] == "直播":
                filter = "live"
            value = content[2]
            if value.isdigit():
                value = int(value)

            if key.isdigit():
                res = select_by_field(gid, key)
            else:
                res = select_by_field(gid, key, 'name')
                print(res)
            mid = res[2]

            update(gid, mid, filter, value)
            await bot.send(event, message=f"ok")
        except:
            await bot.send(event, message=f"失败了～ 发送 mid 字段 内容")
    else:
        await bot.send(event, message="你没有该权限哦～")
        return
