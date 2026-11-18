import os
import json

import execjs
import requests


class MyTokenCap:

    BASE_URL = "https://api.mytokenapi.com/ticker/currencyranklist"
    JS_FILENAME = "mytokencap.js"

    def __init__(self, pages="3,1", sizes="100,100", subject="market_cap",
                 language="en_US", legal_currency="USD"):
        
        self.pages = pages
        self.sizes = sizes
        self.subject = subject
        self.language = language
        self.legal_currency = legal_currency

        
        self._js_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), self.JS_FILENAME
        )
        self._js_ctx = self._load_js()
        self._session = requests.Session()

        
        self._encrypted = self._encrypt()

    # ---------- 属性方法（只读，派生数据） ----------

    @property
    def timestamp(self) -> str:
        
        return self._encrypted["time"]

    @property
    def code(self) -> str:
        
        return self._encrypted["code"]

    @property
    def headers(self) -> dict:
        
        return {
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
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0",
        }

    @property
    def params(self) -> dict:
        return {
            "pages": self.pages,
            "sizes": self.sizes,
            "subject": self.subject,
            "language": self.language,
            "legal_currency": self.legal_currency,
            "code": self.code,
            "timestamp": self.timestamp,
            "platform": "web_pc",
            "v": "0.1.0",
            "mytoken": "",
        }

    # ---------- 私有方法 ----------

    def _load_js(self):
        
        with open(self._js_path, encoding="utf-8") as f:
            return execjs.compile(f.read())

    def _encrypt(self) -> dict:
        
        return self._js_ctx.call("get_params")

    # ---------- 公共方法 ----------

    def refresh_params(self) -> None:
        
        self._encrypted = self._encrypt()

    def fetch(self) -> requests.Response:
        
        return self._session.get(
            self.BASE_URL,
            headers=self.headers,
            params=self.params,
            timeout=15,
        )

    def fetch_json(self) -> dict:
        
        return self.fetch().json()

    def fetch_pretty(self) -> str:
        
        return json.dumps(self.fetch_json(), ensure_ascii=False, indent=2)


def main() -> None:
    client = MyTokenCap()
    print(client.fetch_pretty())


if __name__ == "__main__":
    main()