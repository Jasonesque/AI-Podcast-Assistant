import requests
import json
from config import settings

class FeishuClient:
    def __init__(self):
        self.app_id = settings.FEISHU_APP_ID
        self.app_secret = settings.FEISHU_APP_SECRET
        self.tenant_access_token = ""

    def get_tenant_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        res = requests.post(url, json=payload).json()
        self.tenant_access_token = res.get("tenant_access_token", "")
        return self.tenant_access_token

    def send_message(self, open_id: str, text: str):
        if not self.app_id or not self.app_secret:
            print("Feishu API keys not set!")
            return
            
        self.get_tenant_access_token()
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "receive_id": open_id,
            "msg_type": "text",
            "content": json.dumps({"text": text}, ensure_ascii=False)
        }
        res = requests.post(url, headers=headers, json=payload).json()
        if res.get("code") != 0:
            print(f"Feishu API error: {res}")
