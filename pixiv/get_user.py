from pixivpy3 import *

_REQUESTS_KWARGS = {
    'proxies': {
        'https': 'http://127.0.0.1:1080',
    }}
token = ""

class pixiv_user:
    def __init__(self):
        self.aapi = AppPixivAPI(**_REQUESTS_KWARGS)

    def login(self):
        self.aapi.auth(refresh_token=token)

    #获取搜索的画师id
    def search_user(self,user):
        self.login()
        result = self.aapi.search_user(user)
        id = []
        name = []
        for i in result['user_previews']:
            print(i['user'])
            id.append(i['user']['id'])
            name.append(i['user']['name'])
        return id,name
