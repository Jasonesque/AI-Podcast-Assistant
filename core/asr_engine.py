import os
from faster_whisper import WhisperModel
from config import settings

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes the given audio file using faster-whisper.
    Returns the full transcript as a string.
    """
    print(f"Loading Whisper model ({settings.WHISPER_MODEL_SIZE})...")
    # Using compute_type="int8" for CPU, or "float16" for GPU if available. 
    # Adjust based on environment. Defaulting to int8/cpu for safe local testing.
    model = WhisperModel(settings.WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")

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
