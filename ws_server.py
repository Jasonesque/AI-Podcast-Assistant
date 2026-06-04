import json
import threading
import lark_oapi as lark
from config import settings
from main import process_podcast
from core.feishu_client import FeishuClient

feishu = FeishuClient()

def process_and_reply(open_id: str, url: str):
    feishu.send_message(open_id, "✅ 已收到链接，正在调用本地 GPU 进行极速转写中...\n(请耐心等待...)")
    try:
        summary = process_podcast(url)
        reply_text = f"🎉 处理完成！\n\n{summary}\n\n[完整笔记已同步至电脑端 Obsidian]"
        feishu.send_message(open_id, reply_text)
    except Exception as e:
        feishu.send_message(open_id, f"❌ 处理失败，请检查终端日志: {str(e)}")

def do_message_receive(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    try:
        import re
        message = data.event.message
        sender = data.event.sender.sender_id
        open_id = sender.open_id
        
        # Feishu Desktop often sends links as 'post' (Rich Text) instead of plain 'text'.
        # We bypass the type check and just search for any http/https link in the raw JSON string.
        content_str = message.content
        
        # Regex to find the first URL
        urls = re.findall(r'https?://[^\s\"\'\\]+', content_str)
        
        if urls:
            url = urls[0]
            # Background thread so we don't block the WS connection
            threading.Thread(target=process_and_reply, args=(open_id, url)).start()
        else:
            feishu.send_message(open_id, "主人好！没识别到有效的网址，请直接发给我包含播客或视频链接的内容。")
            
    except Exception as e:
        print(f"Error parsing Feishu WS event: {e}")

# The first two parameters are encryption_key and verification_token, which are not strictly needed for WS local dev
event_handler = lark.EventDispatcherHandler.builder("", "") \
    .register_p2_im_message_receive_v1(do_message_receive) \
    .build()

def main():
    print("🚀 正在启动飞书机器人的本地 WebSocket 长连接服务...")
    print("🔗 这种模式不需要任何内网穿透（无需 Ngrok / Cloudflare）！")
    print("等待飞书消息中...")
    
    cli = lark.ws.Client(
        settings.FEISHU_APP_ID, 
        settings.FEISHU_APP_SECRET, 
        event_handler=event_handler
    )
    cli.start()

if __name__ == "__main__":
    main()
