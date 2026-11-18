import os
import json

import execjs
import requests


class BaoGang:
    """宝钢 CMS 内容列表接口封装。

    签名算法写在前端 baogang.js 中，通过 execjs 复用同一份代码生成签名头。
    """

    BASE_URL = "https://cmsauth.baowugroup.com/v1/web/api/content/list"
    JS_FILENAME = "baogang.js"

    def __init__(self, domain_id="12", page_size=12, node_id=436):
        self.domain_id = domain_id
        self.page_size = page_size
        self.node_id = node_id

        self._js_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), self.JS_FILENAME
        )
        self._js_ctx = self._load_js()
        self._session = requests.Session()

    # ---------- 只读属性 ----------

    @property
    def params(self) -> dict:
        """请求 query 参数。"""
        return {"domainId": self.domain_id}

    # ---------- 私有方法 ----------

    def _load_js(self):
        with open(self._js_path, encoding="utf-8") as f:
            return execjs.compile(f.read())

    def _sign(self, page: int) -> dict:
        """调用 JS 的 get_par() 生成签名头。"""
        return self._js_ctx.call("get_par", page)

    def _build_data(self, page: int) -> str:
        """构造请求体；序列化结果必须与 JS 中 Content-Md5 计算的字符串一致。"""
        data = {
            "pageNo": page,
            "pageSize": self.page_size,
            "condition": {"nodeId": self.node_id},
        }
        return json.dumps(data, separators=(",", ":"))

    def _build_headers(self, page: int) -> dict:
        """拼装完整请求头（含签名字段）。"""
        sign = self._sign(page)
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Md5": sign["Content-Md5"],
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
            "x-date": str(sign["x-date"]),
            "x-nonce": sign["x-nonce"],
            "x-signature": sign["x-signature"],
            "x-user": sign["x-user"],
        }

    # ---------- 公共方法 ----------

    def fetch_page(self, page: int) -> list:
        """请求指定页，返回数据列表。"""
        response = self._session.post(
            self.BASE_URL,
            headers=self._build_headers(page),
            params=self.params,
            data=self._build_data(page),
            timeout=15,
        )
        return response.json()["data"]["data"]

    def fetch_all(self, pages: int) -> list:
        """请求前 pages 页，汇总返回。"""
        result = []
        for page in range(pages):
            result.extend(self.fetch_page(page))
        return result


def main() -> None:
    client = BaoGang()
    for item in client.fetch_page(0):
        print(json.dumps(item, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
