import execjs
import requests
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
js_path = os.path.join(base_dir, "mytokencap.js")

with open(js_path, encoding='utf-8') as f:
    js_code = f.read()
    js = execjs.compile(js_code)
    code = js.call('get_params')

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "origin": "https://www.mytokencap.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.mytokencap.com/",
    "sec-ch-ua": "\"Not=A?Brand\";v=\"99\", \"Microsoft Edge\";v=\"151\", \"Chromium\";v=\"151\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"
}
url = 'https://api.mytokenapi.com/ticker/currencyranklist'
params = {
    "pages": "3,1",
    "sizes": "100,100",
    "subject": "market_cap",
    "language": "en_US",
    "legal_currency": "USD",
    "code": code['code'],
    "timestamp": code['time'],
    "platform": "web_pc",
    "v": "0.1.0",
    "mytoken": ""
}
response = requests.get(url, headers=headers, params=params, timeout=15)

resp_json = json.dumps(response.json(), ensure_ascii=False, indent=2)

print(resp_json)