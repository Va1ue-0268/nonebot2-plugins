import asyncio
from datetime import date, timedelta, datetime
import random
from pixivpy_async import AppPixivAPI
import re

_TOKEN = "JQ5glRsk9hD8XwPsVuHOgcJ-NcljnxUEf-9faM23Q6Q"

class pixiv:
    def __init__(self):
        self.aapi =  AppPixivAPI(proxy="http://127.0.0.1:1080")
        self.today = ''
        self.pic_id = []

        self.pic_user_id = []
        self.pic_user_works = []
        self.pic_user_name = []
        self.pic_today = {"day":[], "week":[], "month":[], "day_male":[], "day_female":[], "week_original":[], "week_rookie":[], "day_r18":[], "day_male_r18":[], "day_female_r18":[], "week_r18":[], "week_r18g":[], "day_manga":[], "week_manga":[], "month_manga":[], "week_rookie_manga":[], "day_r18_manga":[], "week_r18_manga":[], "week_r18g_manga":[]}
        self.author_today = {"day":[], "week":[], "month":[], "day_male":[], "day_female":[], "week_original":[], "week_rookie":[], "day_r18":[], "day_male_r18":[], "day_female_r18":[], "week_r18":[], "week_r18g":[], "day_manga":[], "week_manga":[], "month_manga":[], "week_rookie_manga":[], "day_r18_manga":[], "week_r18_manga":[], "week_r18g_manga":[]}

    
    #转换链接为原图
    def large_to_original (self, url):
        result = re.sub('_master1200', '', re.sub('c/600x1200_90_webp/img-master/', 'img-original/', url, count=0, flags=0), count=0, flags=0)
        return result

    #登录
    async def login(self): 
        await self.aapi.login(refresh_token=_TOKEN)

    #获取日期
    def date(self):
        yesterday = datetime.today() + timedelta(-2)
        yesterday_format = yesterday.strftime('%Y-%m-%d')
        return yesterday_format
    
    #搜索tag
    async def search(self, tag, t):
        await self.login()
        result = await self.aapi.search_illust(tag, search_target='exact_match_for_tags')
        pic = []
        author = []
        pic_fin = []
        author_fin = []
        for i in result.illusts:
            pic.append(self.large_to_original(i['image_urls']['large']))
            author.append(i['user']['name'])
        print(pic)
        try:
            pic_fin.append(pic[t])
            author_fin.append(author[t])
        except:
            pass
        return pic_fin, author_fin

    #搜索画师作品
    async def search_user(self, user_id, a, b):
        pic = []
        author = []
        pic_fin = []
        author_fin = []
        if user_id != self.pic_user_id:
            self.pic_user_id = user_id
            await self.login()
            result = await self.aapi.user_illusts(user_id)
            print(result)
            for i in result.illusts:
                try:
                    pic.append(self.large_to_original(i['image_urls']['large']))
                except:
                    try:
                        pic.append(i['image_urls']['medium'])
                    except:
                        pass
                author.append(i['user']['name'])
            while result.next_url:
                next_qs = self.aapi.parse_qs(result.next_url)
                result = await self.aapi.user_illusts(**next_qs)
                for i in result.illusts:
                    try:
                        pic.append(self.large_to_original(i['image_urls']['large']))
                    except:
                        try:
                            pic.append(i['image_urls']['medium'])
                        except:
                            pass
                    author.append(i['user']['name'])
            print(len(pic))
            self.pic_user_works = pic
            self.pic_user_name = author
            pic_fin = self.pic_user_works[a:b]
            author_fin = self.pic_user_name[a:b]
        else:
            pic_fin = self.pic_user_works[a:b]
            author_fin = self.pic_user_name[a:b]
        return pic_fin, author_fin, len(self.pic_user_works)

    #随机日榜
    async def random(self, t, typ):
        pic = []
        author = []
        pic_fin = []
        author_fin = []
        k = 0
        if self.pic_today[typ] and self.today == self.date():
            while k < t:
                i = random.randint(0,len(self.pic_today[typ])-1)
                if self.pic_today[typ][i] not in pic_fin:
                    pic_fin.append(self.pic_today[typ][i])
                    author_fin.append(self.author_today[typ][i])
                    k += 1
        else:
            if self.today != self.date():
                print('day changed, caching new data')
                print('%s to %s'%(self.today, self.date()))
                self.today = self.date()
            await self.login()
            result = await self.aapi.illust_ranking(typ, date=self.date())
            for i in result.illusts:
                try:
                    pic.append(self.large_to_original(i['image_urls']['large']))
                except:
                    try:
                        pic.append(i['image_urls']['medium'])
                    except:
                        pass
                author.append(i['user']['name'])
            while result.next_url:
                next_qs = self.aapi.parse_qs(result.next_url)
                result = await self.aapi.illust_ranking(**next_qs)
                for i in result.illusts:
                    try:
                        pic.append(self.large_to_original(i['image_urls']['large']))
                    except:
                        try:
                            pic.append(i['image_urls']['medium'])
                        except:
                            pass
                    author.append(i['user']['name'])
            print(len(pic))
            self.pic_today[typ] = pic
            self.author_today[typ] = author
            while k < t:
                i = random.randint(0,len(self.pic_today[typ])-1)
                if pic[i] not in pic_fin:
                    pic_fin.append(self.pic_today[typ][i])
                    author_fin.append(self.author_today[typ][i])
                    k += 1
        return pic_fin, author_fin

# pixiv_bot = pixiv()
# async def main ():
#     id = 333556
#     a = 1
#     b = 2
#     await pixiv_bot.search_user(id, a, b)
# asyncio.run(main())