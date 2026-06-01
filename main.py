import os
import argparse
from core.downloader import download_audio
from core.asr_engine import transcribe_audio
from core.llm_agent import summarize_transcript
from core.file_manager import save_to_obsidian

def process_podcast(url: str):
    print("=== Podcast AI Assistant Pipeline Started ===")
    
    # 1. Download
    print(f"\n[1/4] Downloading audio from {url}...")
    audio_path, title = download_audio(url)
    
    # 2. Transcribe
    print(f"\n[2/4] Transcribing audio...")
    transcript = transcribe_audio(audio_path)
    
    # 3. Summarize
    print(f"\n[3/4] Summarizing with MIMO API...")
    summary = summarize_transcript(transcript, title)
    
    # 4. Save
    print(f"\n[4/4] Saving to Knowledge Base...")
    save_to_obsidian(title, summary, transcript)
    
    # Clean up temp audio
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"Cleaned up temporary audio: {audio_path}")

    print("\n=== Pipeline Completed Successfully! ===")
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Podcast AI Feishu Bot - Local Tester")
    parser.add_argument("url", type=str, help="The URL of the podcast/video to process")
    args = parser.parse_args()
    
    process_podcast(args.url)
