from fastapi import FastAPI, BackgroundTasks, Request
import uvicorn
import json

from core.feishu_client import FeishuClient
from main import process_podcast

app = FastAPI(title="Feishu Podcast Bot")
feishu = FeishuClient()

def process_and_reply(open_id: str, url: str):
    feishu.send_message(open_id, f"✅ 已收到链接，正在调用本地 GPU 进行硬核转写中...\n(这通常需要1-3分钟，请耐心等待)")
    try:
        # process_podcast runs synchronously.
        summary = process_podcast(url)
        # Send brief summary back to Feishu
        reply_text = f"🎉 处理完成！\n\n{summary}\n\n[完整逐字稿笔记已同步至电脑端 Obsidian]"
        feishu.send_message(open_id, reply_text)
    except Exception as e:
        feishu.send_message(open_id, f"❌ 处理失败，请检查电脑端终端日志: {str(e)}")

@app.post("/webhook")
async def feishu_webhook(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    
    # URL Verification for Feishu setup
    if "challenge" in data:
        return {"challenge": data["challenge"]}
        
    # Handle Event V2.0
    if "header" in data and data["header"]["event_type"] == "im.message.receive_v1":
        event = data.get("event", {})
        message = event.get("message", {})
        sender = event.get("sender", {}).get("sender_id", {})
        open_id = sender.get("open_id")
        
        if message.get("message_type") == "text":
            content_str = message.get("content", "{}")
            content_dict = json.loads(content_str)
            text = content_dict.get("text", "").strip()
            
            # Simple URL extraction (assume the whole text is a URL or contains one)
            if "http" in text:
                # Find the first string that starts with http
                url = [word for word in text.split() if "http" in word][0]
                # Background processing so we can return 200 OK immediately
                background_tasks.add_task(process_and_reply, open_id, url)
            else:
                feishu.send_message(open_id, "主人好！请直接扔给我一个包含播客或视频链接（支持 B站/小宇宙/YouTube 等）的文本，我来帮你提取干货！")
                
    return {"msg": "ok"}

if __name__ == "__main__":
    print("🚀 正在启动飞书机器人的本地监听服务端...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
