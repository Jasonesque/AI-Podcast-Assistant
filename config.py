import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # API Settings
    MIMO_API_KEY: str = os.getenv("MIMO_API_KEY", "")
    MIMO_API_BASE: str = "https://token-plan-cn.xiaomimimo.com/v1"
    MODEL_NAME: str = "mimo-v2.5"

    # Feishu Bot Settings
    FEISHU_APP_ID: str = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET: str = os.getenv("FEISHU_APP_SECRET", "")

    # Paths
    WORKSPACE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TMP_AUDIO_DIR: str = os.path.join(WORKSPACE_DIR, "tmp_audio")
    KNOWLEDGE_BASE_DIR: str = r"D:\AI-Agent-Workspace\Knowledge-Base"
    
    # ASR Settings
    WHISPER_MODEL_SIZE: str = "small"  # Using small for speed during testing, can be upgraded to large-v3

settings = Settings()

# Ensure directories exist
os.makedirs(settings.TMP_AUDIO_DIR, exist_ok=True)
os.makedirs(settings.KNOWLEDGE_BASE_DIR, exist_ok=True)
