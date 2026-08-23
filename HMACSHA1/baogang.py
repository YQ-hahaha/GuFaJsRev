import requests
import execjs
import os
import json



url = 'https://cmsauth.baowugroup.com/v1/web/api/content/list'
params = {
    "domainId": "12"
}

for page in range(1):
    print(f"第{page + 1}页:")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    js_path = os.path.join(base_dir, "baogang.js")

    with open(js_path, encoding='utf-8') as f:
        js_code = f.read()
        js = execjs.compile(js_code)
        code = js.call('get_par', page)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Md5": code["Content-Md5"],
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.baosteel.com",
        "Pragma": "no-cache",
        "Referer": "https://www.baosteel.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0",
        "sec-ch-ua": "\"Not=A?Brand\";v=\"99\", \"Microsoft Edge\";v=\"151\", \"Chromium\";v=\"151\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "x-date": str(code['x-date']),
        "x-nonce": code["x-nonce"],
        "x-signature": code["x-signature"],
        "x-user": code["x-user"]
    }

    data = {
        "pageNo":page,
        "pageSize":12,
        "condition":{"nodeId":436}
    }

    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, params=params, data=data)

    for data in response.json()['data']['data']:
        print(json.dumps(data, ensure_ascii=False, indent=2))