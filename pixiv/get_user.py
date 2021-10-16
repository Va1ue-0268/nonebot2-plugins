from pixivpy3 import *


_REQUESTS_KWARGS = {
    'proxies': {
        'https': 'http://127.0.0.1:1080',
    }}
token = "o-HYGiZqb_azny7RSwX7y2uy0Z0JVOu6WHUD9He9Vgk"

class pixiv_user:
    def __init__(self):
        self.aapi = AppPixivAPI(**_REQUESTS_KWARGS)

    def login(self):
        self.aapi.auth(refresh_token=token)

    def search_user(self,user):
        self.login()
        result = self.aapi.search_user(user)
        id = []
        name = []
        total = 0
        for i in result['user_previews']:
            # i = i['illusts']['image_urls']['large']
            print(i['user'])
            id.append(i['user']['id'])
            name.append(i['user']['name'])
            total = total + 1
        return id, name, total
