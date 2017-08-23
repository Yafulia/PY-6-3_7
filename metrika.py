from urllib.parse import urlencode, urljoin
import requests
#from pprint import pprint
import json

AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = '5656dfa185df40c5bbdd9d72aa557061'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

#print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAAf8vjJAAR_ngE_59BkCENdrv2lY47gUcc'

class YMBase:
    MANAGMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
         return {
             'Authorization': 'OAuth {}'.format(TOKEN),
             'User-Agent': 'netology6 test app',
             'Content-Type': 'application-x-yametrika+json'
         }


class YandexMetrika(YMBase):
    def get_counters(self):
        url = urljoin(self.MANAGMENT_URL, 'counters')
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        return [Counter(self.token, counter_id['id']) for counter_id in response.json()['counters']]

    def create_counter(self, name, site):
        url = urljoin(self.MANAGMENT_URL, 'counters')
        headers = self.get_headers()
        data = {'counter': {'name': name, 'site': site}}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.text#self

class Counter(YMBase):
    def __init__(self, token, counter_id):
        super().__init__(token)
        self.counter_id = counter_id

    def get_info(self):
        url = urljoin(self.MANAGMENT_URL, 'counter/{}'.format(self.counter_id))
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        return response.json()

    def get_visits(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()['totals'][0]

    @property
    def views(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()['data'][0]['metrics'][0]

    @property
    def users(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()['data'][0]['metrics'][0]

ym = YandexMetrika(TOKEN)
ym.create_counter('New', 'https://yafulia.github.io/')
counters = ym.get_counters()
print(counters)
for counter in counters:
    print(counter.get_visits())
    print(counter.views)
    print(counter.users)
