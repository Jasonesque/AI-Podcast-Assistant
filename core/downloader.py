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
        'proxy': '', # Bypass system proxy for direct domestic download
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
