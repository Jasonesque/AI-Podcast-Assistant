import os
import yt_dlp
from config import settings

def download_audio(url: str) -> str:
    """
    Downloads audio from a given URL and saves it as an MP3 file in the TMP_AUDIO_DIR.
    Returns the absolute path to the downloaded audio file.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(settings.TMP_AUDIO_DIR, '%(id)s.%(ext)s'),
        'retries': 10,
        'fragment_retries': 10,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.bilibili.com/'
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # Construct the final path
        filename = f"{info['id']}.mp3"
        filepath = os.path.join(settings.TMP_AUDIO_DIR, filename)
        return filepath, info.get('title', 'Unknown Title')
