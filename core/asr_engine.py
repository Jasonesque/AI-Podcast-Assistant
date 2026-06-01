import os
import site
from faster_whisper import WhisperModel
from config import settings

# ==========================================
# 修复 Windows 下找不到 cublas64_12.dll 的问题
# ==========================================
try:
    import sys
    # 获取虚拟环境中的 site-packages 路径
    site_packages = [p for p in sys.path if 'site-packages' in p]
    if site_packages:
        sp = site_packages[0]
        paths_to_add = [
            os.path.join(sp, "nvidia", "cudnn", "bin"),
            os.path.join(sp, "nvidia", "cublas", "bin"),
            os.path.join(sp, "nvidia", "cuda_nvrtc", "bin"),
            os.path.join(sp, "nvidia", "cuda_runtime", "bin")
        ]
        for p in paths_to_add:
            if os.path.exists(p):
                os.add_dll_directory(p)
                os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")
except Exception as e:
    print(f"Warning: Failed to add CUDA DLL directories: {e}")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes the given audio file using faster-whisper.
    Returns the full transcript as a string.
    """
    print(f"Loading Whisper model ({settings.WHISPER_MODEL_SIZE})...")
    # Using compute_type="float16" for GPU
    model = WhisperModel(settings.WHISPER_MODEL_SIZE, device="cuda", compute_type="float16")

    print(f"Transcribing {audio_path}...")
    segments, info = model.transcribe(audio_path, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    transcript = ""
    for segment in segments:
        # segment.start, segment.end, segment.text
        line = f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}"
        print(line)  # 实时打印进度，让你知道它没卡死
        transcript += line + "\n"

    return transcript
