from posixpath import expanduser
from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.typing import T_State
from . import get_url, get_user, aiopic
import re

pixiv = get_url.pixiv()
pixiv_user = get_user.pixiv_user()


try:
    master = get_driver().config.master
except:
    master = []

##bot 指令
setu = on_command('pixiv',aliases={'P站', 'Pixiv'})
@setu.handle()
async def setu_handle(bot: Bot, event: Event, state: T_State):
    user_id = event.user_id
    #获取关键词，数量 并处理
    comman = str(event.message).split(' ')
    del comman[0]
    keyword = ''
    pic_url = []
    id = []
    pixiv_id = 0
    num = 1
    # 变量只有一个 判定是keyword还是num
    if len(comman) > 0:
        if len(comman) == 1: 
            if comman[0].isdigit():
                num = int(comman[0])
                print(num)
            else:
                keyword = comman[0]
        elif len(comman) == 2 and comman[0] != 'id':
            keyword = comman[0]
            num = int(comman[1])
        elif comman[0] == 'user':
            keyword = comman[0]
            user = comman[1]
            id, name, id_total = pixiv_user.search_user(user)
            if id_total == 1:
                keyword = 'id'
                pixiv_id = id[0]
                try:
                    if comman[2] and comman[3]:
                        a = int(comman[2])-1
                        b = int(comman[3])
                except:
                    try:
                        if comman[2]:
                            b = int(comman[2])
                            a = 0
                    except:
                        a = 0
                        b = 1
                if b - a > 10:
                    b = a + 10
                    await bot.send(event, message = f'一次最多10张哦，本姬只能为你发送{a+1}到{b}张')
            else:
                try:
                    print(comman[2])
                    if comman[2][-2:] == 'th':
                        keyword = 'id'
                        pixiv_id = id[int(re.sub("\D", "", comman[2]))-1]
                        try:
                            if comman[3] and comman[4]:
                                a = int(comman[3])-1
                                b = int(comman[4])
                        except:
                            try:
                                if comman[3]:
                                    b = int(comman[3])
                                    a = 0
                            except:
                                a = 0
                                b = 1
                        if b - a > 10:
                            b = a + 10
                            await bot.send(event, message = f'一次最多10张哦，本姬只能为你发送{a+1}到{b}张')
                        print(a)
                        print(b)
                    else:
                        id_num = int(comman[2])
                except:
                    id_num = 1
        elif comman[0] == 'id':
            keyword = comman[0]
            pixiv_id = int(comman[1])
            try:
                if comman[2] and comman[3]:
                    a = int(comman[2])-1
                    b = int(comman[3])
            except:
                try:
                    if comman[2]:
                        b = int(comman[2])
                        a = 0
                except:
                    a = 0
                    b = 1
            if b - a > 10:
                b = a + 10
                await bot.send(event, message = f'一次最多10张哦，本姬只能为你发送{a+1}到{b}张')
            print(a)
            print(b)


    try:
        if num > 10:
            num = 10
            await bot.send(event, message = f'一次最多10张哦，本姬只能为你发送10张')
    except:
        pass

    if keyword:
        if keyword == '涩图':
            pic_url, author = await pixiv.random(int(num), "day_r18")
        elif keyword == '周榜':
            pic_url, author = await pixiv.random(int(num), "week")
        elif keyword == '月榜':
            pic_url, author = await pixiv.random(int(num), "month")
        elif keyword == '原创榜':
            pic_url, author = await pixiv.random(int(num), "week_original")
        elif keyword == '菜鸟榜':
            pic_url, author = await pixiv.random(int(num), "week_rookie")
        elif keyword == 'user':
            pass
        elif keyword == 'id':
            pic_url, author, pic_total = await pixiv.search_user(pixiv_id, a, b)
        else:
            pic_url, author = await pixiv.search(keyword, int(num))
    else:
        pic_url, author = await pixiv.random(int(num), "day")
    if pixiv_id == 0 and len(id) == 0:
        if len(pic_url) == 0:
            #pic_url, author = await pixiv.random(int(num))  
            await bot.send(event, message = f'找不到{keyword}的图哦,随机一张吧')
            pic_url, author = await pixiv.random(int(num), "day")
    print(pic_url)

    if pic_url:
        temp = ''
        for i, p in enumerate(pic_url):
            try:
                print(p)
                pic = await aiopic.get_pic(p)
                if temp != author[i]:
                        print(temp)
                        temp = author[i]
                        await bot.send(event, message = author[i])
                msg = await bot.send(event, message = MessageSegment.image(f'base64://{pic}'))
                pixiv.pic_id.append(msg['message_id'])
            except:
                #await bot.send(event, message = '失败，重试中')
                try:
                    pic = await aiopic.get_pic(re.sub('.jpg', '_master1200.jpg', re.sub('img-original/', 'img-master/', p, count=0, flags=0), count=0, flags=0))
                    if temp != author[i]:
                        print(temp)
                        temp = author[i]
                        await bot.send(event, message = author[i])
                    msg = await bot.send(event, message = MessageSegment.image(f'base64://{pic}'))
                    #await bot.send(event, message = '成功！')
                    pixiv.pic_id.append(msg['message_id'])
                except:
                    await bot.send(event, message = '第%d没救了'%i)
        try:
            if pic_total:
                if b == 1:
                    await bot.send(event, message = '%s 共有%d张作品，这是第1张'%(author[i], pic_total))
                else:
                    await bot.send(event, message = '%s 共有%d张作品，这是第%d到第%d张'%(author[i], pic_total, a+1, b))
        except:
            pass
    else:
        for i, p in enumerate(id):
            n = name[i]
            await bot.send(event, message = f'{n} {p}' )
            if i == id_num-1:
                await bot.send(event, message = f'共有{id_total}个相关用户，现在显示了{id_num}个')
                break

    print(pixiv.pic_id)
    print(len(pixiv.pic_id))



recall_setu = on_command('撤回pixiv')
@recall_setu.handle()
async def recall_setu_handle(bot: Bot, event: Event, state: T_State):

    for id in pixiv.pic_id:
        try:
            await bot.delete_msg(message_id=int(id))
        except:
            pass
        print(id)
    img_src = path + '/recall.png'
    img = MessageSegment.image(f'file://{img_src}')
    await bot.send(event, message = img)
    pixiv.pic_id = []