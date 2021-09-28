from flask import Flask
from flask import request
from pixivpy_async import AppPixivAPI
from datetime import timedelta, datetime
import requests
import json
import asyncio
import random
import re


app = Flask(__name__)

_TOKEN = "o-HYGiZqb_azny7RSwX7y2uy0Z0JVOu6WHUD9He9Vgk"

class pixiv:
    def __init__(self):
        self.aapi =  AppPixivAPI(proxy="http://127.0.0.1:1080")
        self.today = ''
        self.pic_id = []

        self.pic_user_id = []
        self.pic_user_works = []
        self.pic_user_name = []
        self.pic_today = {"day":[], "day_r18":[]}
        self.author_today = {"day":[], "day_r18":[]}
    
    #检查地址是否有效
    def check_url(self, url):
        proxies = {'https': 'http://127.0.0.1:1080'}
        headers = {'referer': 'https://www.pixiv.net'}
        result = requests.get(url, proxies=proxies, headers=headers)
        print(result.status_code)
        if(result.status_code != 200):
            url = re.sub('.jpg', '_master1200.jpg', re.sub('img-original/', 'img-master/', url, count=0, flags=0), count=0, flags=0)
        return url

    #将转换链接为原图
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
    async def random(self, typ='day', t=1):
        pic = []
        author = []
        pic_fin = []
        author_fin = []
        k = 0
        if self.pic_today[typ] and self.today == self.date():
            while k < t:
                i = random.randint(0,len(self.pic_today[typ])-1)
                url = self.check_url(self.pic_today[typ][i])
                if url not in pic_fin:
                    pic_fin.append(url)
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
                url = self.check_url(self.pic_today[typ][i])
                if url not in pic_fin:
                    pic_fin.append(url)
                    author_fin.append(self.author_today[typ][i])
                    k += 1
        return pic_fin, author_fin


pixiv_api = pixiv()

@app.route("/", methods=['GET', 'POST'])
async def get_data():
    if request.method == 'GET':
        typ = request.args.get("type")
        print(typ)
        data = await pixiv_api.random(typ)
        return json.dumps(data)
    else:
        data = await pixiv_api.random(request.form['times'], 'day')
        return json.dumps(data)